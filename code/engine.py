import pygame as pg
import utils

class System():
    def __inti__(self):
        pass
    
    def check(self, entity):
        return True

    def update(self, screen, world):
        for entity in world.entities:
            if self.check(entity):
                self.updateEntity(screen, entity, world)

    def updateEntity(self, screen, entity, world):
        pass


class CameraSystem(System):
    def __init__(self):
        super().__init__()
    
    def check(self, entity):
       return entity.camera is not None

    def updateEntity(self, screen, entity, world):

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pg.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(cameraRect)

        # update camera if tracking an entity
        if entity.camera.entityToTrack is not None:

            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY 

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.worldX = (currentX * 0.95) + (targetX * 0.05)
            entity.camera.worldY = (currentY * 0.95) + (targetY * 0.05)

        # calculate offsets
        offsetX = cameraRect.x + cameraRect.w/2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h/2 - (entity.camera.worldY  * entity.camera.zoomLevel)

        screen.fill((255,125,0))
        # render platforms
        for p in world.platforms:
            newPosRect = pg.Rect(
                (p.x * entity.camera.zoomLevel) + offsetX,
                (p.y * entity.camera.zoomLevel) + offsetY,
                p.w  * entity.camera.zoomLevel,
                p.h  * entity.camera.zoomLevel)
            pg.draw.rect(screen, (125,125,125), newPosRect)

        # render entities
        for e in world.entities:
            state = e.state
            animation = e.animations.animationList[state]
            animation.draw(screen,
                (e.position.rect.x * entity.camera.zoomLevel)  + offsetX,
                (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                e.direction == 'left',
                False,
                entity.camera.zoomLevel)

        # entity HUD
        # score
        if entity.score is not None:
            screen.blit(utils.coin5, (entity.camera.rect.x + 10, entity.camera.rect.y + 10))
            utils.drawText(screen, (255,255,255), str(entity.score.score), entity.camera.rect.x + 45, entity.camera.rect.y + 6)



        # lives
        if entity.battle is not None:
           for l in range(entity.battle.lives):
                screen.blit(utils.heart0, (entity.camera.rect.x + 280 + (l * 30), entity.camera.rect.y + 6))

        # unset clipping rectangle
        screen.set_clip(None)



class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1
    
    def setWorldPos(self,x,y):
        self.worldX = x
        self.worldY = y

    def trackEntity(self, e):
        self.entityToTrack = e




class Position():
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)

class Score():
    def __init__(self):
        self.score = 0

class Battle():
    def __init__(self):
        self.lives = 3

class Animtations():
    def __init__(self):
        self.animationList = {}

    def add(self, state, animation):
        self.animationList[state] = animation        

class Animation():
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 8

    def update(self):
        # increment the timer
        self.animationTimer += 1
        # if the timer gets too high...
        if self.animationTimer >= self.animationSpeed:
            # reset the timer
            self.animationTimer = 0
            # increment the current image
            self.imageIndex += 1
            # loop back to the first image in the list
            # once the index gets too high
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, screen, x, y, flipX, flipY, zoomLevel):   
        image = self.imageList[self.imageIndex]
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pg.transform.scale(pg.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (newWidth, newHeight)), (x,y))


class Entity():
    def __init__(self):
        self.state = 'idle'
        self.type = 'nomal'
        self.position = None
        self.animations = Animtations()
        self.direction = 'right'
        self.camera = None
        self.score = None
        self.battle = None