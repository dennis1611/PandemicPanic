""""
Test file for the adjacent regions effect
"""

import unittest
from project.models.region import Region
from project.models.adjacency import adjust_adjacent_regions


class MyTestCase(unittest.TestCase):

    def test_adjacency_general(self):
        """General test for adjacency"""
        # create test region instances with infection factors of 1 and death factor of 0
        test_region_1 = Region("TestRegion1", 100000, 1, 0, "T1",
                               base_r=1, base_death_factor=0, base_inf=2000)
        test_region_2 = Region("TestRegion2", 100000, 1, 0, "T2",
                               base_r=1, base_death_factor=0, base_inf=1000)
        # create borders list
        borders = [("TestRegion1", "TestRegion2")]

        # check begin situation (week 0)
        self.assertEqual(2000, test_region_1.df["New infections"][0])
        self.assertEqual(1000, test_region_2.df["New infections"][0])
        self.assertEqual(2000, test_region_1.df["Currently infected"][0])
        self.assertEqual(1000, test_region_2.df["Currently infected"][0])

        # calculate new infections for week 1
        test_region_1.update_infections(1)
        test_region_2.update_infections(1)
        # check infections week 1
        self.assertEqual(1000, test_region_1.df["New infections"][1])
        self.assertEqual(500, test_region_2.df["New infections"][1])
        self.assertEqual(3000, test_region_1.df["Currently infected"][1])
        self.assertEqual(1500, test_region_2.df["Currently infected"][1])

        # adjust new infections and currently infected based on adjacency
        adjust_adjacent_regions(borders, [test_region_1, test_region_2], 1, impact=20)
        # check if new infections are updated correctly
        updated_new_inf_1 = test_region_1.df["New infections"][1]
        updated_new_inf_2 = test_region_2.df["New infections"][1]
        self.assertEqual(975, updated_new_inf_1)
        self.assertEqual(525, updated_new_inf_2)
        # also check if total infections has been updated
        updated_current_infected_1 = test_region_1.df["Currently infected"][1]
        updated_current_infected_2 = test_region_2.df["Currently infected"][1]
        self.assertEqual(2975, updated_current_infected_1)
        self.assertEqual(1525, updated_current_infected_2)

    def test_equal_new_infections(self):
        """Tests if case new_inf_1 == new_inf_2 is handled correctly"""
        # Note: zero new infections in both regions is included in this test
        # region1 and region2 have equal new infections and come first
        # then come region2 and region3, but region 3 has more new infections

        # create test region instances with infection factors of 1 and death factor of 0
        test_region_1 = Region("TestRegion1", 100000, 1, 0, "T1",
                               base_r=1, base_death_factor=0, base_inf=1000)
        test_region_2 = Region("TestRegion2", 100000, 1, 0, "T2",
                               base_r=1, base_death_factor=0, base_inf=1000)
        test_region_3 = Region("TestRegion3", 100000, 1, 0, "T3",
                               base_r=1, base_death_factor=0, base_inf=2000)
        # create borders list
        borders = [("TestRegion1", "TestRegion2"), ("TestRegion3", "TestRegion2")]
        # adjust new infections and currently infected based on adjacency
        adjust_adjacent_regions(borders, [test_region_1, test_region_2, test_region_3], 0, impact=20)

        # check if new infections are adjusted correctly
        updated_new_inf_1 = test_region_1.df["New infections"][0]
        updated_new_inf_2 = test_region_2.df["New infections"][0]
        updated_new_inf_3 = test_region_3.df["New infections"][0]
        self.assertEqual(1000, updated_new_inf_1)
        self.assertEqual(1050, updated_new_inf_2)
        self.assertEqual(1950, updated_new_inf_3)

    def test_limit_exchange(self):
        """Tests if the limit on the exchange is handled correctly"""
        # create test region instances with infection factors of 1 and death factor of 0
        inh1 = 100000
        test_region_1 = Region("TestRegion1", inh1, 1, 0, "T1",
                               base_r=1, base_death_factor=0, base_inf=inh1-50)
        inh2 = 200000
        test_region_2 = Region("TestRegion2", inh2, 1, 0, "T2",
                               base_r=1, base_death_factor=0, base_inf=inh2)
        # create borders list
        borders = [("TestRegion1", "TestRegion2")]
        # adjust new infections and currently infected based on adjacency
        impact = 20
        adjust_adjacent_regions(borders, [test_region_1, test_region_2], 0, impact=impact)

        # check if new infections are adjusted correctly
        updated_new_inf_1 = test_region_1.df["New infections"][0]
        updated_new_inf_2 = test_region_2.df["New infections"][0]
        self.assertEqual(inh1, updated_new_inf_1)
        self.assertEqual(inh2 - 50, updated_new_inf_2)


if __name__ == '__main__':
    unittest.main()
