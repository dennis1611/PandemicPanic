

import pygame as pg
import sys


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


        self.scr.fill((0, 0, 255))

        for i in range(len(regions)):

            red = int(regions[i].df.iat[-1,1]/regions[i].inhabitants*255)
            if red>255: red=255

            self.scr.fill((red,0,0))

            break


        pg.display.flip()



    def check_quit(self):
        # check for quit event (closing window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # escape key check: also quit
        #if self.keys[pg.K_ESCAPE]:
            #return False

        # event pump, prevent freeze
        pg.event.pump()




    def click_measure(self):

        button_color = (255, 255, 255)
        button_0 = pg.Rect(700, 25, 200, 20)
        button_1 = pg.Rect(700, 50, 200, 20)
        button_2 = pg.Rect(700, 75, 200, 20)
        button_3 = pg.Rect(700, 100, 200, 20)
        button_4 = pg.Rect(700, 125, 200, 20)
        button_5 = pg.Rect(700, 150, 200, 20)
        button_6 = pg.Rect(700, 175, 200, 20)
        button_7 = pg.Rect(700, 200, 200, 20)
        button_8 = pg.Rect(700, 225, 200, 20)

        running = True
        click = False
        while running:
            #self.keys = pg.key.get_pressed()
            mx,my = pg.mouse.get_pos()

            if button_0.collidepoint((mx,my)):
                if click:
                    return 0
            if button_1.collidepoint((mx,my)):
                if click:
                    return 1
            if button_2.collidepoint((mx,my)):
                if click:
                    return 2
            if button_3.collidepoint((mx,my)):
                if click:
                    return 3
            if button_4.collidepoint((mx,my)):
                if click:
                    return 4
            if button_5.collidepoint((mx,my)):
                if click:
                    return 5
            if button_6.collidepoint((mx,my)):
                if click:
                    return 6
            if button_7.collidepoint((mx,my)):
                if click:
                    return 7
            if button_8.collidepoint((mx,my)):
                if click:
                    return 8

            pg.draw.rect(self.scr, button_color, button_0)
            pg.draw.rect(self.scr, button_color, button_1)
            pg.draw.rect(self.scr, button_color, button_2)
            pg.draw.rect(self.scr, button_color, button_3)
            pg.draw.rect(self.scr, button_color, button_4)
            pg.draw.rect(self.scr, button_color, button_5)
            pg.draw.rect(self.scr, button_color, button_6)
            pg.draw.rect(self.scr, button_color, button_7)
            pg.draw.rect(self.scr, button_color, button_8)
            pg.display.flip()



            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_0:
                        return 0
                    if event.key == pg.K_1:
                        return 1
                    if event.key == pg.K_2:
                        return 2
                    if event.key == pg.K_3:
                        return 3
                    if event.key == pg.K_4:
                        return 4
                    if event.key == pg.K_5:
                        return 5
                    if event.key == pg.K_6:
                        return 6
                    if event.key == pg.K_7:
                        return 7
                    if event.key == pg.K_8:
                        return 8

            # event pump, prevent freeze
            pg.event.pump()



