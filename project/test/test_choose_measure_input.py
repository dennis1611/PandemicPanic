""""
Test file for measure choosing input.
"""

import unittest

from project.models.initialization import initialise_measures
from project.views.measures_terminal import validate_measure_input


class MyTestCase(unittest.TestCase):

    measures = initialise_measures()

    def test_int(self):
        """Tests if integers are handled correctly."""
        self.assertTrue(validate_measure_input('0', self.measures))
        self.assertTrue(validate_measure_input('1', self.measures))
        self.assertTrue(validate_measure_input(str(len(self.measures)), self.measures))
        self.assertFalse(validate_measure_input(str(len(self.measures) + 1), self.measures))

    def test_float(self):
        """Tests if floats are handled correctly."""
        self.assertFalse(validate_measure_input('0.0', self.measures))
        self.assertFalse(validate_measure_input('1.0', self.measures))
        self.assertFalse(validate_measure_input('1.1', self.measures))

    def test_negative(self):
        """Tests negative numbers are handled correctly."""
        self.assertFalse(validate_measure_input('-1', self.measures))

    def test_letters(self):
        """Tests if letters/strings are handled correctly."""
        self.assertFalse(validate_measure_input('a', self.measures))
        self.assertFalse(validate_measure_input('1a', self.measures))

    def test_spaces(self):
        """Tests if spaces are handled correctly."""
        self.assertTrue(validate_measure_input('1 ', self.measures))
        self.assertFalse(validate_measure_input('1 1', self.measures))


if __name__ == '__main__':
    unittest.main()
