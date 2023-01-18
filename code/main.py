# Dinosaur sprite by Arks
# https://arks.itch.io/dino-characters
# Twitter:  @ScissorMarks
#
# Coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0
#
# Enemy sprite by bevouliin.com
# https://opengameart.org/content/bevouliin-free-ingame-items-spike-monsters
#
# Font by Jayvee D anaguas (Grand Chaos)
# https://www.dafont.com/grand9k-pixel.font
#
# Heart sprite by Nicole Marie T
# https://opengameart.org/content/heart-1616

import pygame as pg

# function
def drawText(text, x, y):
    text = font.render(text, False, WHITE, None)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)

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
# font
font = pg.font.Font('graphics/font/Grand9K Pixel.ttf', 24)

#game states = playing // win // lose
game_state = 'playing'

# player
player_image = pg.image.load('graphics/DinoSprites - doux/doux_00.png').convert_alpha()
player_x = 300

player_y = 0
player_speed = 0
player_acceleration = 0.2

player_width = 44
player_height = 51

# platforms
platforms = [
    pg.Rect(100, 300, 400, 50),
    pg.Rect(100, 250,  50, 50),
    pg.Rect(450, 250,  50, 50)
]

# coins
coin_image = pg.image.load('graphics/coin/coin_0.png').convert_alpha()
coins = [
        pg.Rect(100, 200, 23, 23),
        pg.Rect(200, 250, 23, 23)
]

score = 0

# enemies
enemy_image = pg.image.load('graphics/enemy/spike monster B.png').convert_alpha()
enemies = [
    pg.Rect(150,275,50,26)
]

lives = 3
heart_image = pg.image.load('graphics/heart/heart.png').convert_alpha()

# game loop
while running:

    # INPUT ---------------
    # check for quit
    for event in    pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if game_state == 'playing':
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
        # jump ( if on the ground)
        if keys[pg.K_w] and player_on_ground:
            player_speed = -5

    # UPDATE -----

    if game_state == 'playing':
        # horizontal movement
        new_player_rect = pg.Rect(new_player_x, player_y, player_width,player_height)
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

        new_player_rect = pg.Rect(player_x, new_player_y, player_width,player_height)
        y_collision = False
        player_on_ground = False

        # check against every platform 
        for p in platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                # if platform is below the player
                if p[1] > new_player_y:
                    # stick the player to the platform
                    player_y = p[1] - player_height
                    player_on_ground = True
                break

        if y_collision == False:
            player_y = new_player_y


        # see if any coins have been collected
        player_rect = pg.Rect(player_x, player_y, player_width, player_height)
        for c in coins:
            if c.colliderect(player_rect):
                coins.remove(c)
                score += 1
                # change the game state
                # if all coins are collected
                if score >= 2:
                    game_state = 'win'

        
        # see if any enemies have been collided with
        for e in enemies:
            if e.colliderect(player_rect):
                lives -= 1
                player_y = 0
                player_speed = 0
                # change the game state
                # if no lives remaining
                if lives <= 0:
                    game_state = 'lose'
        

    # RENDER ------------


    # Background
    screen.fill(ORANGE)



    # platform
    for p in platforms:
        pg.draw.rect(screen, GREY, p)

    # coins
    for c in coins:
            screen.blit(coin_image, (c[0],c[1]))

    # enemies
    for e in enemies:
            screen.blit(enemy_image, (e[0],e[1]))
    # Player
    screen.blit(player_image, (player_x,player_y))

    # player information

    # score
    drawText(('Score: ' + str(score)), SCR_W // 2, 10)

    
    # lives
    for l in range(lives):
        screen.blit(heart_image, (10 + (l * 30), 10))

    if game_state == 'win':
        drawText('You win!', SCR_W // 2, SCR_H // 2)
        
    if game_state == 'lose':
        drawText('You lose!', SCR_W // 2, SCR_H // 2)

    # present screen
    pg.display.flip()
 
    clock.tick(60)

# quit
pg.quit()