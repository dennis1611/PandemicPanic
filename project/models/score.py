class Score:
    def __init__(self, measures):
        self.score = 0
        self.base_penalties = [1 - measure.factor for measure in measures]

    def penalize_measure(self, regions, week):
        # adjust the score based on measure taken and number of infections
        # TODO: figure out how to make this function read the measures currently active in a region
        # use active_measures dict
        limit = 0.05  # this is temporary until the percentages for the map color are certain
        light = 1
        heavy = 3
        result = 0
        for region in regions:
            region_measures = region.region_measures
            for i, measure in enumerate(region_measures):
                if measure.is_active():
                    if region.df["Currently infected"][week] <= limit * region.inhabitants:
                        result += light * self.base_penalties[i] * region.inhabitants
                    else:
                        result += heavy * self.base_penalties[i] * region.inhabitants
        self.score -= result

    def reward_survivors(self, regions):
        result = 0
        for region in regions:
            result += region.inhabitants - region.df["Total deaths"][52]
        self.score += result
