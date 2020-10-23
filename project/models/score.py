# these are currently instable if score is balanced!

import numpy as np
from project.models.region import RegionExtended


class Score:
    def __init__(self, measures):
        # use these attributes to balance the score system
        self.score = 0
        self.death_penalty = 100
        self.survivor_bonus = 1
        self.recover_bonus = 1
        self.effect_penalties = [1 - measure.factor for measure in measures]
        self.base_measure_penalty = 0.01
        self.regular_measure_modifier = 1
        self.strict_measure_modifier = 3
        self.limit = 0.001 # this is hardcoded to match the colours in the map.
        self.long_measure_modifier = 2
        self.patience = 10
        self.both_modifier = 6
        # this determines how the score is displayed at the end
        self.display_zeros = 3
        # this should stay the same
        self.length_matrix = np.zeros((len(measures), 12))

    def penalize_measure(self, regions, week, global_measures=None):
        """Adjust the score based on measure taken and number of infections"""
        result = 0
        for col, region in enumerate(regions):
            # use region measures if visual mode, else use global measures
            if isinstance(region, RegionExtended):
                measures = region.region_measures
            else:
                measures = global_measures

            for i, measure in enumerate(measures):
                if measure.is_active():
                    self.length_matrix[i][col] += 1
                    strict = region.df["Currently infected"][week] <= self.limit * region.inhabitants
                    long = self.length_matrix[i][col] > self.patience
                    if strict and long:
                        penalty_factor = self.both_modifier
                    elif strict:
                        penalty_factor = self.strict_measure_modifier
                    elif long:
                        penalty_factor = self.long_measure_modifier
                    else:
                        penalty_factor = self.regular_measure_modifier
                    result += penalty_factor * self.effect_penalties[i] * region.inhabitants
                else:
                    if self.length_matrix[i][col] > 0:
                        self.length_matrix[i][col] -= 1
        self.score -= self.base_measure_penalty * result

    def reward_survivors(self, regions, week):
        survived = 0
        deaths = 0
        for region in regions:
            deaths += region.df["Total deaths"][week]
            survived += region.inhabitants
        self.score += self.survivor_bonus * survived - self.death_penalty * deaths

    def reward_recoveries(self, regions, week):
        recovered = 0
        deaths = 0
        for region in regions:
            deaths += region.df["Total deaths"][week]
            recovered += region.df["Total recoveries"][week]
        self.score += self.recover_bonus * recovered - self.death_penalty * deaths

    def finalize_score(self):
        if self.score < 0:
            self.score = 0
        self.score = round(self.score, -1 * self.display_zeros)
