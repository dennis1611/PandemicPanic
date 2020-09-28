""""
Test file for measure choosing input
"""

import unittest
from project.initialization import initialise_measures


def validate_measure_input(user_input):
    """Returns a boolean whether the user's input to choose a measure is valid"""
    is_int = True
    number_chosen = -1
    try:
        number_chosen = int(user_input)
    except ValueError:
        is_int = False

    # if: the input was an int
    if is_int:
        # case 1 (valid): the input was an int corresponding to a measure
        if number_chosen in measure_numbers:
            return True
        # case 2 (valid): the input was 0
        elif number_chosen == 0:
            return True
        # case 3 (invalid): the input was an int out of bounds
        else:
            return False
    # else (invalid): the input was not an int
    else:
        return False


measures, measure_numbers = initialise_measures()


class MyTestCase(unittest.TestCase):

    def test_int(self):
        self.assertTrue(validate_measure_input('0'))
        self.assertTrue(validate_measure_input('1'))
        self.assertTrue(validate_measure_input(str(len(measures))))

    def test_float(self):
        self.assertFalse(validate_measure_input('0.0'))
        self.assertFalse(validate_measure_input('1.0'))
        self.assertFalse(validate_measure_input('1.1'))

    def test_negative_int(self):
        self.assertFalse(validate_measure_input('-1'))

    def test_letters(self):
        self.assertFalse(validate_measure_input('a'))
        self.assertFalse(validate_measure_input('1a'))

    def test_spaces(self):
        self.assertTrue(validate_measure_input('1 '))
        self.assertFalse(validate_measure_input('1 1'))


if __name__ == '__main__':
    unittest.main()
