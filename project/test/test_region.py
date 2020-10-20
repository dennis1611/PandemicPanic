"""
Test file for the Region class.
"""

import unittest
import pandas as pd
from project.models.region import Region
from project.models.initialization import initialise_regions


class MyTestCase(unittest.TestCase):

    regions = initialise_regions()

    def test_amount(self):
        """check whether all provinces are used."""
        amount = 12
        self.assertEqual(amount, len(self.regions))

    def test_csv_order(self):
        """Check whether the data is read in correctly by testing the first case."""
        name = "Groningen"
        inhabitants = 585866
        self.assertEqual((self.regions[0].name, self.regions[0].inhabitants), (name, inhabitants))
        self.assertAlmostEqual(self.regions[0].death_factor, 0.992*0.02)

    def test_calculations_no_measures(self):
        name = "TestRegion"
        inh = 1000000
        inf_f = 1.25
        ded_f = 0.75
        # following attributes are hardcoded in test, so they still work after balancing changes
        base_r = 3
        base_death_f = 0.02
        base_inf = 1000
        abbreviation = 'TEST'
        test_region = Region(name, inh, inf_f, ded_f, abbreviation,
                            base_r=base_r, base_death_factor=base_death_f, base_inf=base_inf)
        for week in range(1, 4):
            test_region.update_infections(week)
            test_region.update_R(week, 1)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 1000)
        # adjusted for new code black
        self.assertAlmostEqual(13621, test_region.df["New infections"][3])
        self.assertAlmostEqual(3 * 28, test_region.df["New deaths"][3])
        self.assertAlmostEqual(1847 - 2 * 28, test_region.df["New recoveries"][3])


    def test_maximum_inhabitants(self):
        name = "TestRegion"
        inh = 1000000
        inf_f = 1.25
        ded_f = 0
        # following attributes are hardcoded in test, so they still work after balancing changes
        base_r = 3
        base_death_f = 0.02
        base_inf = 900000
        abbreviation = 'TEST'
        test_region = Region(name, inh, inf_f, ded_f, abbreviation,
                             base_r=base_r, base_death_factor=base_death_f, base_inf=base_inf)
        for week in range(1, 5):
            test_region.update_infections(week)
            test_region.update_R(week, 1)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 1000)
        self.assertAlmostEqual(1000000, test_region.df["Currently infected"][1])
        self.assertAlmostEqual(900000, test_region.df["New recoveries"][2])

    def test_code_black(self):
        name = "TestRegion"
        inh = 1000000
        inf_f = 1
        ded_f = 1
        # following attributes are hardcoded in test, so they still work after balancing changes
        base_r = 3
        base_death_f = 0.02
        base_inf = 5000
        abbreviation = 'TEST'
        test_region = Region(name, inh, inf_f, ded_f, abbreviation,
                             base_r=base_r, base_death_factor=base_death_f, base_inf=base_inf)
        test_region.capacity = 0.01
        test_region.code_black_effect = 3
        for week in range(1, 10):
            test_region.update_infections(week)
            test_region.update_R(week, 1)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 1000)
        self.assertAlmostEqual(7500, test_region.df["New infections"][1])
        self.assertAlmostEqual(12500, test_region.df["Currently infected"][1])
        self.assertAlmostEqual(0.06 * 18750, test_region.df["New deaths"][4])


if __name__ == '__main__':
    unittest.main()
