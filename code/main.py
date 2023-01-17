import pygame as pg
import sys

class Plattformer():
    def __init__(self):
        # initiliaze pygame
        pg.init

        # define window using pygame
        self.window = pg.display.set_mode((800, 600))
        pg.display.set_caption("2D Plattformer Testbed")

        # timing
        self.clock = pg.time.Clock()

    def check_event(self):
        for event in pg.event.get():
            # Check if program is closed or escape is pressed, then exit the application gracefully
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def render(self):
        # fill background with color (orange)
        self.window.fill((255,128,0))

        # update content of the display surface on the screen
        # by flipping the back buffer to the front
        pg.display.flip()

    def run(self):
        # application loop
        while True:
            self.check_event()
            self.render()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Plattformer()
    game.run()