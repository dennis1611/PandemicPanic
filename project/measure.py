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

    def __str__(self):
        """"Return a human readable string"""
        return f"#{self.number}| {self.active}| {self.name}: {self.desc}"

    def menu(self):
        """"Print the description of the measure for the player"""
        print(f"{str(self)}")

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
