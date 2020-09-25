

import pygame as pg


class Screen:


    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    bgcolour = black

    # Set up pygame window
    xmax = 1344
    ymax = 756


    def __init__(self):

        #pg.init()
        self.res = (self.xmax, self.ymax)
        self.scr = pg.display.set_mode(self.res)

        self.tlast = pg.time.get_ticks()*0.001


    def start_turn(self,regions):

        # Get time step
        self.t = pg.time.get_ticks() * 0.001
        self.dt = min(0.01, self.t - self.tlast)
        self.tlast = self.t

        # get key input
        self.keys = pg.key.get_pressed()

        self.scr.fill((0,0,255))

        for i in range(len(regions)):

            red = int(regions[i].df.iat[-1,1]/regions[i].inhabitants*255)
            if red>255: red=255

            self.scr.fill((red,0,0))

            break

        pg.time.wait(1000)
        pg.display.flip()



    def check_quit(self):
        # check for quit event (closing window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False

        # escape key check: also quit
        if self.keys[pg.K_ESCAPE]:
            return False

        # event pump, prevent freeze
        pg.event.pump()

        return True













