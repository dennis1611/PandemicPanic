"""
File that contains the region class.
"""

import pandas as pd


class Region:
    """
    Class that contains all information of a certain region.
    """

    def __init__(self, name, inhabitants, infectionfactor, deathfactor, base_r=3, base_inf=1000):
        self.name = name
        self.inhabitants = inhabitants
        self.infectionfactor = infectionfactor
        self.deathfactor = deathfactor
        region_r = base_r * infectionfactor

        df = pd.DataFrame(data=[[base_inf, base_inf, 0, 0, 0, 0, region_r]],
                          columns=['New infections', 'Total infections', 'New deaths', 'Total deaths', 'New recoveries',
                                   'Total recoveries', 'R value'],
                          index=[0])
        self.df = df

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}, " \
                 f"{self.infectionfactor}, {self.deathfactor}"

        return string

    def update_infections(self, current_week):
        """"Calculates how many people got infected and recovered in the past week"""
        # Assumption is made that people stay sick for two weeks

        prev_data = self.df.loc[current_week - 1]
        prev_inf = prev_data.loc['New infections']
        prev_r = prev_data.loc['R value']

        if current_week >= 2:
            prev_prev_inf = self.df.loc[current_week - 2, 'New infections']
            new_infections = (1 / 2) * (prev_r * prev_inf + prev_r * prev_prev_inf) // 1
            new_deaths = (prev_prev_inf * self.deathfactor) // 1
            new_recovs = prev_prev_inf - new_deaths
        else:
            new_infections = prev_r * prev_inf // 1
            new_deaths = 0
            new_recovs = 0

        new_data = {'New infections': new_infections,
                    'Total infections': prev_data.loc['Total infections'] + new_infections - new_recovs - new_deaths,
                    'New deaths': new_deaths, 'Total deaths': new_deaths + prev_data.loc['Total deaths'], 'R value': None,
                    'New recoveries': new_recovs, 'Total recoveries': new_recovs + prev_data.loc['Total recoveries']}
        self.df = self.df.append(new_data, ignore_index=True)

    def update_R(self, current_week, factor):
        self.df.loc[current_week, 'R value'] = factor * self.df.loc[current_week - 1, 'R value']
