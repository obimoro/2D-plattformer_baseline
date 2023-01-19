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

