"""
The initialization functions for the measures and for the regions can be found here.
"""

import os

from pandas import read_csv
from project.models.measure import Measure
from project.models.region import Region


def initialise_measures():
    """"Creates and returns a list of all measures"""
    measures_df = read_csv(os.path.abspath("source_data/measures_data_simple.csv"), index_col=1)
    measures = []
    measure_names = measures_df.index.values
    for measure_name in measure_names:
        new_measure = Measure(measures_df.loc[measure_name, "number"],
                              measure_name,
                              measures_df.loc[measure_name, "description"],
                              measures_df.loc[measure_name, "factor"])
        measures.append(new_measure)
    return tuple(measures)


def initialise_regions():
    """"Creates and returns a list of all regions"""
    regions_df = read_csv(os.path.abspath("source_data/regional_data.csv"), index_col=0)
    regions = []
    region_names = regions_df.index.values
    for region_name in region_names:
        new_region = Region(region_name,
                            regions_df.loc[region_name, "population"],
                            regions_df.loc[region_name, "inf_factor"],
                            regions_df.loc[region_name, "death_factor"],
                            regions_df.loc[region_name, "abbreviation"])
        regions.append(new_region)
    return tuple(regions)
