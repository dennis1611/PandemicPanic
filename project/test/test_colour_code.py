import unittest
from project.models.region import Region


class MyTestCase(unittest.TestCase):

    def test_no_infections(self):
        """Test case for no infections"""
        infections = 0
        population = 1000
        region = Region("Name", population, 0, 0, "abbreviation", base_inf=infections)
        colour_number = region.return_colour_code()
        self.assertEqual(1, colour_number)

    def test_full_infections(self):
        """Test case for entire population infected"""
        infections = 1000
        population = 1000
        region = Region("Name", population, 0, 0, "abbreviation", base_inf=infections)
        colour_number = region.return_colour_code()
        self.assertEqual(6, colour_number)

    def test_code_black_colour(self):
        """Test case that roughly corresponds to code black"""
        infections = 10
        population = 1000
        region = Region("Name", population, 0, 0, "abbreviation", base_inf=infections)
        colour_number = region.return_colour_code()
        self.assertEqual(4, colour_number)

    def test_high_infections(self):
        """Test case for a high but realistic number of infections"""
        infections = 15
        population = 1000
        region = Region("Name", population, 0, 0, "abbreviation", base_inf=infections)
        colour_number = region.return_colour_code()
        self.assertEqual(5, colour_number)


if __name__ == '__main__':
    unittest.main()
