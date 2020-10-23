"""
The initialization functions for the measures and for the regions can be found here.
"""

import os

from pandas import read_csv
from project.models.measure import Measure
from project.models.region import Region, RegionExtended


def initialise_measures():
    """"Creates and returns a list of all measures"""
    project_path = os.path.dirname(os.path.dirname(__file__))
    file_path = project_path + '/source_data/measures_data_simple.csv'
    measures_df = read_csv(file_path, index_col=1)
    measures = []
    measure_names = measures_df.index.values
    for measure_name in measure_names:
        new_measure = Measure(measures_df.loc[measure_name, "number"],
                              measure_name,
                              measures_df.loc[measure_name, "description"],
                              measures_df.loc[measure_name, "factor"])
        measures.append(new_measure)
    return tuple(measures)


def initialise_regions(visual=False):
    """"Creates and returns a list of all regions"""
    project_path = os.path.dirname(os.path.dirname(__file__))
    file_path = project_path + '/source_data/regional_data.csv'
    regions_df = read_csv(file_path, index_col=0)
    regions = []
    region_names = regions_df.index.values
    if not visual:
        for region_name in region_names:
            new_region = Region(region_name,
                                regions_df.loc[region_name, "population"],
                                regions_df.loc[region_name, "inf_factor"],
                                regions_df.loc[region_name, "death_factor"],
                                regions_df.loc[region_name, "abbreviation"])
            regions.append(new_region)
    elif visual:
        for region_name in region_names:
            new_region = RegionExtended(region_name,
                                        regions_df.loc[region_name, "population"],
                                        regions_df.loc[region_name, "inf_factor"],
                                        regions_df.loc[region_name, "death_factor"],
                                        regions_df.loc[region_name, "abbreviation"],
                                        initialise_measures())
            regions.append(new_region)
    return tuple(regions)


def initialise_borders():
    """"Creates and returns a list of all borders (as tuple)"""
    project_path = os.path.dirname(os.path.dirname(__file__))
    file_path = project_path + '/source_data/borders.csv'
    borders = []
    with open(file_path) as borders_file:
        for line in borders_file:
            new_border = tuple(line.strip().split(','))
            borders.append(new_border)
    return tuple(borders)
