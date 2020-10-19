class Score:
    def __init__(self):
        self.score = 0

    @staticmethod
    def base_penalty(measure):
        # determine the base pnealty for a certain measure
        return 1 - measure.factor

    def penalize_measure(self, week, region, measures):
        # adjust the score based on measure taken and number of infections
        limit = 0.05
        light = 1
        heavy = 3
        if region.df["Currently Infected"] > limit * region.inhabitants
            pass
        else:
            pass
