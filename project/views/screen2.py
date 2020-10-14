import sys
import pygame as pg


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

    # Set screen dimensions and create the surface.
    scr = pg.display.set_mode((x_max, y_max))

    def __init__(self, num_regions, num_measures, regions_dict, unused):

        self.num_regions = num_regions
        self.num_measures = num_measures
        self.regions_dict = regions_dict

        # create instances
        self.map = Map()
        self.measure_table = MeasureTable(self.num_regions, self.num_measures)
        self.info_table = InfoTable(self.x_div, self.y_div)

        # TurnButton and EndButton setup and creation
        self.next_turn_button = TurnButton(25, 0, 50, 50)
        self.end_button = EndButton(800, 600, 100, 100)

    def start_turn(self, regions, week):
        # clear screen to black
        self.scr.fill((0, 0, 0))

        # write number of week on turn-button
        Screen.draw_text(f"Week: {week}", self.white, 200, 0, "top_right")

        self.map.start_turn(regions)
        self.measure_table.start_turn(regions)
        self.info_table.start_turn(regions)

        pg.display.flip()

    def end_turn(self, regions):
        self.click_button(False)

        return_dict = {}
        for j in range(self.num_regions):
            active_array = []
            for i in range(self.num_measures):
                active_array.append(self.measure_table.measure_buttons[self.num_measures * j + i].active)
            return_dict[regions[j].name] = active_array
        # print(return_dict)

        # enable this to return the measure dictionary per region
        return return_dict

    def end_game(self, score):
        while True:
            # clear screen to black
            self.scr.fill((0, 0, 0))
            # print ending message and score
            self.draw_text("The game has ended", self.white, 800, 400, "top_right")
            self.draw_text(f"Tour score is {score}", self.white, 800, 500, "top_right")
            # draw the end button
            pg.draw.rect(self.scr, self.end_button.return_color(), self.end_button.rect)
            self.click_button(True)
            pg.display.flip()
            pg.event.pump()

    @staticmethod
    def draw_text(text, color, x, y, loc):
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

    def click_button(self, ending):
        clean_rect = pg.Rect(700, 40, 1000, 280)

        click = False
        while True:

            # get mouse position
            mouse_x, mouse_y = pg.mouse.get_pos()

            # clean buttons with background color rectangle
            pg.draw.rect(self.scr, self.bg_colour, clean_rect)

            if not ending:
                # if next turn button is clicked return to main loop
                if self.next_turn_button.rect.collidepoint(mouse_x, mouse_y):
                    if click:
                        return
                # check if one of the measure buttons is clicked
                for i in range(len(self.measure_table.measure_buttons)):
                    if self.measure_table.measure_buttons[i].rect.collidepoint(mouse_x, mouse_y):
                        if click:
                            self.measure_table.measure_buttons[i].clicked()
                    # TODO: write comment (just copied this)
                    pg.draw.rect(self.scr, self.measure_table.measure_buttons[i].return_color(), self.measure_table.measure_buttons[i].rect)

            elif ending:
                # if the end game button is clicked
                if self.end_button.rect.collidepoint(mouse_x, mouse_y):
                    if click:
                        pg.quit()
                        sys.exit()

            # draw the next turn button
            pg.draw.rect(self.scr, self.next_turn_button.return_color(), self.next_turn_button.rect)

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


class Map:
    @staticmethod
    def start_turn(regions):
        for i in range(len(regions)):
            inf = regions[i].df.iat[-1, 1]
            pop = regions[i].inhabitants
            num = int(inf / pop * 6)
            if num > 5:
                num = 5
            Screen.scr.blit(regions[i].images[num].img, regions[i].images[num].img_rect)


class MeasureTable:
    measure_button_size = (25, 25)
    offset = 40
    button_y_diff = 10 + measure_button_size[1]
    x_loc = 750
    y_loc_abbr = 0

    def __init__(self, num_regions, num_measures):
        # Measure buttons creation
        self.measure_buttons = self.create_measure_buttons(num_regions, num_measures)

    def create_measure_buttons(self, num_regions, num_measures):
        # create button for each measure for each region
        measure_buttons = []
        for region_n in range(num_regions):
            for meas_n in range(num_measures):
                measure_buttons.append(
                    MeasureButton(self.x_loc + 50 * region_n, self.offset + self.button_y_diff * meas_n, 25, 25))
        return measure_buttons

    def start_turn(self, regions):
        # make local copy of x_loc
        x_loc_abbr = self.x_loc
        for region in regions:
            # write abbreviation
            Screen.draw_text(region.abbreviation, Screen.white, x_loc_abbr, self.y_loc_abbr, "mid")
            # go to next column
            x_loc_abbr += 50


class InfoTable:
    def __init__(self, x_div, y_div):
        self.x_loc = x_div
        self.y_loc = y_div

    def start_turn(self, regions):
        # make local copy of y_loc
        y_loc_table = self.y_loc

        # write "infected" at info table
        Screen.draw_text("Infected", Screen.white, self.x_loc + 300, y_loc_table, "top_right")

        for region in regions:
            # go to next row
            y_loc_table += 30

            # write region names at info table
            Screen.draw_text(region.name, Screen.white, self.x_loc, y_loc_table, "top_left")
            # write infections per region at info table
            Screen.draw_text(str(int(region.df.iat[-1, 1])), Screen.white, self.x_loc + 300, y_loc_table, "top_right")