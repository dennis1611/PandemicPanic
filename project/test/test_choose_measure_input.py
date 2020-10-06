""""
Test file for measure choosing input
"""

import unittest
from project.models.initialization import initialise_measures
from project.views.measures_terminal import validate_measure_input


measures = initialise_measures()


class MyTestCase(unittest.TestCase):

    def test_int(self):
        self.assertTrue(validate_measure_input('0', measures))
        self.assertTrue(validate_measure_input('1', measures))
        self.assertTrue(validate_measure_input(str(len(measures)), measures))
        self.assertFalse(validate_measure_input(str(len(measures) + 1), measures))

    def test_float(self):
        self.assertFalse(validate_measure_input('0.0', measures))
        self.assertFalse(validate_measure_input('1.0', measures))
        self.assertFalse(validate_measure_input('1.1', measures))

    def test_negative(self):
        self.assertFalse(validate_measure_input('-1', measures))

    def test_letters(self):
        self.assertFalse(validate_measure_input('a', measures))
        self.assertFalse(validate_measure_input('1a', measures))

    def test_spaces(self):
        self.assertTrue(validate_measure_input('1 ', measures))
        self.assertFalse(validate_measure_input('1 1', measures))


if __name__ == '__main__':
    unittest.main()
