"""
The initialization functions for the measures and for the regions can be found here.
"""

from pandas import read_csv
from project.measure import Measure
from project.region import Region

import os


def initialise_measures():
    """"Creates and returns a list of all measures"""
    measures = []
    with open(os.path.abspath("source_data/measures_data_simple.csv")) as data:
        next(data)  # skip first line
        for line in data:
            line = line.strip().split(",")
            number = int(line[0])
            name = line[1]
            desc = line[2]
            factor = float(line[3])
            measures.append(Measure(number, name, desc, factor))
    return tuple(measures)


def initialise_regions():
    """"Creates and returns a list of all regions"""
    regions_df = read_csv(os.path.abspath("source_data/regional_data.csv"), index_col=0)
    region_instances = []
    region_names = regions_df.index.values
    for region_name in region_names:
        region = Region(region_name, regions_df.loc[region_name, "Population"],
                        regions_df.loc[region_name, "inf_factor"], regions_df.loc[region_name, "death_factor"],
                        regions_df.loc[region_name, "abbreviation"])
        region_instances.append(region)
    return tuple(region_instances)
