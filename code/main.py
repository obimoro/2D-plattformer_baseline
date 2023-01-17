# Dinosaur sprite by Arks
# https://arks.itch.io/dino-characters
# Twitter:  @ScissorMarks
 
import pygame as pg

# constant variables 
# screen dimensions
SCR_W = 800
SCR_H = 600
# colors
BLACK = (0,0,0)
WHITE = ( 255,255,255)
GREY = (125,125,125)
ORANGE = (255,125,0)

running = True

# INIT ------------
pg.init()
screen = pg.display.set_mode((SCR_W, SCR_H))
pg.display.set_caption('2D Platform')
# timing
clock = pg.time.Clock()

# player
player_image = pg.image.load('graphics/DinoSprites - doux/doux_00.png').convert_alpha()
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.2

# platforms
platforms = [
    pg.Rect(100, 300, 400, 50),
    pg.Rect(100, 250,  50, 50),
    pg.Rect(450, 250,  50, 50)
]

# game loop
while running:

    # INPUT ---------------
    # check for quit
    for event in    pg.event.get():
        if event.type == pg.QUIT:
            running = False


    new_player_x = player_x
    new_player_y = player_y
    # player input 
    keys = pg.key.get_pressed()    
    # left
    if keys[pg.K_a]:
        new_player_x -= 2
    # right
    if keys[pg.K_d]:
        new_player_x += 2
    # jump
    if keys[pg.K_w]:
        player_speed = -5

    # horizontal movement
    new_player_rect = pg.Rect(new_player_x, player_y, 72,72)
    x_collision = False

    # check against every platform 
    for p in platforms:
        if p.colliderect(new_player_rect):
            x_collision = True
            break

    if x_collision == False:
       player_x = new_player_x

    # vertical movment
    player_speed += player_acceleration
    new_player_y += player_speed

    new_player_rect = pg.Rect(player_x, new_player_y, 72,72)
    y_collision = False

    # check against every platform 
    for p in platforms:
        if p.colliderect(new_player_rect):
            y_collision = True
            player_speed = 0
            break

    if y_collision == False:
       player_y = new_player_y


    # update

    # RENDER ------------
    # Background
    screen.fill(ORANGE)
    #platform
    for p in platforms:
        pg.draw.rect(screen, GREY, p)
    # Player
    screen.blit(player_image, (player_x,player_y))
    # present screen
    pg.display.flip()

    clock.tick(60)

# quit
pg.quit()