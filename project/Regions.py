"""
File that contains the region class.
"""


class region:
    """
    Class that contains all information of a certain region.
    """

    def __init__(self,name,inhabitants,infected):
        self.name = name
        self.healthy = inhabitants - infected
        self.infected = infected
        self.dead = 0














