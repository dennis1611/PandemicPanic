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

        df = pd.DataFrame(data=[[base_inf, base_inf, 0, 0, region_r]],
                          columns=['New infections', 'Total infections', 'New deaths', 'Total deaths', 'R value'],
                          index=[0])
        self.df = df

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}, " \
                 f"{self.infectionfactor}, {self.deathfactor}"

        return string

    def update_infections(self, current_week):
        """"Calculates how many people got infected and recovered in the past week"""
        # Assumption is made that people stay sick for two weeks
        # TODO: calculate with recoveries
        # TODO: calculate with deaths

        prev_data = self.df.loc[current_week - 1]
        prev_inf = prev_data.loc['New infections']
        prev_r = prev_data.loc['R value']

        if current_week >= 2:
            prev_prev_inf = self.df.loc[current_week - 2, 'New infections']
            new_infections = 1 / 2 * (prev_r * prev_inf + prev_r * prev_prev_inf) // 1
        else:
            new_infections = prev_r * prev_inf // 1

        new_data = {'New infections': new_infections,
                    'Total infections': new_infections + prev_data.loc['Total infections'],
                    'New deaths': 0, 'Total deaths': 0, 'R value': None}
        self.df = self.df.append(new_data, ignore_index=True)

    def update_R(self, current_week, factor):
        self.df.loc[current_week, 'R value'] = factor * self.df.loc[current_week - 1, 'R value']

    # TODO: unused, check if this can be deleted
    # def update_infected(self, current_week):
    #     """"Calculates how many people got infected and recovered in the past week"""
    #     # Assumption is made that people stay sick for two weeks
    #
    #     if current_week >= 2:
    #         # R-number tells how many other people an infected person infects during two weeks, hence the '* 1/2'
    #         prev_infs = self.df.loc[current_week - 1, 'New infections']
    #         prev_prev_infs = self.df.loc[current_week - 2, 'New infections']
    #         prev_r = self.df.loc[current_week - 1, 'R value']
    #
    #         new_infections = 1/2 * (prev_r * prev_infs + prev_r * prev_prev_infs) // 1
    #         # recoveries = 0
    #     else:
    #         new_infections = self.df.loc[current_week - 1, 'R value'] * \
    #                          self.df.loc[current_week - 1, 'New infections'] // 1
    #         # recoveries = 0
    #
    #     return new_infections
    #
    # def add_data(self, measure_factor, week_n):
    #
    #     new_r = measure_factor * self.region_r
    #     prev_data = self.df.loc[week_n - 1]
    #
    #     new_infs = self.update_infected(week_n, new_r)
    #     new_row = {'New infections': new_infs, 'Total infections': new_infs + prev_data.loc['Total infections'],'New deaths': 0,'Total deaths': 0, 'R value': new_r}
    #
    #     self.df = self.df.append(new_row, ignore_index=True)
