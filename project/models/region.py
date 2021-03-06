"""
File that contains the Region class.
"""

import os

import pandas as pd
import pygame as pg


class Region:
    """
    Class that contains all information of a certain region.
    Only has basic properties needed for terminal mode.
    """

    def __init__(self, name, inhabitants,
                 regional_infection_factor, regional_death_factor, abbreviation,
                 base_r=2.2, base_death_factor=0.02, base_inf=10):
        self.name = name
        self.inhabitants = inhabitants
        self.abbreviation = abbreviation
        self.inhabitants = inhabitants
        self.capacity = 0.01
        self.code_black_effect = 3
        self.code_black_active = False

        self.death_factor = base_death_factor * regional_death_factor

        region_r = base_r * regional_infection_factor

        df = pd.DataFrame(data=[[base_inf, base_inf, 0, 0, 0, 0, region_r]],
                          columns=['New infections',
                                   'Currently infected',
                                   'New deaths',
                                   'Total deaths',
                                   'New recoveries',
                                   'Total recoveries',
                                   'R value'],
                          index=[0])
        self.df = df

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}, "
        return string

    def get_limit_new_infections(self):
        """
        Returns the maximum amount of new infections possible based on last row of df.
        Note: previous week for update_infections -> limit_new_infections;
              current week for adjust_infections -> limit_exchange.
        """
        data_row = self.df.tail(1).iloc[0]
        limit_new_infections = self.inhabitants - \
                               data_row.loc['Currently infected'] - \
                               data_row.loc["Total recoveries"] - \
                               data_row.loc["Total deaths"]
        return limit_new_infections

    def update_infections(self, current_week):
        """"Calculates how many people got infected and recovered in the past week."""
        # get references for relevant data
        prev_data = self.df.loc[current_week - 1]
        prev_inf_total = prev_data.loc['Currently infected']
        prev_r = prev_data.loc['R value']

        new_infections = (1 / 2) * prev_r * prev_inf_total // 1

        # check if calculated new infections do not exceed physical limitations
        limit_new_infections = self.get_limit_new_infections()
        if new_infections > limit_new_infections:
            new_infections = limit_new_infections

        # people stay sick for two weeks; at the end, they either recover or die
        if current_week >= 2:
            prev_prev_inf_new = self.df.loc[current_week - 2, 'New infections']
            # increased deaths if code black is active
            if prev_inf_total > self.capacity * self.inhabitants:
                new_deaths = (prev_prev_inf_new * self.death_factor * self.code_black_effect) // 1
                self.code_black_active = True
            else:
                new_deaths = (prev_prev_inf_new * self.death_factor) // 1
                self.code_black_active = False
            new_recoveries = prev_prev_inf_new - new_deaths
        # no deaths or recoveries when there are not yet two weeks in the df
        else:
            new_deaths = 0
            new_recoveries = 0

        cur_inf = prev_data.loc['Currently infected'] + new_infections - new_recoveries - new_deaths

        # create and append the new row (with R as NaN)
        new_data = {'New infections': new_infections,
                    'Currently infected': cur_inf,
                    'New deaths': new_deaths,
                    'Total deaths': new_deaths + prev_data.loc['Total deaths'],
                    'New recoveries': new_recoveries,
                    'Total recoveries': new_recoveries + prev_data.loc['Total recoveries'],
                    'R value': None}
        self.df = self.df.append(new_data, ignore_index=True)

    # pylint: disable=invalid-name
    def update_R(self, current_week: int, factor: float):
        """Fills in R in the current week, based on the previous R * factor."""
        self.df.loc[current_week, 'R value'] = factor * self.df.loc[current_week - 1, 'R value']

    def get_data_row(self, week):
        """"Returns the dataframe row for given week."""
        return self.df.loc[week]

    def adjust_new_infections(self, week, amount):
        """"
        Adds or subtracts the given amount to latest new infections and currently infected
        Only used for adjacent regions effect.
        """
        self.df.loc[week, "New infections"] += amount
        self.df.loc[week, "Currently infected"] += amount

    def return_colour_code(self):
        """Return the colour code of this region"""
        # get current infections
        infections = self.df.tail(1).iloc[0].loc['Currently infected']
        # assert that the number of infections is not negative
        if infections < 0:
            raise ValueError("Infections cannot be negative")
        # calculate the colour code
        percentage = (infections / self.inhabitants) * 100
        num = ((percentage * (1 * percentage + 10)) ** 0.5 // 1) + 1
        if num > 6:
            return 6
        else:
            return int(num)


class RegionImg:
    """
    Class that has the properties of an image for the map.
    """

    def __init__(self, img_name, topleft, num):
        project_path = os.path.dirname(os.path.dirname(__file__))
        dir_path = project_path + '/source_data/provinces/'
        self.img = pg.image.load(dir_path + img_name.lower() + str(num) + ".png")
        self.img_rect = self.img.get_rect()
        self.img_rect.topleft = topleft


class RegionExtended(Region):
    """
    Child class of Region that is extended with functionalities for visual mode.
    """

    def __init__(self, name, inhabitants,
                 regional_infection_factor, regional_death_factor, abbreviation, region_measures,
                 base_r=2.2, base_death_factor=0.02, base_inf=10):
        super().__init__(name, inhabitants,
                         regional_infection_factor, regional_death_factor, abbreviation,
                         base_r=base_r, base_death_factor=base_death_factor, base_inf=base_inf)
        self.region_measures = region_measures
        self.images = []
        self.load_pngs()

    def load_pngs(self):
        """"Creates the images to be shown in the map."""
        topleft = (-30, 30)
        for i in range(7):
            self.images.append(RegionImg(self.name, topleft, i))

    def calculate_measures_factor(self, measure_statuses):
        """"
        Calculates the measure factor from scratch based on a list of measure statuses.
        Also updates the .active parameter of each measure.
        """
        active_factors = 1
        for i, measure_active in enumerate(measure_statuses):
            self.region_measures[i].active = measure_active
            if measure_active:
                active_factors *= self.region_measures[i].factor
        return active_factors

    def update_R(self, current_week: int, factor: float):
        """"
        Fills in R in the current week, based on the first R * factor.
        Overwrites method from parent class.
        """
        self.df.loc[current_week, 'R value'] = factor * self.df.loc[0, 'R value']
