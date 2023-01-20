import pygame as pg
import engine

coin0 = pg.image.load('graphics/coin/coin_0.png')
coin1 = pg.image.load('graphics/coin/coin_1.png')
coin2 = pg.image.load('graphics/coin/coin_2.png')
coin3 = pg.image.load('graphics/coin/coin_3.png')
coin4 = pg.image.load('graphics/coin/coin_4.png')
coin5 = pg.image.load('graphics/coin/coin_5.png')

def makeCoin(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,23,23)
    entityAnimation = engine.Animation([coin0, coin1, coin2, coin3, coin4, coin5])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'collectable'
    return entity

enemy0 = pg.image.load('graphics/enemy/spike monster B.png')

def makeEnemy(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,50,26)
    entityAnimation = engine.Animation([enemy0])
    entity.animations.add('idle', entityAnimation)
    entity.type = 'dangerous'
    return entity


idle0 = pg.image.load('graphics/DinoSprites - doux/idle/idle_00.png')
idle1 = pg.image.load('graphics/DinoSprites - doux/idle/idle_01.png')
idle2 = pg.image.load('graphics/DinoSprites - doux/idle/idle_02.png')
idle3 = pg.image.load('graphics/DinoSprites - doux/idle/idle_03.png')

walking0 =  pg.image.load('graphics/DinoSprites - doux/walking/walking_1.png')
walking1 =  pg.image.load('graphics/DinoSprites - doux/walking/walking_2.png')
walking2 =  pg.image.load('graphics/DinoSprites - doux/walking/walking_3.png')
walking3 =  pg.image.load('graphics/DinoSprites - doux/walking/walking_4.png')
walking4 =  pg.image.load('graphics/DinoSprites - doux/walking/walking_5.png')
walking5 =  pg.image.load('graphics/DinoSprites - doux/walking/walking_6.png')

def makePlayer(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x,y,32,51)
    entityIdleAnimation = engine.Animation([idle0, idle1, idle2, idle3])
    entityWalkingAnimation = engine.Animation([walking0, walking1, walking2, walking3, walking4, walking5])
    entity.animations.add('idle', entityIdleAnimation)
    entity.animations.add('walking', entityWalkingAnimation)
    entity.type = 'player'
    return entity


def drawText(screen, font, color, text, x, y):
    text = font.render(text, False, color, None)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)