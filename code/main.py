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
import engine
import utils

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

#game states = playing // win // lose
game_state = 'playing'


# Player
# player attri
player_speed = 0
player_acceleration = 0.2
player_on_ground = False



# platforms
platforms = [
    pg.Rect(100, 300, 400, 50),
    pg.Rect(100, 250,  50, 50),
    pg.Rect(450, 250,  50, 50)
]

entities = []
entities.append(utils.makeCoin(100, 200))
entities.append(utils.makeCoin(200, 250))

enemy = utils.makeEnemy(150, 274)
enemy.camera = engine.Camera(420,10, 200,200)
enemy.camera.setWorldPos(150, 250)
entities.append(enemy)

player = utils.makePlayer(300, 0)
player.camera = engine.Camera(10,10, 400, 400)
player.camera.setWorldPos(300, 0)
player.camera.trackEntity(player)
player.score = engine.Score()
player.battle = engine.Battle()
entities.append(player)

cameraSystem = engine.CameraSystem()

# game loop
while running:

    # INPUT ---------------
    # check for quit
    for event in    pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if game_state == 'playing':
        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

        # player input 
        keys = pg.key.get_pressed()    
        # left
        if keys[pg.K_a]:
            new_player_x -= 3
            player.direction = 'left'
            player.state = 'walking'
        # right
        if keys[pg.K_d]:
            new_player_x += 3
            player.direction = 'right'
            player.state = 'walking'

        if not keys[pg.K_a] and not keys[pg.K_d] and player_on_ground:
            player.state = 'idle'


        # jump ( if on the ground)
        if keys[pg.K_SPACE] and player_on_ground:
            player_speed = -5

        if keys[pg.K_ESCAPE]:
            running = False

        # control zoom level of the player camera
        # zoom out
        if keys[pg.K_q]:
            player.camera.zoomLevel -= 0.01
            if player.camera.zoomLevel < 0.05:
                player.camera.zoomLevel = 0.05
        # zoom in
        if keys[pg.K_e]:
            player.camera.zoomLevel += 0.01


    # UPDATE -----

    if game_state == 'playing':
        # update animations
        for entity in entities:
            entity.animations.animationList[entity.state].update()

        # horizontal movement
        new_player_rect = pg.Rect(new_player_x, player.position.rect.y, player.position.rect.width ,player.position.rect.height)
        x_collision = False

        # check against every platform 
        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if x_collision == False:
            player.position.rect.x = new_player_x

        # vertical movment
        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pg.Rect(int(player.position.rect.x), int(new_player_y), player.position.rect.width ,player.position.rect.height)
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
                    player.position.rect.y = p[1] - player.position.rect.height
                    player_on_ground = True
                break

        if y_collision == False:
            player.position.rect.y = int(new_player_y)


        # see if any coins have been collected
        player_rect = pg.Rect(int(player.position.rect.x), int(player.position.rect.y), player.position.rect.width, player.position.rect.height)

        # collection system
        for entity in entities:
            if entity.type == 'collectable':
                if entity.position.rect.colliderect(player_rect):
                    entities.remove(entity)
                    player.score.score += 1
                    # change the game state
                    # if all coins are collected
                    if player.score.score >= 2:
                        game_state = 'win'
        
        # enemy system
        for entity in entities:
            if entity.type == 'dangerous':
                if entity.position.rect.colliderect(player_rect):
                    player.battle.lives -= 1
                    # reste player position
                    player.position.rect.x = 300
                    player.position.rect.y = 0
                    player_speed = 0    
                # change the game state 
                # if no lives remaining
                if player.battle.lives <= 0:
                    game_state = 'lose'
        

    # RENDER ------------

    # Background
    screen.fill(BLACK)

    cameraSystem.update(screen, entities, platforms)

    # present screen
    pg.display.flip()
 
    clock.tick(60)

# quit
pg.quit()