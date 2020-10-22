from project.models.region import RegionExtended


class Score:
    def __init__(self, measures):
        self.score = 0
        self.base_penalties = [1 - measure.factor for measure in measures]
        self.death_penalty = 100
        self.measure_penalty = 1
        self.display_zeros = 3

    def penalize_measure(self, regions, measure_dict, week):
        # adjust the score based on measure taken and number of infections
        # TODO: figure out how to make this function read the measures currently active in a region
        # use active_measures dict
        limit = 0.05 # this is temporary until the percentages for the map color are certain
        light = 1
        heavy = 3
        result = 0
        for region in regions:
            for i in range(len(measure_dict[region.name])):
                if measure_dict[region.name][i]:
                    if region.df["Currently infected"][week] <= limit * region.inhabitants:
                        result += light * self.base_penalties[i] * region.inhabitants
                    else:
                        result += heavy * self.base_penalties[i] * region.inhabitants
        self.score -= self.measure_penalty * result

    def reward_survivors(self, regions):
        survived = 0
        deaths = 0
        for region in regions:
            deaths += region.df["Total deaths"][52]
            survived += region.inhabitants
        self.score += survived - self.death_penalty * deaths

    def finalize_score(self):
        # if self.score < 0:
        #     self.score = 0
        self.score = round(self.score, -1 * self.display_zeros)
