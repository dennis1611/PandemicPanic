from project.models.region import RegionExtended
import numpy as np


class Score:
    def __init__(self, measures):
        self.score = 0
        self.base_penalties = [1 - measure.factor for measure in measures]
        self.death_penalty = 100
        self.measure_penalty = 0.01
        self.display_zeros = 3
        self.length_mtrx = np.zeros((len(measures), 12))

    def penalize_measure(self, regions, measure_dict, week):
        # adjust the score based on measure taken and number of infections
        # TODO: figure out how to make this function read the measures currently active in a region
        # use active_measures dict
        limit = 0.001
        light = 1
        heavy = 3
        patience = 10
        result = 0
        for r, region in enumerate(regions):
            for i in range(len(measure_dict[region.name])):
                if measure_dict[region.name][i]:
                    self.length_mtrx[i][r] += 1
                    if region.df["Currently infected"][week] >= limit * region.inhabitants or \
                    self.length_mtrx[i][r] > patience:
                        result += heavy * self.base_penalties[i] * region.inhabitants
                    else:
                        result += light * self.base_penalties[i] * region.inhabitants
                else:
                    if self.length_mtrx[i][r] > 0:
                        self.length_mtrx[i][r] -= 1
        self.score -= self.measure_penalty * result

    def reward_survivors(self, regions):
        survived = 0
        deaths = 0
        for region in regions:
            deaths += region.df["Total deaths"][52]
            survived += region.inhabitants
        self.score += survived - self.death_penalty * deaths

    def finalize_score(self):
        if self.score < 0:
            self.score = 0
        self.score = round(self.score, -1 * self.display_zeros)
