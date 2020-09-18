

"""
File that contains the region class.
"""


class Region:
    """
    Class that contains all information of a certain region.
    """

    def __init__(self, name, inhabitants, infected=0):
        self.name = name
        self.inhabitants = inhabitants
        self.infected = infected
        self.dead = 0

    def __repr__(self):
        string = f"This class is for {self.name} with a population of {self.inhabitants}"

        return string
