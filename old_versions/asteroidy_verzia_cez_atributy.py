import pygame, random
from pygame.locals import *
import sys

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
BASIC_FONT_SIZE = 20
ASTEROID_SIZE = 40
SHIP_SIZE = 40
FPS = 30
BLACK = (0,0,0)
GRAY = (100,100,100)
ASTEROID_SPEED = 2


asteroids = []
occuped_asteroid_spawn_positions = []

class Asteroid:
    def __init__(self, x, size):
        #suradnice laveho horneho rohu collide obdlznik
        self.asteroid_x_coord = x
        self.asteroid_y_coord = -40  #vrch obrazovky
        self.size = size
        self.speed = ASTEROID_SPEED
    def move_down(self):
        self.asteroid_y_coord += self.speed

def get_random_asteroid_spawn_x(size):
    space_between_asteroids = 10
    possible_positions = []
    free_asteroid_spawn_positions = [item for item in list(range(0, WINDOWWIDTH)) if item not in occuped_asteroid_spawn_positions ]
    for x in free_asteroid_spawn_positions:   #to v [] je list vsetkych pozicii minus list obsadených --> list volnych pozicii
        if x + size + space_between_asteroids < WINDOWWIDTH:
            for check_x in range(x - space_between_asteroids, x + size + space_between_asteroids):
                if check_x not in free_asteroid_spawn_positions:
                    break
            else:
                possible_positions.append(x)
    return possible_positions

def update_occuped_asteroid_spawn_positions():
    global occuped_asteroid_spawn_positions
    for asteroid in asteroids:
        if asteroid.asteroid_y_coord > 2 * ASTEROID_SIZE:
            x = asteroid.asteroid_x_coord
            size = asteroid.size
            occuped_asteroid_spawn_positions = [item for item in occuped_asteroid_spawn_positions if item not in list(range(x - 11, x + 11 + size))]
        if asteroid.asteroid_y_coord > WINDOWHEIGHT + ASTEROID_SIZE:
            asteroids.remove(asteroid)
    

def add_new_asteroid_occupated_positions_to_occuped_asteroid_spawn_positions(asteroid):
    x = asteroid.asteroid_x_coord
    size = asteroid.size
    new_asteroid_occupated_positions = list(range(x - 10, x + 10 + size))
    for pos in new_asteroid_occupated_positions:
        if pos in occuped_asteroid_spawn_positions:
            print("Chyba: pozicia je uz okupovana!", pos)
        occuped_asteroid_spawn_positions.append(pos)
    occuped_asteroid_spawn_positions.sort()        
            

def spawn_asteroid():
    update_occuped_asteroid_spawn_positions()
    size = random.randint(ASTEROID_SIZE//2, ASTEROID_SIZE)
    possible_x_positions = get_random_asteroid_spawn_x(size)
    if possible_x_positions == []:
        return
    x = random.choice(get_random_asteroid_spawn_x(size))
    new_asteroid = Asteroid(x, size)
    add_new_asteroid_occupated_positions_to_occuped_asteroid_spawn_positions(new_asteroid)
    return new_asteroid
    


class Ship:
    def __init__(self):
        #suradnice laveho horneho rohu
        self.ship_x_coord = WINDOWWIDTH//2 - SHIP_SIZE//2
        self.ship_y_coord = WINDOWHEIGHT - SHIP_SIZE - 10


def run_game():
    while True:
        if random.randint(1, 20) == 1:    #zo sancou 1 ku 20 sa spawnne asteroid
            new_asteroid = spawn_asteroid()
            if new_asteroid != None:
                asteroids.append(new_asteroid)
        draw_board()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def draw_board():
    DISPLAY_SURF.fill(BLACK)
    #vykreslit hracie pole    -->   vykreslit raketku

    for asteroid in asteroids:
        asteroid.move_down()
        asteroid_rect = pygame.Rect(asteroid.asteroid_x_coord, asteroid.asteroid_y_coord - ASTEROID_SIZE, asteroid.size, asteroid.size)
        pygame.draw.rect(DISPLAY_SURF, GRAY, asteroid_rect)

    pass
        
def main():
    global DISPLAY_SURF, BASIC_FONT, FPSCLOCK
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Asteroid")
    BASIC_FONT = pygame.font.Font("freesansbold.ttf", BASIC_FONT_SIZE)
    FPSCLOCK = pygame.time.Clock()

    #nieco s uvodnou obrazovkou

    run_game()


def terminate():
    pygame.quit()
    sys.exit()

if __name__ =="__main__":
    main()









"""  nejake poznamky

pygame.sprite.collide_mask()   zistit ako to funguje

lod dole na hracej ploche ide doprava-doľava

asteroidy idu smerom dole

vytvorit zoznam miest okupovaných asteroidamy

"""
