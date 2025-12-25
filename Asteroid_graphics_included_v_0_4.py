import pygame, random, copy
from pygame.locals import *
import sys
import json
import math
import time



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
imp = pygame.image.load("Asteroid//vesmir_2.jpg")

class Asteroid:
    def __init__(self, x):
        self.asteroid_x_coord = x
        self.asteroid_y_coord = 0
        self.asteroid_size = ASTEROID_SIZE
        self.color = GREY
        self.mass = 1
        self.track = False
        self.image = pygame.image.load("Asteroid/" + random.choice(['asteroid_1.png','asteroid_2.png','asteroid_3.png']))
        #self.image = pygame.transform.scale(img, (ASTEROID_SIZE*self.mass*1.5, ASTEROID_SIZE*self.mass*1.5))

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
    ship = Ship()
    key_down = set()
    direction = None
    direction_2 = None
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
                a.move_down(2, ship)
            elif direction_2 == "down":
                a.move_down(1/2, ship)
            elif direction_2 == None:
                a.move_down(1, ship)

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
        asteroid_rect = pygame.Rect(asteroid.asteroid_x_coord, asteroid.asteroid_y_coord, ASTEROID_SIZE*asteroid.mass, ASTEROID_SIZE*asteroid.mass)
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
    global score
    global raketka
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(imp.convert(), (0,0))
    img = pygame.image.load("Asteroid/" + raketka)
    img = pygame.transform.scale(img, (SHIP_SIZE, SHIP_SIZE))
    DISPLAY_SURF.blit(img, (ship.x, TOP_SHIP))

    for a in asteroids:            
            image = pygame.transform.scale(a.image, (ASTEROID_SIZE*a.mass, ASTEROID_SIZE*a.mass))
            DISPLAY_SURF.blit(image, (a.asteroid_x_coord,a.asteroid_y_coord))

            
            
    if laser is not None:
        pygame.draw.rect(DISPLAY_SURF, (RED), laser)

    # Draw score
    score_surface = BASIC_FONT.render('Score: ' + str(score), True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAY_SURF.blit(score_surface, score_rect)
    save_json(score, raketka)
    score, raketka = load_json()
        
def main():
    global DISPLAY_SURF, BASIC_FONT, FPSCLOCK
    
    pygame.init()
    pygame.mixer.init()
    DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Asteroid")
    BASIC_FONT = pygame.font.Font("freesansbold.ttf", BASIC_FONT_SIZE)
    FPSCLOCK = pygame.time.Clock()
    global score
    global raketka
    score, raketka = load_json()
    
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
    img = pygame.image.load('Asteroid/asteroid_bg_image.png')
    image = pygame.transform.scale(img, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAY_SURF.blit(image, (0,0))
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
        msg1_surface = BASIC_FONT.render('Stlačte kláves pre pokračovanie.', True, WHITE)
        msg1_rect = msg1_surface.get_rect()
        msg1_rect.topleft = (WINDOWWIDTH - 350, WINDOWHEIGHT - 60)
        DISPLAY_SURF.blit(msg1_surface, msg1_rect)
        msg2_surface = BASIC_FONT.render('Stlačte "b" pre vstup do obchodu.', True, WHITE)
        msg2_rect = msg2_surface.get_rect()
        msg2_rect.topleft = (WINDOWWIDTH - 350, WINDOWHEIGHT - 30)
        DISPLAY_SURF.blit(msg2_surface, msg2_rect)
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
    img = pygame.image.load('Asteroid/asteroid_bg_game_over_screen.png')
    image = pygame.transform.scale(img, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAY_SURF.blit(image, (0,0))
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

    run_game()

def get_button_clicked(x, y, buttons):
    for button in buttons:
        if button.collidepoint((x, y)):
            return button
        
def shop_screen():
    while True:
        global score
        global raketka
        save_json(score, raketka)
        score, raketka = load_json()

        # Background    asteroid_bg_shop
        DISPLAY_SURF.fill(BLACK)
        img = pygame.image.load('Asteroid/asteroid_bg_shop.png')
        image = pygame.transform.scale(img, (WINDOWWIDTH, WINDOWHEIGHT))
        DISPLAY_SURF.blit(image, (0,0))


        # Draw title
        shop_font = pygame.font.Font('freesansbold.ttf', 50)
        obchod_surface = shop_font.render('Obchod', True, WHITE)
        obchod_rect = obchod_surface.get_rect()
        obchod_rect.midtop = (WINDOWWIDTH / 2, 20)
        DISPLAY_SURF.blit(obchod_surface, obchod_rect)

        # Draw score
        score_font = pygame.font.Font('freesansbold.ttf', 30)
        score_surface = score_font.render('Score: ' + str(score), True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (WINDOWWIDTH - 180, 30)
        DISPLAY_SURF.blit(score_surface, score_rect)

        # Draw buttons
        buttons = []
        # Ruleta button
        ruleta_text_surface = BASIC_FONT.render('Ruleta', True, BLACK)
        ruleta_text_rect = ruleta_text_surface.get_rect()
        ruleta_text_rect.topleft = (WINDOWWIDTH//2 - 35, WINDOWHEIGHT//2 - 20)
        ruleta_button_rect = pygame.Rect(WINDOWWIDTH//2 - 110, WINDOWHEIGHT//2 - 30, 200, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, ruleta_button_rect)
        DISPLAY_SURF.blit(ruleta_text_surface, ruleta_text_rect)

        buttons.append(ruleta_button_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_b:
                    run_game()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                button_clicked = get_button_clicked(mouse_position[0], mouse_position[1], buttons)
                if button_clicked == ruleta_button_rect:
                    ruleta_screen()

def ruleta_screen():
    global score
    betted_amount = 0
    while True:
        DISPLAY_SURF.fill(WHITE)
        

        # Draw title
        ruleta_font = pygame.font.Font('freesansbold.ttf', 50)
        ruleta_title_surface = ruleta_font.render('Ruleta', True, BLACK)
        ruleta_title_rect = ruleta_title_surface.get_rect()
        ruleta_title_rect.midtop = (WINDOWWIDTH / 2, 20)
        DISPLAY_SURF.blit(ruleta_title_surface, ruleta_title_rect)

        # Draw score
        score_font = pygame.font.Font('freesansbold.ttf', 30)
        score_surface = score_font.render('Score: ' + str(score), True, BLACK)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (WINDOWWIDTH - 180, 30)
        DISPLAY_SURF.blit(score_surface, score_rect)

        # Draw buttons
        buttons = []

        # bet button
        bet_button_font = pygame.font.Font('freesansbold.ttf', 30)
        ruleta_text_surface = bet_button_font.render('Bet', True, BLACK)
        ruleta_text_rect = ruleta_text_surface.get_rect()
        ruleta_text_rect.topleft = (WINDOWWIDTH//2 - 35, WINDOWHEIGHT - 45)
        ruleta_button_rect = pygame.Rect(WINDOWWIDTH//2 - 110, WINDOWHEIGHT - 50, 200, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, ruleta_button_rect)
        DISPLAY_SURF.blit(ruleta_text_surface, ruleta_text_rect)
        buttons.append(ruleta_button_rect)

        # +1 button
        plus_1_button_font = pygame.font.Font('freesansbold.ttf', 30)
        plus_1_text_surface = plus_1_button_font.render('+1', True, BLACK)
        plus_1_text_rect = plus_1_text_surface.get_rect()
        plus_1_text_rect.topleft = (WINDOWWIDTH - 90, WINDOWHEIGHT - 45)
        plus_1_button_rect = pygame.Rect(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, 90, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, plus_1_button_rect)
        DISPLAY_SURF.blit(plus_1_text_surface, plus_1_text_rect)
        buttons.append(plus_1_button_rect)

        # -1 button
        minus_1_button_font = pygame.font.Font('freesansbold.ttf', 30)
        minus_1_text_surface = minus_1_button_font.render('-1', True, BLACK)
        minus_1_text_rect = minus_1_text_surface.get_rect()
        minus_1_text_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 45)
        minus_1_button_rect = pygame.Rect(WINDOWWIDTH - 210, WINDOWHEIGHT - 50, 90, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, minus_1_button_rect)
        DISPLAY_SURF.blit(minus_1_text_surface, minus_1_text_rect)
        buttons.append(minus_1_button_rect)

        # +10 button
        plus_10_button_font = pygame.font.Font('freesansbold.ttf', 30)
        plus_10_text_surface = plus_10_button_font.render('+10', True, BLACK)
        plus_10_text_rect = plus_10_text_surface.get_rect()
        plus_10_text_rect.topleft = (WINDOWWIDTH - 90, WINDOWHEIGHT - 95)
        plus_10_button_rect = pygame.Rect(WINDOWWIDTH - 100, WINDOWHEIGHT - 100, 90, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, plus_10_button_rect)
        DISPLAY_SURF.blit(plus_10_text_surface, plus_10_text_rect)
        buttons.append(plus_10_button_rect)

        # -10 button
        minus_10_button_font = pygame.font.Font('freesansbold.ttf', 30)
        minus_10_text_surface = minus_10_button_font.render('-10', True, BLACK)
        minus_10_text_rect = minus_10_text_surface.get_rect()
        minus_10_text_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 95)
        minus_10_button_rect = pygame.Rect(WINDOWWIDTH - 210, WINDOWHEIGHT - 100, 90, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, minus_10_button_rect)
        DISPLAY_SURF.blit(minus_10_text_surface, minus_10_text_rect)
        buttons.append(minus_10_button_rect)

        # +100 button
        plus_100_button_font = pygame.font.Font('freesansbold.ttf', 30)
        plus_100_text_surface = plus_100_button_font.render('+100', True, BLACK)
        plus_100_text_rect = plus_100_text_surface.get_rect()
        plus_100_text_rect.topleft = (WINDOWWIDTH - 90, WINDOWHEIGHT - 145)
        plus_100_button_rect = pygame.Rect(WINDOWWIDTH - 100, WINDOWHEIGHT - 150, 90, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, plus_100_button_rect)
        DISPLAY_SURF.blit(plus_100_text_surface, plus_100_text_rect)
        buttons.append(plus_100_button_rect)

        # -100 button
        minus_100_button_font = pygame.font.Font('freesansbold.ttf', 30)
        minus_100_text_surface = minus_100_button_font.render('-100', True, BLACK)
        minus_100_text_rect = minus_100_text_surface.get_rect()
        minus_100_text_rect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 145)
        minus_100_button_rect = pygame.Rect(WINDOWWIDTH - 210, WINDOWHEIGHT - 150, 90, 40)
        pygame.draw.rect(DISPLAY_SURF, GREY, minus_100_button_rect)
        DISPLAY_SURF.blit(minus_100_text_surface, minus_100_text_rect)
        buttons.append(minus_100_button_rect)

        # red bet button
        red_button_font = pygame.font.Font('freesansbold.ttf', 30)
        red_text_surface = red_button_font.render('Red', True, WHITE)
        red_text_rect = red_text_surface.get_rect()
        red_text_rect.topleft = (55, WINDOWHEIGHT - 145)
        red_button_rect = pygame.Rect(45, WINDOWHEIGHT - 150, 100, 40)
        pygame.draw.rect(DISPLAY_SURF, RED, red_button_rect)
        DISPLAY_SURF.blit(red_text_surface, red_text_rect)
        buttons.append(red_button_rect)

        # black bet button
        black_button_font = pygame.font.Font('freesansbold.ttf', 30)
        black_text_surface = black_button_font.render('Black', True, WHITE)
        black_text_rect = black_text_surface.get_rect()
        black_text_rect.topleft = (55, WINDOWHEIGHT - 95)
        black_button_rect = pygame.Rect(45, WINDOWHEIGHT - 100, 100, 40)
        pygame.draw.rect(DISPLAY_SURF, BLACK, black_button_rect)
        DISPLAY_SURF.blit(black_text_surface, black_text_rect)
        buttons.append(black_button_rect)

        # green bet button
        green_button_font = pygame.font.Font('freesansbold.ttf', 30)
        green_text_surface = green_button_font.render('Green', True, WHITE)
        green_text_rect = green_text_surface.get_rect()
        green_text_rect.topleft = (55, WINDOWHEIGHT - 195)
        green_button_rect = pygame.Rect(45, WINDOWHEIGHT - 200, 100, 40)
        pygame.draw.rect(DISPLAY_SURF, RED, green_button_rect)
        DISPLAY_SURF.blit(green_text_surface, green_text_rect)
        buttons.append(green_button_rect)

        # betted amount text
        minus_100_button_font = pygame.font.Font('freesansbold.ttf', 30)
        minus_100_text_surface = minus_100_button_font.render("your bet: " + str(betted_amount), True, BLACK)
        minus_100_text_rect = minus_100_text_surface.get_rect()
        minus_100_text_rect.topleft = (WINDOWWIDTH - 210, WINDOWHEIGHT - 200)
        DISPLAY_SURF.blit(minus_100_text_surface, minus_100_text_rect)

        draw_ruleta(-0.1,0,124)
        pygame.display.update()
        FPSCLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                button_clicked = get_button_clicked(mouse_position[0], mouse_position[1], buttons)
                if button_clicked == ruleta_button_rect:
                    spin()
                    time.sleep(2)
                elif button_clicked == plus_1_button_rect:
                    if score - 1 >= 0:
                        betted_amount += 1
                        score -= 1
                elif button_clicked == minus_1_button_rect:
                    if betted_amount - 1 >= 0:
                        betted_amount -= 1
                        score += 1
                elif button_clicked == plus_10_button_rect:
                    if score - 10 >= 0:
                        betted_amount += 10
                        score -= 10
                elif button_clicked == minus_10_button_rect:
                    if betted_amount - 10 >= 0:
                        betted_amount -= 10
                        score += 10
                elif button_clicked == plus_100_button_rect:
                    if score - 100 >= 0:
                        betted_amount += 100
                        score -= 100
                elif button_clicked == minus_100_button_rect:
                    if betted_amount - 100 >= 0:
                        betted_amount -= 100
                        score += 100

def play_shot_sound():
    pygame.mixer.music.load("gunshot.mp3")
    pygame.mixer.music.set_volume(0.7),
    pygame.mixer.music.play()

def load_json():
    with open('Asteroid/data_asteroid.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data["score"], data["raketka"]

def save_json(data, raketka):
    data = {"score": data,
            "raketka": raketka}
    data = json.dumps(data)
    with open('Asteroid/data_asteroid.json', 'w') as f:
        f.write(data)
        f.close()


#
#RULETA
#
def slow_down_ball_by_air_resistence(v, delta_t):
    m = 0.006 #6gramov
    r = 0.009 #9mm
    if v > 0:
        direction = 1
    else:
        direction = -1
    v = abs(v)
    old_v = v
    v = v - (0.5*1.225*0.4*math.pi*(r**2)*(v**2))/m*delta_t
    #assert v >= 0
    #assert v <= old_v
    return v * direction

def spin():
    speed = random.randint(1000, 2000)
    a = 0.5
    b = 0.5
    time_of_rulet = 0
    start_speed = speed
    movement = 0
    ball_speed = 0
    ball_speed_centrifugal = 0
    ball_position_centrifugal = 124
    ball_position = 0
    ball_fly_timeout = 0
    while speed > 5:
        old_ball_position = ball_position-movement
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        if ball_fly_timeout > 0:
            ball_fly_timeout -= 1
        speed = ((a+b*start_speed)* math.e ** (-b*time_of_rulet) - a) / b
        time_of_rulet += 1/FPS
        movement += math.pi/360/FPS*speed
        if movement >= math.pi * 2:
            movement = 0
        ball_speed = slow_down_ball_by_air_resistence(ball_speed, 1/FPS)
        ball_speed_centrifugal += 0.006**2*ball_speed**2*ball_position_centrifugal/FPS
        if ball_position_centrifugal >= 132:
            ball_position_centrifugal = 132
            ball_speed_centrifugal = (0 - 0.8 * ball_speed_centrifugal)
        if ball_position_centrifugal <= 118:
            ball_position_centrifugal = 118
            ball_speed_centrifugal = (0 - 0.8 * ball_speed_centrifugal)
        ball_position_centrifugal += ball_speed_centrifugal/FPS
        ball_position += math.pi/360/FPS*ball_speed
        if ball_position >= math.pi * 2:
            ball_position = 0
        if ((38*(ball_position+1-movement)/(2*math.pi))//1 != (38*(old_ball_position+1-movement)/(2*math.pi))//1 ) and ball_fly_timeout == 0:
            ball_speed = (speed - 0.8 * (ball_speed - speed))
            ball_fly_timeout = random.randint(50, 150)  
        DISPLAY_SURF.fill(WHITE)
        draw_ruleta(movement, ball_position, ball_position_centrifugal)
        FPSCLOCK.tick(FPS)
    if (38*(ball_position+1-movement)/(2*math.pi)) < (38*(ball_position+1-movement)/(2*math.pi))//1 + 0.2:
        ball_position = (((38*(ball_position+1-movement)/(2*math.pi))//1 + 0.2)*math.pi)/19 + movement - 1
    elif (38*(ball_position+1-movement)/(2*math.pi)) > (38*(ball_position+1-movement)/(2*math.pi))//1 + 0.8:
        ball_position = (((38*(ball_position+1-movement)/(2*math.pi))//1 + 0.8)*math.pi)/19 + movement - 1
    result_position = 38*(ball_position-movement)/(2*math.pi)
    draw_ruleta(movement, ball_position, ball_position_centrifugal)
    if result_position < 0:
        result_position += 38
    result_position = result_position // 1
    return int(result_position)

def draw_ruleta(movement, ball, ball_position_centrifugal):
    center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    radius = 200

    pygame.draw.circle(DISPLAY_SURF, BLACK, center, radius)
    pygame.draw.circle(DISPLAY_SURF, WHITE, center, radius-15)

    
    for x in range(0, 38, 2):
        draw_circular_cutout(center, radius-20, DISPLAY_SURF, RED, math.pi/19*x + movement, math.pi/19*(x+1) + movement)
        draw_circular_cutout(center, radius-20, DISPLAY_SURF, BLACK, math.pi/19*(x+1) + movement, math.pi/19*(x+2) + movement)
    draw_circular_cutout(center, radius-20, DISPLAY_SURF, GREEN, math.pi/19 + movement, math.pi/19*2 + movement)
    pygame.draw.circle(DISPLAY_SURF, WHITE, center, radius-55)
    for x in range(0, 38, 2):
        for y in range(0, 2):
            number_text_surface = BASIC_FONT.render(str(x+y), True, WHITE)
            rotated_surface = pygame.transform.rotozoom(number_text_surface, -math.degrees(math.pi/19*(x+y) + movement + math.pi/38)-90, 1)
            rotated_rect = rotated_surface.get_rect(center=(math.cos(math.pi/19*(x+y) + movement + math.pi/38) * (radius - 35) + (WINDOWWIDTH // 2), math.sin(math.pi/19*(x+y) + movement + math.pi/38) * (radius - 35) + (WINDOWHEIGHT // 2)))
            DISPLAY_SURF.blit(rotated_surface, rotated_rect)
        draw_circular_cutout(center, radius-60, DISPLAY_SURF, RED, math.pi/19*x + movement, math.pi/19*(x+1) + movement)
        draw_circular_cutout(center, radius-60, DISPLAY_SURF, BLACK, math.pi/19*(x+1) + movement, math.pi/19*(x+2) + movement)
    draw_circular_cutout(center, radius-60, DISPLAY_SURF, GREEN, math.pi/19 + movement, math.pi/19*2 + movement)
    for x in range(0, 380, 10):
        draw_circular_cutout(center, radius-17, DISPLAY_SURF, WHITE, math.pi/190*x + movement, math.pi/190*(x+1) + movement)
    pygame.draw.circle(DISPLAY_SURF, WHITE, center, radius-90)
    pygame.draw.circle(DISPLAY_SURF, BLACK, center, radius-95)
    center_of_ball = (math.cos(ball) * ball_position_centrifugal + (WINDOWWIDTH // 2), math.sin(ball) * ball_position_centrifugal + (WINDOWHEIGHT // 2))
    pygame.draw.circle(DISPLAY_SURF, BLUE,  center_of_ball, 8)

    numbers_font = pygame.font.Font('freesansbold.ttf', 15)
    numbers_surface = numbers_font.render('Game', True, WHITE)
    numbers_rect = numbers_surface.get_rect()

    
    pygame.display.update()

def draw_circular_cutout(center, radius, display, color, start_angle, end_angle):
    steps = 30
    points = [center]
    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(display, color, points)

if __name__ =="__main__":
    main()
