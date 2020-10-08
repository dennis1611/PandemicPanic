"""
The initialization functions for the measures and for the regions can be found here.
"""

from pandas import read_csv
from project.measure import Measure

import os


def initialise_measures():
    """"Creates and returns a list of all measures"""
    measures = []
    with open(os.path.abspath("measures_data_simple.csv")) as data:
        next(data)  # skip first line
        for line in data:
            line = line.strip().split(",")
            number = int(line[0])
            name = line[1]
            desc = line[2]
            factor = float(line[3])
            measures.append(Measure(number, name, desc, factor))
    return measures


def initialise_regions():
    """"Creates and returns a list of all regions"""
    from project.region import Region
    regions_df = read_csv(os.path.abspath("regional_data.csv"), index_col=0)
    region_instances = []
    region_names = regions_df.index.values
    for region in region_names:
        region = Region(region, regions_df.loc[region, "Population"],
                        regions_df.loc[region, "inf_factor"], regions_df.loc[region, "death_factor"],
                        regions_df.loc[region, "img_name"],regions_df.loc[region, "abbreviation"])
        region.load_pngs()
        region_instances.append(region)
    return region_instances
