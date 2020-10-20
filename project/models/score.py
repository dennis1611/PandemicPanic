class Score:
    def __init__(self):
        self.score = 0

    @staticmethod
    def base_penalty(measure):
        # determine the base penalty for a certain measure
        return 1 - measure.factor

    def penalize_measure(self, region, measures):
        # adjust the score based on measure taken and number of infections
        # TODO: figure out how to make this function read the measures currently active in a region
        limit = 0.05
        light = 1
        heavy = 3
        for measure in measures:
            if measure.active:
                if region.df["Currently Infected"] > limit * region.inhabitants:
                    self.score -= self.base_penalty(measure) * heavy
                else:
                    self.score -= self.base_penalty(measure) * light
