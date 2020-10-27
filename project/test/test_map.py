import unittest
from project.views.screen import Map

maps = Map()

class MyTestCase(unittest.TestCase):

    def test_no_infections(self):
        infections = 0
        population = 1000
        colour_number = maps.calc_picture_number(infections, population)
        self.assertEqual(1, colour_number)

    def test_full_infections(self):
        infections = 1000
        population = 1000
        colour_number = maps.calc_picture_number(infections, population)
        self.assertEqual(6, colour_number)

    def test_code_black_colour(self):
        infections = 10
        population = 1000
        colour_number = maps.calc_picture_number(infections, population)
        self.assertEqual(4, colour_number)

    def test_high_infections(self):
        infections = 15
        population = 1000
        colour_number = maps.calc_picture_number(infections, population)
        self.assertEqual(5, colour_number)


if __name__ == '__main__':
    unittest.main()
