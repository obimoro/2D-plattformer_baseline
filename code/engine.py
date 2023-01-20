import pygame as pg

class System():
    def __inti__(self):
        pass
    
    def check(self, entity):
        return True

    def update(self, screen, entities, platforms):
        for entity in entities:
            if self.check(entity):
                self.updateEntity(screen, entity,entities, platforms)

    def updateEntity(self, screen, entity,entities, platforms):
        pass


class CameraSystem(System):
    def __init__(self):
        super().__init__()
    
    def check(self, entity):
       return entity.camera is not None

    def updateEntity(self, screen, entity, entities, platforms):

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pg.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(cameraRect)

        # update camera if tracking an entity
        if entity.camera.entityToTrack is not None:
            trackedEntity = entity.camera.entityToTrack
            entity.camera.worldX = trackedEntity.position.rect.x
            entity.camera.worldY = trackedEntity.position.rect.y

        # calculate offsets
        offsetX = cameraRect.x + cameraRect.w/2 - entity.camera.worldX
        offsetY = cameraRect.y + cameraRect.h/2 - entity.camera.worldY

        screen.fill((255,125,0))
        # render platforms
        for p in platforms:
            newPosRect = pg.Rect(p.x + offsetX, p.y + offsetY, p.w, p.h)
            pg.draw.rect(screen, (125,125,125), newPosRect)

        # render entities
        for e in entities:
            state = e.state
            animation = e.animations.animationList[state]
            animation.draw(screen, e.position.rect.x + offsetX, e.position.rect.y + offsetY, e.direction == 'left', False)

        # unset clipping rectangle
        screen.set_clip(None)



class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
    
    def setWorldPos(self,x,y):
        self.worldX = x
        self.worldY = y

    def trackEntity(self, e):
        self.entityToTrack = e



class Position():
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)

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

    def draw(self, screen, x, y, flipX, flipY):      
        screen.blit(pg.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x,y))


class Entity():
    def __init__(self):
        self.state = 'idle'
        self.type = 'nomal'
        self.position = None
        self.animations = Animtations()
        self.direction = 'right'
        self.camera = None