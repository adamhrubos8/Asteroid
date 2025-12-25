import pygame, random, copy
from pygame.locals import *
import sys
import json


WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BASIC_FONT_SIZE = 20
ASTEROID_SIZE = 40
SHIP_SIZE = 40
FPS = 30
TOP_SHIP = WINDOWHEIGHT - SHIP_SIZE - 10
BLACK = (0,0,0)
BLUE = (0,200,255)
GREY = (155,155,155)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

score = 0

class Asteroid:
    def __init__(self, x):
        self.asteroid_x_coord = x
        self.asteroid_y_coord = 0
        self.asteroid_size = ASTEROID_SIZE
        self.mass = 1
        self.track = False

    def move_down(self,speed,ship):
        self.asteroid_y_coord += 4* speed
        if self.track == True:
            if self.asteroid_x_coord < ship.x:
                self.asteroid_x_coord += 2
            elif self.asteroid_x_coord > ship.x:
                self.asteroid_x_coord -= 2  


class Ship:
    def __init__(self):
        self.x = WINDOWWIDTH//2 - SHIP_SIZE//2

def run_game():
    direction_2 = None
    ship = Ship()
    key_down = set()
    direction = None
    button = None
    shot = False
    laser = None
    laser_timer = 0
    shot_timer = 0
    asteroid_timer = 30
    asteroids = []

    while True:
        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            elif event.type == MOUSEBUTTONDOWN:
                button = event.button
                if button == 1:
                    shot = True 

            elif event.type == KEYDOWN:
                key = event.key
                if key in (K_a,K_d,K_w,K_s):
                    key_down.add(key)
            elif event.type == KEYUP:
                key = event.key
                if key in (K_a,K_d,K_w,K_s):
                    key_down.discard(key)

        if K_a in key_down and K_d in key_down:
            direction = None
        elif K_a in key_down or K_d in key_down:
            if K_a in key_down and K_d not in key_down:
                direction = "left"
            elif K_a not in key_down and K_d in key_down:
                direction = "right"
        elif K_a not in key_down and K_d not in key_down:
            direction = None

        if K_w in key_down and K_s in key_down:
            direction_2 = None
        elif K_w in key_down or K_s in key_down:
            if K_w in key_down and K_s not in key_down:
                direction_2 = "up"
            elif K_w not in key_down and K_s in key_down:
                direction_2 = "down"
        elif K_w not in key_down and K_s not in key_down:
            direction_2 = None
        
        if shot_timer == 0:
            if shot:
                laser = shoot_sniper(ship)
                laser_timer = 5
                shot_timer = 120
                shot = False
        elif shot_timer > 0:
            shot_timer -= 1
            shot = False
        
        if direction != None:
            ship_move(ship,direction)
        
        if laser != None:
            laser_timer -= 1
            if laser_timer <= 0:
                laser = None

        if asteroid_timer == 0:
            asteroids.append(generate_asteroid())
            asteroid_timer = random.choice([30,45,60,85,90])
        elif asteroid_timer > 0:
            asteroid_timer -= 1

        if check_game(ship,asteroids,laser):
            show_game_over_screen()

        for a in asteroids:
            if direction_2 == "up":
                a.move_down(2)
            elif direction_2 == "down":
                a.move_down(1/2)
            elif direction_2 == None:
                a.move_down(1)

        draw_board(ship, asteroids, laser)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def shoot_sniper(ship):
    laser = pygame.Rect(ship.x+18,-160,4,160+TOP_SHIP)
    play_shot_sound()
    return laser

def asteroid_break(asteroids,laser):
    global score
    asteroids_copy = copy.copy(asteroids)
    if laser != None:
        for asteroid in asteroids_copy:
            asteroid_rect = pygame.Rect(asteroid.asteroid_x_coord, asteroid.asteroid_y_coord, ASTEROID_SIZE, ASTEROID_SIZE)
            if laser.colliderect(asteroid_rect):
                if asteroid.color == GREEN:
                    score += 2
                elif asteroid.color == GREY:
                    score += 1
                asteroids.remove(asteroid)

def generate_asteroid():
    x = random.choice(range(0,WINDOWWIDTH-ASTEROID_SIZE))
    asteroid = Asteroid(x)

    if random.choice(range(5)) == 1:
        asteroid.mass = 2

    if random.choice(range(5)) == 1:
        asteroid.track = True

    return asteroid

def check_game(ship, asteroids,laser):
    ship_rect = pygame.Rect(ship.x,TOP_SHIP,SHIP_SIZE,SHIP_SIZE) 
    copy_asteroids = copy.copy(asteroids)
    for asteroid_lower in copy_asteroids:
        if asteroid_lower.asteroid_y_coord > WINDOWHEIGHT + 160:
            asteroids.remove(asteroid_lower)
    for asteroid in asteroids:
        asteroid_rect = pygame.Rect(asteroid.asteroid_x_coord, asteroid.asteroid_y_coord, ASTEROID_SIZE, ASTEROID_SIZE)
        if ship_rect.colliderect(asteroid_rect):
            return True
    asteroid_break(asteroids,laser)
    return False      

def ship_move(ship, direction):
    if direction == "right" and ship.x < WINDOWWIDTH - SHIP_SIZE -10:
        ship.x += 5
    elif direction == "left" and ship.x > 10:
        ship.x -= 5
        
def draw_board(ship, asteroids, laser):
    DISPLAY_SURF.fill(BLACK)
    pygame.draw.rect(DISPLAY_SURF, (BLUE),
                     (ship.x, TOP_SHIP, SHIP_SIZE, SHIP_SIZE))
    for a in asteroids:
            pygame.draw.rect(DISPLAY_SURF, (a.color),
                            (a.asteroid_x_coord, a.asteroid_y_coord,
                            ASTEROID_SIZE, ASTEROID_SIZE))
    if laser is not None:
        pygame.draw.rect(DISPLAY_SURF, (RED), laser)

    # Draw score
    score_surface = BASIC_FONT.render('Score: ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAY_SURF.blit(score_surface, score_rect)
        
def main():
    global DISPLAY_SURF, BASIC_FONT, FPSCLOCK
    
    pygame.init()
    pygame.mixer.init()
    DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Asteroid")
    BASIC_FONT = pygame.font.Font("freesansbold.ttf", BASIC_FONT_SIZE)
    FPSCLOCK = pygame.time.Clock()
    
    show_start_screen()
    run_game()

def terminate():
    pygame.quit()
    sys.exit()

def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surface = title_font.render('Asteroid!', True, WHITE)
    title_rect = title_surface.get_rect()
    title_rect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)

    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(title_surface, title_rect)
    wait_for_key_pressed()

def was_key_pressed():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_b:
                shop_screen()
            return True
    return False

def wait_for_key_pressed():
    while was_key_pressed() == False:
        msg_surface = BASIC_FONT.render('Press a key to continue.', True, GREY)
        msg_rect = msg_surface.get_rect()
        msg_rect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 30)
        DISPLAY_SURF.blit(msg_surface, msg_rect)
        pygame.display.update()

def show_game_over_screen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 150)
    game_surface = game_over_font.render('Game', True, WHITE)
    over_surface = game_over_font.render('Over', True, WHITE)
    game_rect = game_surface.get_rect()
    over_rect = over_surface.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(game_surface, game_rect)
    DISPLAY_SURF.blit(over_surface, over_rect)

    # Draw score
    game_over_score_font = pygame.font.Font('freesansbold.ttf', 50)
    score_surface = game_over_score_font.render('Score: ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 + 100)
    DISPLAY_SURF.blit(score_surface, score_rect)

    pygame.display.update()

    wait_for_key_pressed()

    terminate()

def get_button_clicked(x, y, buttons):
    for button in buttons:
        if button.collidepoint((x, y)):
            return button

def shop_screen():
    game_over_font = pygame.font.Font('freesansbold.ttf', 50)
    obchod_surface = game_over_font.render('Obchod', True, WHITE)
    obchod_rect = obchod_surface.get_rect()
    obchod_rect.midtop = (WINDOWWIDTH / 2, 10)
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(obchod_surface, obchod_rect)
    buttons = []
    ruleta_button = pygame.Rect(WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 - 25, 200, 50)
    pygame.draw.rect(DISPLAY_SURF, GREY, ruleta_button)
    buttons.append(ruleta_button)
    operations = {ruleta_button: spin()}
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_b:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()

    pygame.display.update()

    wait_for_key_pressed()

def play_shot_sound():
    pygame.mixer.music.load("gunshot.mp3")
    pygame.mixer.music.set_volume(0.7),
    pygame.mixer.music.play()

def load_json():
    with open('data.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data

def save_json(data):
    data = json.dumps(data)
    with open('data.json', 'w') as f:
        f.write(data)
        f.close()

if __name__ =="__main__":
    main()
