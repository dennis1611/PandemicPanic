import sys
import pygame as pg
import os


class Button:
    """
    Class to handle buttons in order to not clutter the Screen class.
    """

    # possible colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)

    def __init__(self, x, y, width, height):
        """
        Determine location and create rectangle.
        """
        self.rect = pg.Rect(0, 0, width, height)
        self.rect.midtop = (x, y)


class TurnButton(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def return_color(self):
        """
        Next turn button should be white.
        """
        return self.white


class MeasureButton(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.active = False

    def return_color(self):
        """
        Active buttons should be green, inactive red.
        This function return the correct color.
        """
        if self.active:
            return self.green
        elif not self.active:
            return self.red

    def clicked(self):
        """
        If button is clicked, active boolean should be changed.
        """
        if self.active:
            self.active = False
        elif not self.active:
            self.active = True


class EndButton(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def return_color(self):
        """
        Next turn button should be white.
        """
        return self.white


class Screen:
    """
    Class to handle the visualization of the game.
    """

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    bgcolour = black
    txtcolor = white

    # font
    pg.font.init()
    myfont = pg.font.SysFont("Arial Black", 20)

    # Set up pygame window
    xmax = 1344
    ymax = 756
    x = 725
    y_table = 360

    def __init__(self, num_regions, num_measures, regions_dict, regions):

        # Set screen dimensions and create the surface.
        self.scr = pg.display.set_mode((self.xmax, self.ymax))

        self.num_regions = num_regions
        self.num_measures = num_measures
        self.regions_dict = regions_dict

        # create instances
        self.map = Map()
        self.measure_table = MeasureTable()
        self.info_table = InfoTable()

        # Measure buttons creation
        self.measure_buttons = self.measure_table.return_measure_buttons(regions, num_measures)

        # Next Turn button and end button setup and creation
        self.next_turn_button = TurnButton(25, 0, 50, 50)
        self.end_button = EndButton(800, 600, 100, 100)

        # Overlay setup
        project_path = os.path.dirname(os.path.dirname(__file__))
        dir_path = project_path + '/source_data/provinces/'
        self.overlay = pg.image.load(dir_path + "overlay.png")
        self.overlay_rect = self.overlay.get_rect()
        self.overlay_rect.topleft = (-30, 30)

    def start_turn(self, regions, week):

        # set location for info table
        xloc_table = self.x
        yloc_table = self.y_table

        # set location for abbreviations in measures table
        xloc_abbr = 750
        yloc_abbr = 0

        # clear screen to black
        self.scr.fill(self.bgcolour)

        # write "infected" at info table
        self.draw_text("Infected", self.myfont, self.white, xloc_table + 300, yloc_table, "topright")

        # write number of week on turn-button
        self.draw_text(f"Week: {week}", self.myfont, self.white, 200, 0, "topright")

        for i in range(self.num_regions):

            # go to next row
            yloc_table += 30

            inf = regions[i].df.iat[-1, 1]
            pop = regions[i].inhabitants

            self.draw_text(regions[i].name, self.myfont, self.white, xloc_table, yloc_table, "topleft")
            self.draw_text(regions[i].abbreviation, self.myfont, self.white, xloc_abbr, yloc_abbr, "mid")
            self.draw_text(str(int(inf)), self.myfont, self.white, xloc_table+300, yloc_table, "topright")

            num = int(inf/pop*6)+1
            if num > 6:
                num = 6
            self.scr.blit(regions[i].images[num].img, regions[i].images[num].img_rect)

            xloc_abbr += 50

        self.scr.blit(self.overlay,self.overlay_rect)

        # If code_black flag is enabled, draw emergency signs
        for r in regions:

            if True: #r.code_black
                self.scr.blit(r.images[0].img, r.images[0].img_rect)



        pg.display.flip()

    def draw_text(self, text, font, color, x, y, loc):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()

        if loc=="topleft":
            textrect.topleft = (x, y)
        elif loc=="topright":
            textrect.topright = (x, y)
        elif loc=="mid":
            textrect.midtop = (x, y)

        self.scr.blit(textobj, textrect)

    def click_button(self, ending):

        clean_rect = pg.Rect(700, 40, 1000, 280)

        click = False
        while True:

            # get mouse position
            mx, my = pg.mouse.get_pos()

            # clean buttons with background color rectangle
            pg.draw.rect(self.scr, self.bgcolour, clean_rect)

            # if clicked swap activation status, then draw new button
            if not ending:
                for i in range(len(self.measure_buttons)):
                    if self.measure_buttons[i].rect.collidepoint(mx, my):
                        if click:
                            self.measure_buttons[i].clicked()

                    pg.draw.rect(self.scr, self.measure_buttons[i].return_color(), self.measure_buttons[i].rect)

                # if next turn button is clicked return to main loop
                if self.next_turn_button.rect.collidepoint(mx, my):
                    if click:
                        return

            # if end game button is clicked, quit game
            if ending:
                if self.end_button.rect.collidepoint(mx, my):
                    if click:
                        pg.quit()
                        sys.exit()

            # draw the next turn button
            pg.draw.rect(self.scr, self.next_turn_button.return_color(), self.next_turn_button.rect)

            # to be fixed, this draws the measure text, however, obviously it looks ugly now.
            # offset = 40
            # button_y_diff = 35
            # x_loc = 710


            # self.draw_text(measures[0].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 0-3, "topleft")
            # self.draw_text(measures[1].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 1-3, "topleft")
            # self.draw_text(measures[2].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 2-3, "topleft")
            # self.draw_text(measures[3].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 3-3, "topleft")
            # self.draw_text(measures[4].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 4-3, "topleft")
            # self.draw_text(measures[5].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 5-3, "topleft")
            # self.draw_text(measures[6].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 6-3, "topleft")
            # self.draw_text(measures[7].__str__(), self.myfont, self.txtcolor, x_loc, offset + button_y_diff * 7-3, "topleft")

            # flip the display and check events
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

    def end_turn(self, regions):
        self.click_button(False)

        return_dict = {}
        for j in range(self.num_regions):
            active_array = []
            for i in range(self.num_measures):
                active_array.append(self.measure_buttons[self.num_measures * j + i].active)
            return_dict[regions[j].name] = active_array
        # print(return_dict)

        # enable this to return the measure dictionary per region
        return return_dict

    def end_game(self, score):
        while True:
            # clear screen to black
            self.scr.fill((0, 0, 0))
            # print ending message and score
            self.draw_text("The game has ended", self.myfont, self.white, 800, 400, "topright")
            self.draw_text(f"Tour score is {score}", self.myfont, self.white, 800, 500, "topright")
            # draw the end button
            pg.draw.rect(self.scr, self.end_button.return_color(), self.end_button.rect)
            self.click_button(True)
            pg.display.flip()
            pg.event.pump()






class Map:
    def ___init__(self):
        pass


class MeasureTable:
    measure_button_size = (25, 25)
    offset = 40
    button_y_diff = 10 + measure_button_size[1]
    x_loc = 750

    def __init__(self):
        pass

    def return_measure_buttons(self, regions, num_measures):
        # create button for each measure for each region
        measure_buttons = []
        for region_n in range(len(regions)):
            for meas_n in range(num_measures):
                measure_buttons.append(
                    MeasureButton(self.x_loc + 50 * region_n, self.offset + self.button_y_diff * meas_n, 25, 25))
        return measure_buttons


class InfoTable:
    def __init__(self):
        pass
