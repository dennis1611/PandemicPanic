"""
Test file for the Region class.
"""

import unittest
import pandas as pd
from project.region import Region
from project.models.initialization import initialise_measures, initialise_regions


class MyTestCase(unittest.TestCase):

    regions = initialise_regions()

    def test_amount(self):
        """check whether all provinces are used."""
        amount = 12
        self.assertEqual(amount,len(self.regions))

    def test_csv_order(self):
        """Check whether the data is read in correctly by testing the first case."""
        name = "Groningen (PV)"
        inhabitants = 585866
        self.assertEqual((self.regions[0].name, self.regions[0].inhabitants), (name, inhabitants))
        self.assertAlmostEqual(self.regions[0].death_factor, 0.019837855)

    def test_calculations_no_measures(self):
        name = "TestRegion"
        inh = 1000000
        inf_f = 1.25
        ded_f = 0.75
        base_inf = 1000
        testregion = Region(name, inh, inf_f, ded_f, base_inf)
        for week in range(1, 4):
            testregion.update_infections(week)
            testregion.update_R(week, 1)
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 1000)
        print()
        print(testregion.df)
        self.assertAlmostEqual(13621, testregion.df["New infections"][3])
        self.assertAlmostEqual(1847, testregion.df["New recoveries"][3])
        self.assertAlmostEqual(28, testregion.df["New deaths"][3])


if __name__ == '__main__':
    unittest.main()
