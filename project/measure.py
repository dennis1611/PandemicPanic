class Measure:
    """
    Class that contains all aspects of a measure to be taken.
    Give it a name, a number, a description for the player and determine the types and attributes.
    Current types are:
    > R_reduce: Reduce the R factor by R_influence
    """

    def __init__(self, name, number, desc, R_influence, active=False):
        self.name = name
        self.number = number
        self.desc = desc
        self.factor = R_influence
        self.active = active

        # self.types = types

        # if "R_reduce" in self.types:
        #     self.R_influence = R_influence

    def __repr__(self):
        string = f"This is measure number {self.number}, called: {self.name}, and it has the following effects:"
        # TODO: self.types has (currently) been removed, make sure the following line works
        if "R_reduce" in self.types:
            string += f"\nReduce the R factor by {self.R_influence}"
        return string

    def menu(self):
        """"Print the description of the measure for the player"""
        print(f"#{self.number}| {self.name}: {self.desc}")

    """""
    Willem's idea: do not perform the multiplication in the Measure class, 
    Instead perform this in the game.py file or a new file. 
    Makes the whole process easier, as it can be performed through matrix multiplication (DataFrames)
    
    The loop will look like this:
    
    R = 1
    for measure in measures:
        if measure.is_active:
            R = R * measure.factor
    """

    #
    # not needed for now
    # def effect(self, R_old):
    #     """Apply the measure on the right stat, according to its type"""
    #     if self.active:
    #         if "R_reduce" in self.types:
    #             R_new = R_old * self.R_influence
    #             return R_new
    #
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
