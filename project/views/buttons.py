import pygame as pg


class Button:
    """
    Class to handle buttons in order to not clutter the Screen class.
    """

    # possible colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)

    width = 0

    def __init__(self, x, y, width, height):
        """
        Determine location and create rectangle.
        """
        self.rect = pg.Rect(0, 0, width, height)
        self.rect.midtop = (x, y)


class ProvinceMaster(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.width = 1

    def return_color(self):
        """
        Next turn button should be white.
        """
        return self.blue

    def clicked(self, *args):

        all_on = True
        for i in range(8):
            if not args[0][i + 8 * args[1]].active:
                all_on = False

        for i in range(8):
            if all_on:
                args[0][i + 8 * args[1]].active = False
            else:
                args[0][i + 8 * args[1]].active = True


class MeasureMaster(Button):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.width = 1

    def return_color(self):
        """
        Next turn button should be white.
        """
        return self.white

    def clicked(self, *args):

        all_on = True
        for i in range(12):
            if not args[0][i * 8 + args[1]].active:
                all_on = False

        for i in range(12):
            if all_on:
                args[0][i * 8 + args[1]].active = False
            else:
                args[0][i * 8 + args[1]].active = True


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
        else:
            return self.red

    # TODO: args is unused, but program crashes without
    # pylint: disable=unused-argument
    def clicked(self, *args):
        """
        If button is clicked, active boolean should be changed.
        """
        if self.active:
            self.active = False
        elif not self.active:
            self.active = True


class TurnButton(Button):
    def return_color(self):
        """
        Next turn button should be white.
        """
        return self.white


class EndButton(Button):
    def return_color(self):
        """
        Next turn button should be white.
        """
        return self.white
