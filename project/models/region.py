"""
File that contains the region class.
"""
import os

import pandas as pd
import pygame as pg


class RegionImg:

    def __init__(self, img_name, topleft, num):
        project_path = os.path.dirname(os.path.dirname(__file__))
        dir_path = project_path + '/source_data/provinces/'
        self.img = pg.image.load(dir_path + img_name.lower() + str(num) + ".png")
        self.img_rect = self.img.get_rect()
        self.img_rect.topleft = topleft


class Region:
    """
    Class that contains all information of a certain region.
    """

    def __init__(self, name, inhabitants, regional_infection_factor, regional_death_factor, abbreviation,
                 base_r=3, base_death_factor=0.02, base_inf=1000):
        self.name = name
        self.inhabitants = inhabitants
        self.abbreviation = abbreviation
        self.inhabitants = inhabitants
        self.capacity = 0.01
        self.code_black_effect = 3  # both of these to be balanced later
        self.code_black_active = False

        # base_death_factor = 0.02
        self.death_factor = base_death_factor * regional_death_factor

        # base_r = 3
        region_r = base_r * regional_infection_factor

        df = pd.DataFrame(data=[[base_inf, base_inf, 0, 0, 0, 0, region_r]],
                          columns=['New infections', 'Currently infected', 'New deaths', 'Total deaths',
                                   'New recoveries', 'Total recoveries', 'R value'],
                          index=[0])
        self.df = df

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}, "
        return string

    def update_infections(self, current_week):
        """"Calculates how many people got infected and recovered in the past week"""
        # get references for relevant data
        prev_data = self.df.loc[current_week - 1]
        prev_inf_total = prev_data.loc['Currently infected']
        prev_r = prev_data.loc['R value']

        new_infections = (1 / 2) * prev_r * prev_inf_total // 1

        # check if calculated new infections do not exceed physical limitations
        limit_new_infections = self.inhabitants - prev_data.loc['Total recoveries'] - prev_data.loc[
            'Currently infected'] - prev_data.loc['Total deaths']
        if new_infections > limit_new_infections:
            new_infections = limit_new_infections

        # people stay sick for two weeks; at the end, they either recover or die
        if current_week >= 2:
            prev_prev_inf_new = self.df.loc[current_week - 2, 'New infections']
            if prev_prev_inf_new > self.capacity * self.inhabitants: # whether code black should be active or not
                new_deaths = (prev_prev_inf_new * self.death_factor * self.code_black_effect) // 1
                self.code_black_active = True
            else:
                new_deaths = (prev_prev_inf_new * self.death_factor) // 1
                self.code_black_active = False
            new_recoveries = prev_prev_inf_new - new_deaths
        else:
            new_deaths = 0
            new_recoveries = 0

        cur_infectious = prev_data.loc['Currently infected'] + new_infections - new_recoveries - new_deaths

        # create and append the new row (with R as NaN)
        new_data = {'New infections': new_infections,
                    'Currently infected': cur_infectious,
                    'New deaths': new_deaths,
                    'Total deaths': new_deaths + prev_data.loc['Total deaths'],
                    'New recoveries': new_recoveries,
                    'Total recoveries': new_recoveries + prev_data.loc['Total recoveries'],
                    'R value': None}
        self.df = self.df.append(new_data, ignore_index=True)

    def calculate_measure_effects(self, new_measure):
        pass

    def update_R(self, current_week: int, factor: float):
        """Fills in R in the current week, based on the previous R * factor"""
        self.df.loc[current_week, 'R value'] = factor * self.df.loc[current_week - 1, 'R value']


class RegionExtended(Region):
    def __init__(self, name, inhabitants, regional_infection_factor, regional_death_factor, abbreviation,
                 base_r=3, base_death_factor=0.02, base_inf=1000, region_measures=None):
        super().__init__(name, inhabitants, regional_infection_factor, regional_death_factor, abbreviation,
                         base_r=3, base_death_factor=0.02, base_inf=1000)
        self.region_measures = region_measures
        self.images = []
        self.load_pngs()

    def load_pngs(self):
        """"..."""
        topleft = (-30, 30)
        for i in range(6):
            self.images.append(RegionImg(self.name, topleft, i + 1))

    def update_R(self, current_week: int, factor: float):
        """"Fills in R in the current week, based on the first R * factor
                Overwrites method from parent class"""
        self.df.loc[current_week, 'R value'] = factor * self.df.loc[0, 'R value']

    def calculate_measures_factor(self, active_measures):
        """"..."""
        active_factors = 1

        for i in range(len(active_measures)):
            if active_measures[i]:
                active_factors *= self.region_measures[i].factor

        return active_factors

    # Doe de factor berekening nu even op de Nigel manier, zal aangepast worden
    def measure_booleans(self):
        booleans = []
        for measure in self.region_measures:
            booleans.extend([measure.is_active()])
        return booleans
