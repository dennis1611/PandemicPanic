

import pygame as pg
import sys


class Button:

    red = (255,0,0)
    green = (0,255,0)


    def __init__(self,x,y,width,height,measure_value):

        self.rect = pg.Rect(0,0,width,height)
        self.rect.midtop = (x,y)
        self.active = False
        self.measure_value = measure_value


    def return_color(self):
        if self.active:
            return self.green
        else:
            return self.red


    def clicked(self):
        if self.active:
            self.active = False
        else:
            self.active = True



class Screen:

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    bgcolour = black
    txtcolor = white

    #font
    pg.font.init()
    myfont = pg.font.SysFont("Arial Black", 20)

    # Set up pygame window
    xmax = 1344
    ymax = 756
    x = 725
    y_table = 360


    def __init__(self):

        #pg.init()
        self.res = (self.xmax, self.ymax)
        self.scr = pg.display.set_mode(self.res)

        self.tlast = pg.time.get_ticks()*0.001


        measure_button_size = (25, 25)
        offset = 40
        button_y_diff = 10+measure_button_size[1]
        x_loc = 750


        self.measure_buttons = []
        for j in range(12):

            for i in range(8):
                self.measure_buttons.append(Button(x_loc+50*j,offset + button_y_diff*i, 25, 25,i+1))

        self.next_turn_button = Button(25,0, 50, 50,0)


    def start_turn(self,regions):

        # Get time step
        self.t = pg.time.get_ticks() * 0.001
        self.dt = min(0.01, self.t - self.tlast)
        self.tlast = self.t

        xloc_table = self.x
        yloc_table = self.y_table

        xloc_abbr = 750
        yloc_abbr = 0

        self.scr.fill((0, 0, 0))

        self.draw_text_right("Infected", self.myfont, self.white, xloc_table + 300, yloc_table)

        for i in range(len(regions)):

            yloc_table += 30

            inf = regions[i].df.iat[-1,1]
            pop = regions[i].inhabitants

            self.draw_text(regions[i].name,self.myfont,self.white,xloc_table,yloc_table)
            self.draw_text_mid(regions[i].abbreviation, self.myfont, self.white, xloc_abbr, yloc_abbr)
            self.draw_text_right(str(int(inf)), self.myfont, self.white, xloc_table+300, yloc_table)

            num = int(inf/pop*6)
            if num>5: num = 5
            self.scr.blit(regions[i].images[num].img, regions[i].images[num].img_rect)

            xloc_abbr += 50

        pg.display.flip()


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


    def draw_text_mid(self,text,font,color,x,y):
        textobj = font.render(text,1,color)
        textrect = textobj.get_rect()
        textrect.midtop = (x,y)
        self.scr.blit(textobj,textrect)


    def click_measure(self,measures,regions):


        clean_rect = pg.Rect(700,40,1000,280)

        click = False
        while True:

            mx,my = pg.mouse.get_pos()


            pg.draw.rect(self.scr,self.bgcolour,clean_rect)


            for i in range(len(self.measure_buttons)):
                if self.measure_buttons[i].rect.collidepoint((mx,my)):
                    if click:
                        self.measure_buttons[i].clicked()

                pg.draw.rect(self.scr, self.measure_buttons[i].return_color(), self.measure_buttons[i].rect)


            if self.next_turn_button.rect.collidepoint((mx,my)):
                if click:

                    return_dict = {}

                    for j in range(12):

                        active_array = []

                        for i in range(8):
                            active_array.append(self.measure_buttons[8*j+i].active)

                        return_dict[regions[j].name] = active_array


                    print(return_dict)

                    #return this to get no errors
                    return self.next_turn_button.measure_value

                    #enable this to return the measure dictionary per region
                    #return return_dict


            pg.draw.rect(self.scr, self.next_turn_button.return_color(), self.next_turn_button.rect)



            offset = 40
            button_y_diff = 35
            x_loc = 710

            self.draw_text(measures[0].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 0-3)
            self.draw_text(measures[1].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 1-3)
            self.draw_text(measures[2].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 2-3)
            self.draw_text(measures[3].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 3-3)
            self.draw_text(measures[4].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 4-3)
            self.draw_text(measures[5].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 5-3)
            self.draw_text(measures[6].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 6-3)
            self.draw_text(measures[7].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 7-3)
            #self.draw_text(" End turn", self.myfont, self.txtcolor, self.x, offset + button_y_diff * 8 - 3)


            pg.display.flip()

            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            # event pump, prevent freeze
            pg.event.pump()
