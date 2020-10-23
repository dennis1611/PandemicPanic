import sys
import os

import pygame as pg
from project.views.buttons import RegionMasterButton, \
    MeasureMasterButton, \
    MeasureButton, \
    TurnButton, \
    EndButton


class Screen:
    """
    Class to handle the visualization of the game.
    """

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    bg_colour = black
    txt_color = white

    # font
    pg.font.init()
    my_font = pg.font.SysFont("Arial Black", 20)

    # Set up pygame window
    x_max = 1344
    y_max = 756
    x_div = 725
    y_div = 360

    # Create window
    project_path = os.path.dirname(os.path.dirname(__file__))
    dir_path = project_path + '/source_data/provinces/'
    icon = pg.image.load(dir_path + "icon.png")
    pg.display.set_icon(icon)
    pg.display.set_caption('PandemicPanic')
    scr = pg.display.set_mode((x_max, y_max))

    def __init__(self, num_regions, num_measures, regions_dict, measures):

        self.num_regions = num_regions
        self.num_measures = num_measures
        self.regions_dict = regions_dict

        # create instances
        self.map = Map()
        self.measure_table = MeasureTable(self.num_regions, self.num_measures, measures)
        self.info_table = InfoTable(self.x_div, self.y_div)

        # TurnButton and EndButton setup and creation
        self.next_turn_button = TurnButton(75, 45, 120, 25)
        self.end_button = EndButton(800, 600, 100, 100)

    def start_turn(self, regions, week):
        """Resets/updates the screen at the start of each turn, and handles individual sections"""
        # clear screen to black
        self.scr.fill(self.bg_colour)

        # draw the next turn button
        pg.draw.rect(self.scr, self.next_turn_button.return_color(), self.next_turn_button.rect)
        self.draw_text("Next turn", self.black, 75, 42, "mid")

        # write number of week above turn-button
        Screen.draw_text(f"Week: {week}", self.white, 25, 10, "top_left")

        self.map.start_turn(regions)
        self.measure_table.start_turn(regions)
        self.info_table.start_turn(regions)

        pg.display.flip()

    def end_turn(self, regions):
        """Waits until end turn button is clicked, then returns relevant information"""
        self.click_button_game()

        return_dict = {}
        for j in range(self.num_regions):
            active_array = []
            for i in range(self.num_measures):
                active_array.append(
                    self.measure_table.measure_buttons[self.num_measures * j + i].active
                )
            return_dict[regions[j].name] = active_array
        # print(return_dict)

        # enable this to return the measure dictionary per region
        return return_dict

    def end_game(self, score, deaths):
        """Ends the game and gives a score"""
        while True:
            # clear screen to black
            self.scr.fill(self.bg_colour)
            # print ending message and score
            self.draw_text("The game has ended", self.white, 800, 300, "top_right")
            self.draw_text(f"Your death count is {deaths}", self.white, 800, 400, "top_right")
            self.draw_text(f"Your score is {score}", self.white, 800, 500, "top_right")
            # draw the end button
            pg.draw.rect(self.scr, self.end_button.return_color(), self.end_button.rect)
            self.click_button_ending()
            pg.display.flip()
            pg.event.pump()

    @staticmethod
    def draw_text(text, color, x, y, loc):
        """Helper function to draw text on the screen"""
        font = Screen.my_font
        text_obj = font.render(text, 1, color)
        text_rect = text_obj.get_rect()

        if loc == "top_left":
            text_rect.topleft = (x, y)
        elif loc == "top_right":
            text_rect.topright = (x, y)
        elif loc == "mid":
            text_rect.midtop = (x, y)

        Screen.scr.blit(text_obj, text_rect)

    # pylint: disable=too-many-branches
    def click_button_game(self):
        """Listener for all buttons during the game"""
        # rectangle for the measures table
        # Note: includes only the non-master buttons
        clean_rect = pg.Rect(725, 40, 1000, 280)

        click = False
        while True:

            # get mouse position
            mouse_x, mouse_y = pg.mouse.get_pos()

            # get keys
            keys = pg.key.get_pressed()

            # if next turn button is clicked return to main loop
            if self.next_turn_button.rect.collidepoint(mouse_x, mouse_y) and click:
                return

            # clean buttons with background color rectangle (measures table only)
            pg.draw.rect(self.scr, self.bg_colour, clean_rect)

            if keys[pg.K_SPACE]:
                # write full description of measures if SPACE is pressed
                self.measure_table.draw_descriptions(self.measure_table.measure_descriptions,
                                                     self.measure_table.measure_masters)
            else:
                # else draw normal measure buttons
                for button in self.measure_table.measure_buttons:
                    pg.draw.rect(Screen.scr, button.return_color(), button.rect, button.width)

            # listen to clicks for measure master buttons
            for measure_i, button in enumerate(self.measure_table.measure_masters):
                if button.rect.collidepoint(mouse_x, mouse_y) and click:
                    button.clicked(self.measure_table.measure_buttons, measure_i,
                                   self.num_measures, self.num_regions)
            # listen to clicks for region master buttons
            for region_i, button in enumerate(self.measure_table.region_masters):
                if button.rect.collidepoint(mouse_x, mouse_y) and click:
                    button.clicked(self.measure_table.measure_buttons, region_i,
                                   self.num_measures)
            # listen to clicks for normal measure buttons
            for button in self.measure_table.measure_buttons:
                if button.rect.collidepoint(mouse_x, mouse_y) and click:
                    button.clicked()

            # flip the display and check events
            pg.display.flip()

            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            # event pump, prevent freeze
            pg.event.pump()

    def click_button_ending(self):
        """Listener for all buttons in the ending"""
        click = False
        while True:
            # get mouse position
            mouse_x, mouse_y = pg.mouse.get_pos()

            # if the end game button is clicked
            if self.end_button.rect.collidepoint(mouse_x, mouse_y) and click:
                pg.quit()
                sys.exit()

            # flip the display and check events
            pg.display.flip()

            click = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            # event pump, prevent freeze
            pg.event.pump()


class Map:
    def __init__(self):
        # Overlay setup
        project_path = os.path.dirname(os.path.dirname(__file__))
        dir_path = project_path + '/source_data/provinces/'
        self.overlay = pg.image.load(dir_path + "overlay.png")
        self.overlay_rect = self.overlay.get_rect()
        self.overlay_rect.topleft = (-30, 30)

    def start_turn(self, regions):
        """Updates the map at the start of each turn"""
        # show each region in the correct colour

        # TODO: This function is TEMPORARY, only until the right configuration is found -- Willem
        def tempfunc(inf, pop):
            percentage = (inf / pop) * 100
            return (percentage * (1 * percentage + 10)) ** 0.5 // 1

        for region in regions:
            inf = region.df.iat[-1, 1]
            pop = region.inhabitants
            num = int(tempfunc(inf, pop)) + 1
            if num > 6:
                num = 6
            Screen.scr.blit(region.images[num].img, region.images[num].img_rect)

        # show overlay on screen
        Screen.scr.blit(self.overlay, self.overlay_rect)

        # Second loop is needed for order of displaying
        for region in regions:
            # show warning sign for region if code black is active
            if region.code_black_active:
                Screen.scr.blit(region.images[0].img, region.images[0].img_rect)


class MeasureTable:
    button_size_x, button_size_y = 25, 25
    master_size_x, master_size_y = 25, 25
    offset = 40
    button_y_diff = 10 + button_size_y
    x_loc = 700
    y_loc_abbr = 0

    @staticmethod
    def draw_descriptions(descriptions, loc):
        """Draws the measure descriptions on the screen (excl. number)"""
        # Note: loc is a list of MeasureMasterButtons
        for count, description in enumerate(descriptions):
            Screen.draw_text(description[1:], Screen.white,
                             loc[count].x + 30, loc[count].y - 4, "top_left")

    def __init__(self, num_regions, num_measures, measures):
        # Measure buttons creation
        measure_buttons = []
        measure_masters = []
        region_masters = []
        for region_n in range(num_regions + 1):
            for meas_n in range(num_measures + 1):
                # master buttons for measures
                if region_n == 0 and not meas_n == 0:
                    measure_masters.append(
                        MeasureMasterButton(self.x_loc + 50 * region_n,
                                            self.offset + self.button_y_diff * (meas_n - 1),
                                            self.master_size_x, self.master_size_y
                                            )
                    )
                # master buttons for regions
                elif meas_n == 0 and not region_n == 0:
                    region_masters.append(
                        RegionMasterButton(self.x_loc + 50 * region_n,
                                           self.offset + self.button_y_diff * (meas_n - 1),
                                           self.master_size_x + 10, self.master_size_y
                                           )
                    )
                # normal measure buttons
                elif not (region_n == 0 and meas_n == 0):
                    measure_buttons.append(
                        MeasureButton(self.x_loc + 50 * region_n,
                                      self.offset + self.button_y_diff * (meas_n - 1),
                                      self.button_size_x, self.button_size_y
                                      )
                    )

        self.measure_buttons = measure_buttons
        self.measure_masters = measure_masters
        self.region_masters = region_masters

        measure_descriptions = []
        for meas in measures:
            measure_descriptions.append(repr(meas))
        self.measure_descriptions = measure_descriptions

    def start_turn(self, regions):
        """Updates the measure table at the start of each turn
        Note: non-master buttons need to be drawn in click_button_game"""
        # draw region master buttons in the measures table
        for button in self.region_masters:
            pg.draw.rect(Screen.scr, button.return_color(), button.rect, button.width)
        # write the abbreviations in the buttons
        x_loc_abbr = self.x_loc + 50  # local copy of x_loc
        for region in regions:
            # write abbreviation
            Screen.draw_text(region.abbreviation, Screen.white, x_loc_abbr, self.y_loc_abbr, "mid")
            # go to next column
            x_loc_abbr += 50

        # draw measure master buttons in the measures table
        for button in self.measure_masters:
            pg.draw.rect(Screen.scr, button.return_color(), button.rect, button.width)
        # write measure number in measure master button
        for i, description in enumerate(self.measure_descriptions):
            Screen.draw_text(description[0], Screen.white,
                             self.measure_masters[i].x - 6,
                             self.measure_masters[i].y - 4,
                             "top_left")


class InfoTable:
    def __init__(self, x_div, y_div):
        self.x_loc = x_div - 35
        self.y_loc = y_div

    def start_turn(self, regions):
        """Updates the info table at the start of each turn"""
        # make local copy of y_loc
        y_loc_table = self.y_loc

        # write column names at info table
        Screen.draw_text("Cases (C)", Screen.white, self.x_loc + 250, y_loc_table, "top_right")
        Screen.draw_text("C/100k", Screen.white, self.x_loc + 350, y_loc_table, "top_right")
        Screen.draw_text("Deaths", Screen.white, self.x_loc + 450, y_loc_table, "top_right")
        Screen.draw_text("R-value", Screen.white, self.x_loc + 550, y_loc_table, "top_right")
        Screen.draw_text("Recvrd", Screen.white, self.x_loc + 650, y_loc_table, "top_right")

        for region in regions:
            # go to next row
            y_loc_table += 30

            # write region names at info table
            Screen.draw_text(region.name, Screen.white, self.x_loc, y_loc_table, "top_left")
            # write data columns at info table
            cases = str(int(region.df.iat[-1, 1]))
            Screen.draw_text(cases, Screen.white,
                             self.x_loc + 250, y_loc_table, "top_right")
            cases_100k = str(int(region.df.iat[-1, 1] / region.inhabitants * 100000))
            Screen.draw_text(cases_100k, Screen.white,
                             self.x_loc + 350, y_loc_table, "top_right")
            deaths = str(int(region.df.iat[-1, 3]))
            Screen.draw_text(deaths, Screen.white,
                             self.x_loc + 450, y_loc_table, "top_right")

            r_val = str(round(region.df.iat[-2, 6], 2))
            diff = 4 - len(r_val)
            if diff != 0:
                for _ in range(diff):
                    r_val = r_val + "0"
            Screen.draw_text(r_val, Screen.white,
                             self.x_loc + 550, y_loc_table, "top_right")
            recoveries = str(int(region.df.iat[-1, 5]))
            Screen.draw_text(recoveries, Screen.white,
                             self.x_loc + 650, y_loc_table, "top_right")
