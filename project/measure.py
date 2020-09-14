# This is a W.I.P., I'll improve it when Nigel finishes his class

class Measure:
    def __init__(self, name, number, influence, type):
        #
        self.name = name
        self.number = number
        self.influence = influence
        self.type = type

    def __repr__(self,):
        return f'''This measure has the following effects:
        Reduce the R-value for the chosen regions with a factor {self.effect}
        '''

    def effect(self, R_old):
        R_new = R_old * self.influence
        return R_new
