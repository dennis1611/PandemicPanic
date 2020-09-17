from project.passive_factors import *

regions = Populations.index.values

"""
File that contains the region class.
"""


class Region:
    """
    Class that contains all information of a certain region.
    """

    def __init__(self, name, inhabitants, infection_factor, death_factor, infected=0):
        self.name = name
        self.inhabitants = inhabitants
        # self.healthy = inhabitants - infected
        self.infected = infected
        self.dead = 0

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}"

        return string


for region in regions:
    region = Region(region, Populations.loc[region].values[0],
                    total_infectionfactor(data)[region], total_deathfactor(data)[region])
