import unittest
import pandas as pd

from project.models.measure import Measure
from project.models.score import Score
from project.models.region import Region


class MyTestCase(unittest.TestCase):
    def generate_test_case(self):
        # test measure
        number = 1
        name = "test_measure"
        desc = "this measure does something"
        factor = 0.5
        test_measure = [Measure(number, name, desc, factor)]
        # test region
        name = "TestRegion"
        inh = 1000000
        inf_f = 1.25
        ded_f = 0.75
        # hardcode attributes to nullify balancing effects
        base_r = 3
        base_death_f = 0.02
        base_inf = 1000
        abbreviation = 'TEST'
        test_region = [Region(name, inh, inf_f, ded_f, abbreviation,
                             base_r=base_r, base_death_factor=base_death_f, base_inf=base_inf)]
        # test score
        test_score = Score(test_measure)
        # hardcode attributes to nullify balancing effects
        test_score.score = 0
        test_score.death_penalty = 100
        test_score.survivor_bonus = 1
        test_score.recover_bonus = 1
        test_score.effect_penalties = [1 - measure.factor for measure in test_measure]
        test_score.base_measure_penalty = 0.01
        test_score.regular_measure_modifier = 1
        test_score.strict_measure_modifier = 3
        test_score.limit = 0.001
        test_score.long_measure_modifier = 2
        test_score.patience = 10
        test_score.both_modifier  = 6
        test_score.display_zeros = 3
        return test_region, test_measure, test_score

    def test_reward_survivors(self):
        test_region, test_measure, test_score = self.generate_test_case()
        for week in range(1, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
        test_score.reward_survivors(test_region, 3)
        self.assertAlmostEqual((1000000 - int(1000 * 0.015 + 1000 * 3.75/2 * 0.015) * 100), test_score.score)

    def test_reward_recoveries(self):
        test_region, test_measure, test_score = self.generate_test_case()
        for week in range(1, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
        test_score.reward_recoveries(test_region, 3)
        total_inf = int(1000 + 1000 * 3.75/2)
        dead = int(0.015 * total_inf)
        recov = int(total_inf - dead)
        self.assertAlmostEqual(recov - 100 * dead, test_score.score)

    def test_regular_measure(self):
        test_region, test_measure, test_score = self.generate_test_case()

        # activate measure
        test_measure[0].active = True

        test_region[0].update_infections(1)
        test_region[0].update_R(1, test_measure[0].factor)
        for week in range(2, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
            test_score.penalize_measure(test_region, week, test_measure)
        self.assertAlmostEqual(-2 * 0.01 * 1000000 * 0.5, test_score.score)
        test_score.reward_survivors(test_region, 3)
        self.assertAlmostEqual(995700.0 - 10000, test_score.score)

    def test_strict_measure(self):
        test_region, test_measure, test_score = self.generate_test_case()
        test_score.limit = 0.1

        # activate measure
        test_measure[0].active = True

        test_region[0].update_infections(1)
        test_region[0].update_R(1, test_measure[0].factor)
        for week in range(2, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
            test_score.penalize_measure(test_region, week, test_measure)
        self.assertAlmostEqual(-2 * 3 * 0.01 * 1000000 * 0.5, test_score.score)
        test_score.reward_survivors(test_region, 3)
        self.assertAlmostEqual(995700.0 - 30000, test_score.score)

    def test_long_measure(self):
        test_region, test_measure, test_score = self.generate_test_case()
        test_score.patience = 0

        # activate measure
        test_measure[0].active = True

        test_region[0].update_infections(1)
        test_region[0].update_R(1, test_measure[0].factor)
        for week in range(2, 4):
            test_region[0].update_infections(week)
            test_region[0].update_R(week, 1)
            test_score.penalize_measure(test_region, week, test_measure)
        self.assertAlmostEqual(-2 * 2 * 0.01 * 1000000 * 0.5, test_score.score)
        test_score.reward_survivors(test_region, 3)
        self.assertAlmostEqual(995700.0 - 20000, test_score.score)

    def test_finalize(self):
        test_region, test_measure, test_score = self.generate_test_case()
        test_score.score = -69420.1337
        test_score.finalize_score()
        self.assertAlmostEqual(0, test_score.score)
        test_score.score = 69420.1337
        test_score.finalize_score()
        self.assertAlmostEqual(69000, test_score.score)


if __name__ == '__main__':
    unittest.main()
