"""
File that contains all the Button (sub)classes for the visual window.
"""

import pygame as pg


class Button:
    """
    Class to handle buttons.
    """

    # possible colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)

    width = 0

    def __init__(self, x, y, width, height, color=white):
        """Determine location and create rectangle with color."""
        self.rect = pg.Rect(0, 0, width, height)
        self.rect.midtop = (x, y)
        self.color = color

    def return_color(self):
        """Returns color corresponding to the button."""
        return self.color


class MasterButton(Button):
    """
    Button that switches all measure buttons on/off.
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=self.white)
        self.width = 1

    @staticmethod
    def clicked(measure_buttons):
        """Switch all measure buttons on/off."""
        # check if all buttons for this measure are on
        all_on = True
        for i in measure_buttons:
            if not i.active:
                all_on = False
        # if all on: turn all off
        if all_on:
            for i in measure_buttons:
                i.active = False
        # if one or more are turned off: turn all on
        else:
            for i in measure_buttons:
                i.active = True


class RegionMasterButton(Button):
    """
    Button that switches all measure buttons in a region column on/off.
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=self.white)
        self.width = 1

    @staticmethod
    def clicked(measure_buttons, region_i, num_measures):
        """Switch all measure buttons in a region column on/off."""
        # check if all buttons for this region are on
        all_on = True
        for i in range(num_measures):
            if not measure_buttons[i + num_measures * region_i].active:
                all_on = False
        # if all on: turn all off
        if all_on:
            for i in range(num_measures):
                measure_buttons[i + num_measures * region_i].active = False
        # if one or more are turned off: turn all on
        else:
            for i in range(num_measures):
                measure_buttons[i + num_measures * region_i].active = True


class MeasureMasterButton(Button):
    """
    Button that switches all measure buttons in a measure row on/off.
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, color=self.white)
        self.width = 1
        self.x = x
        self.y = y

    @staticmethod
    def clicked(measure_buttons, measure_i, num_measures, num_regions):
        """Switch all measure buttons in a measure row on/off"""
        # check if all buttons for this measure are on
        all_on = True
        for i in range(num_regions):
            if not measure_buttons[i * num_measures + measure_i].active:
                all_on = False
        # if all on: turn all off
        if all_on:
            for i in range(num_regions):
                measure_buttons[i * num_measures + measure_i].active = False
        # if one or more are turned off: turn all on
        else:
            for i in range(num_regions):
                measure_buttons[i * num_measures + measure_i].active = True


class MeasureButton(Button):
    """
    Button for a single measure in a single region.
    """
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
        else:
            return self.red

    def clicked(self):
        """
        If button is clicked, active boolean should be changed.
        """
        if self.active:
            self.active = False
        elif not self.active:
            self.active = True
