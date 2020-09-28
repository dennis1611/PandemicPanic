"""
Test file for the Region class.
"""

import unittest
from project.region import Region
from project.initialization import initialise_measures, initialise_regions


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
        self.assertEqual((self.regions[0].name,self.regions[0].inhabitants),(name,inhabitants))
        self.assertAlmostEqual(self.regions[0].infectionfactor,1.125812437855936)
        self.assertAlmostEqual(self.regions[0].deathfactor,0.9918927528470189)


if __name__ == '__main__':
    unittest.main()
