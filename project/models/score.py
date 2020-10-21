from project.models.region import RegionExtended


class Score:
    def __init__(self, measures):
        self.score = 0
        self.base_penalties = [1 - measure.factor for measure in measures]

    def penalize_measure(self, regions, week, global_measures=None):
        # adjust the score based on measure taken and number of infections
        # TODO: figure out how to make this function read the measures currently active in a region
        # use active_measures dict
        limit = 0.05  # this is temporary until the percentages for the map color are certain
        light = 1
        heavy = 3
        result = 0
        for region in regions:
            # use region measures if visual mode, else use global measures
            if isinstance(region, RegionExtended):
                measures = region.region_measures
            else:
                measures = global_measures
            # calculate penalty for each measure in current region
            for i, measure in enumerate(measures):
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
