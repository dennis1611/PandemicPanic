class Measure:
    """
    Class that contains all aspects of a measure to be taken.
    Give it a name, a number, a description for the player and determine the types and attributes.
    Current types are:
    > R_reduce: Reduce the R factor by factor
    """

    def __init__(self, number, name, desc, factor, active=False):
        self.number = number
        self.name = name
        self.desc = desc
        self.factor = factor
        self.active = active

        # self.types = types

    # def __repr__(self):
    #     string = f"This is measure number {self.number}, called: {self.name}, and it has the following effects:"
    #     # TODO: self.types has (currently) been removed, make sure the following line works
    #     if "R_reduce" in self.types:
    #         string += f"\nReduce the R factor by {self.factor}"
    #     return string

    def __str__(self):
        """"Return a human readable string"""
        return f"#{self.number}| {self.active}| {self.name}: {self.desc}"

    def menu(self):
        """"Print the description of the measure for the player"""
        print(f"{str(self)}")

    # not needed for now
    # def effect(self, R_old):
    #     """Apply the measure on the right stat, according to its type"""
    #     if self.active:
    #         if "R_reduce" in self.types:
    #             R_new = R_old * self.factor
    #             return R_new
    #
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
