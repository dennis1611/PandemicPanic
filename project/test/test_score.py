import unittest
import pandas as pd

from project.models.measure import Measure
from project.models.score import Score
from project.models.region import Region


class MyTestCase(unittest.TestCase):
    def generate_test_case(self):
        # test region
        name = "TestRegion"
        inh = 1000000
        inf_f = 1.25
        ded_f = 0.75
        # following attributes are hardcoded in test, so they still work after balancing changes
        base_r = 3
        base_death_f = 0.02
        base_inf = 1000
        abbreviation = 'TEST'
        test_region = [Region(name, inh, inf_f, ded_f, abbreviation,
                             base_r=base_r, base_death_factor=base_death_f, base_inf=base_inf)]
        # test measure
        number = 1
        name = "test_measure"
        desc = "this measure does something"
        factor = 0.5
        test_measure = [Measure(number, name, desc, factor)]

        return test_region, test_measure

    def test_score_no_measures(self):
        test_region, test_measure = self.generate_test_case()
        test_score = Score(test_measure)
        for week in range(1, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
        test_score.reward_survivors(test_region, 3)
        self.assertAlmostEqual((1000000 - int(1000 * 0.015 + 1000 * 3.75/2 * 0.015) * 100), test_score.score)

    def test_score_with_measure(self):
        test_region, test_measure = self.generate_test_case()
        test_score = Score(test_measure)
        test_measure_dict = {test_region[0].name: [True]}
        test_region[0].update_infections(1)
        test_region[0].update_R(1, test_measure[0].factor)
        for week in range(2, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
            test_score.penalize_measure(test_region, test_measure_dict, week)
        self.assertAlmostEqual(-2 * 3 * 0.01 * 1000000 * 0.5, test_score.score)
        test_score.reward_survivors(test_region, 3)
        self.assertAlmostEqual(995700.0 - 30000, test_score.score)
