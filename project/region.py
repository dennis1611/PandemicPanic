



"""
File that contains the region class.
"""


class Region:
    """
    Class that contains all information of a certain region.
    """

    def __init__(self, name, inhabitants, infectionfactor, deathfactor, infected=0, deaths=0):
        self.name = name
        self.inhabitants = inhabitants
        self.infectionfactor = infectionfactor
        self.deathfactor = deathfactor
        self.infected = infected
        self.deaths = deaths

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}"

        return string



