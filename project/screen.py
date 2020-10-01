

import pygame as pg
import sys


class Screen:


    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    bgcolour = black
    txtcolor = black

    #font
    pg.font.init()
    myfont = pg.font.SysFont("Arial Black", 20)

    # Set up pygame window
    xmax = 1344
    ymax = 756
    x = 725
    y_table = 350


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
        #self.keys = pg.key.get_pressed()

        xloc = self.x
        yloc = self.y_table


        self.scr.fill((0, 0, 0))

        self.draw_text_right("Infected", self.myfont, self.white, xloc + 300, yloc)

        for i in range(len(regions)):

            yloc += 30
            inf = regions[i].df.iat[-1,1]
            pop = regions[i].pops

            self.draw_text(regions[i].name[0:-4],self.myfont,self.white,xloc,yloc)
            self.draw_text_right(str(int(inf)), self.myfont, self.white, xloc+300, yloc)


            num = inf/pop*6
            print(num)
            if num<=1:
                self.scr.blit(regions[i].img1,regions[i].img1_rect)
            elif num<=2:
                self.scr.blit(regions[i].img2,regions[i].img2_rect)
            elif num<=3:
                self.scr.blit(regions[i].img3,regions[i].img3_rect)
            elif num<=4:
                self.scr.blit(regions[i].img4,regions[i].img4_rect)
            elif num<=5:
                self.scr.blit(regions[i].img5,regions[i].img5_rect)
            else:
                self.scr.blit(regions[i].img6,regions[i].img6_rect)

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


    def draw_text(self,text,font,color,x,y):
        textobj = font.render(text,1,color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        self.scr.blit(textobj,textrect)

    def draw_text_right(self,text,font,color,x,y):
        textobj = font.render(text,1,color)
        textrect = textobj.get_rect()
        textrect.topright = (x,y)
        self.scr.blit(textobj,textrect)


    def click_measure(self,measures):

        button_color = (255, 255, 255)
        button_size = (600, 25)
        offset = 10
        button_x = self.x
        button_y_diff = offset+button_size[1]


        button_0 = pg.Rect(button_x, offset + button_y_diff*0, button_size[0], button_size[1])
        button_1 = pg.Rect(button_x, offset + button_y_diff*1, button_size[0], button_size[1])
        button_2 = pg.Rect(button_x, offset + button_y_diff*2, button_size[0], button_size[1])
        button_3 = pg.Rect(button_x, offset + button_y_diff*3, button_size[0], button_size[1])
        button_4 = pg.Rect(button_x, offset + button_y_diff*4, button_size[0], button_size[1])
        button_5 = pg.Rect(button_x, offset + button_y_diff*5, button_size[0], button_size[1])
        button_6 = pg.Rect(button_x, offset + button_y_diff*6, button_size[0], button_size[1])
        button_7 = pg.Rect(button_x, offset + button_y_diff*7, button_size[0], button_size[1])
        button_8 = pg.Rect(button_x, offset + button_y_diff*8, button_size[0], button_size[1])


        click = False
        while True:
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


            self.draw_text("#0| Take no action", self.myfont,self.txtcolor,button_x, offset + button_y_diff*0)
            self.draw_text(measures[0].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 1)
            self.draw_text(measures[1].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 2)
            self.draw_text(measures[2].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 3)
            self.draw_text(measures[3].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 4)
            self.draw_text(measures[4].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 5)
            self.draw_text(measures[5].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 6)
            self.draw_text(measures[6].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 7)
            self.draw_text(measures[7].__str__(), self.myfont, self.txtcolor, button_x, offset + button_y_diff * 8)



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



