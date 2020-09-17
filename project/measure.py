class Measure:
    """
    Class that contains all aspects of a measure to be taken.
    Give it a name, a number, a description for the player and determine the types and attributes.
    Current types are:
    > R_reduce: Reduce the R factor by R_influence
    """
    def __init__(self, name, number, desc, active, types, R_influence):
        # there may be different types of measures with different effects
        # maybe enter these as (a list of) strings?
        self.name = name
        self.number = number
        self.desc = desc
        self.types = types
        self.active = active
        if "R_reduce" in self.types:
            self.R_influence = R_influence

    def __repr__(self):
        string = f"This is measure number {self.number}, called: {self.name}, and it has the following effects:"
        if "R_reduce" in self.types:
            string += f"\nReduce the R factor by {self.R_influence}"
        return string

    def effect(self, R_old):
        """Apply the measure on the right stat, according to its type"""
        if self.active:
            if "R_reduce" in self.types:
                R_new = R_old * self.R_influence
                return R_new

    def menu(self):
        """"Print the description of the measure for the player"""
        print(f"#{self.number}| {self.name}: {self.desc}")


# # testing:
# M1 = Measure("Half the R", 1, "It halves the R!", ["R_reduce"], 0.5)
# R0 = 0.8
# print(f"R0 is {R0}")
# print(M1)
# M1.menu()
# R1 = M1.effect(R0)
# print(f"R1 is {R1}")
