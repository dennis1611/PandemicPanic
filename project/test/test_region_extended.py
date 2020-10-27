"""
Test file for the RegionExtended/RegionImg class.
"""

import unittest

from project.models.region import RegionImg
from project.models.initialization import initialise_regions


class MyTestCase(unittest.TestCase):

    regions = initialise_regions(visual=True)
    groningen = regions[0]

    def test_images(self):
        """Tests if the images for a region are created."""
        image = self.groningen.images[0]
        self.assertTrue(isinstance(image, RegionImg))

    def test_calculations_statuses(self):
        """
        Tests if the calculations work as expected,
        and if the Measure attributes are updated correctly.
        """
        # set the factor for all measures to 0.9
        for measure in self.groningen.region_measures:
            measure.factor = 0.9
        # create a list of current measure statuses
        measure_statuses = []
        for _ in range(len(self.groningen.region_measures)):
            measure_statuses.append(False)
        measure_statuses[0] = True
        measure_statuses[1] = True
        # get the total factor and update region measure statuses
        effect = self.groningen.calculate_measures_factor(measure_statuses)
        self.assertEqual(0.81, effect)
        self.assertTrue(self.groningen.region_measures[0].active)
        self.assertTrue(self.groningen.region_measures[1].active)
        self.assertFalse(self.groningen.region_measures[2].active)
        # also check if other regions are not linked to the same measures list
        self.assertFalse(self.regions[1].region_measures[0].active)
