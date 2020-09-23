from pandas import read_csv
from project.measure import Measure
from project.region import Region
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

# Basics for visuals, ignore
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 15)


# START initialising methods
def initialise_measures():
    """"Creates and returns a list of all measures"""
    measures = []
    numbers = []
    with open("measures_data_simple.csv") as data:
        next(data)  # skip first line
        for line in data:
            line = line.strip().split(",")
            number = int(line[0])
            name = line[1]
            desc = line[2]
            factor = float(line[3])
            measures.append(Measure(number, name, desc, factor))
            numbers.append(number)
    return measures, numbers


def initialise_regions():
    """"Creates and returns a list of all regions"""
    regions_df = read_csv('regional_data.csv', index_col=0)
    region_instances = []
    for region in regions_df.index.values:
        region = Region(region, regions_df.loc[region, "Population"],
                        regions_df.loc[region, "inf_factor"], regions_df.loc[region, "death_factor"])
        region_instances.append(region)
    return regions_df, region_instances
# END initialising methods


# START weekly methods
def update_infected(current_week: int):
    """"Calculates how many people got infected and recovered in the past week"""
    # Assumption is made that people stay sick for two weeks
    # TODO: replace separate calculations by dataframe

    if current_week >= 2:
        # R-number tells how many other people an infected person infects during two weeks, hence the '* 1/2'
        newinf_df.loc[:, f"Week {current_week}"] = \
            (1/2 * (R_df.loc[:, f"Week {current_week-1}"] * newinf_df.loc[:, f"Week {current_week-1}"] +
                    R_df.loc[:, f"Week {current_week-2}"] * newinf_df.loc[:, f"Week {current_week-1}"]))
        # recoveries = newinf_df.loc[f"Week {current_week - 2}"]
    else:
        newinf_df.loc[:, f"Week {current_week}"] = \
            (R_df.loc[:, f"Week {current_week - 1}"] * newinf_df.loc[:, f"Week {current_week -1}"])
        # recoveries = 0


def display_report():
    """"Displays a report to the user containing recent developments of the virus"""
    # print('********************************')
    # a = infected_total
    # b = infected_new
    # c = R
    # print('Total number of infected people:')
    # for x in range(len(a)):
    #     print(a[x])
    # print()
    #
    # print('Number of new infected people:')
    # for y in range(len(b)):
    #     print(b[y])
    # print()
    #
    # print('R number:')
    # for z in range(len(c)):
    #     print(c[z])
    # print('\n********************************')

    df_with_only_integers = newinf_df.round(decimals=0)
    print(df_with_only_integers)

    print(R_df)


def choose_measure():
    """"Displays all available measures to the user, and lets them choose one to take"""
    print('Choose one of the following measures:')
    for measure in measures_classes:
        measure.menu()
    print('or #0| to take no action this turn')

    while True:
        measure_chosen = input('Your choice (type a number): ')  # This could probably use a better name
        if int(measure_chosen) in measure_numbers:
            measure_taken = measures_classes[int(measure_chosen)-1]
            measure_taken.activate()
            print(f'You chose: {measure_taken.name}, but note that it is not used yet in this version')
            return measure_taken
        elif int(measure_chosen) == 0:
            print('You decided to take no action, the game will move on')
            return None
        else:
            print(f'Your input: {measure_chosen}, is not recognised, please try again')


def update_r(week_n):
    """"Updates R based on the chosen measure"""
    base_year = R_df.loc[:, 'Week 0']
    measure_factor = calc_r_from_base()

    R_df[f'Week {week_n}'] = measure_factor * base_year


def calc_r_from_base():
    measure_factors = 1
    for measure in measures_classes:
        if measure.is_active():
            measure_factors = measure_factors * measure.factor

    return measure_factors

# END weekly methods


# create general setup
measures_classes, measure_numbers = initialise_measures()
regions_data, regions_classes = initialise_regions()

# Create DataBase for the R value
region_names = regions_data.index.values
base_R = 3
arr_of_regional_inffactors = regions_data.loc[:, "inf_factor"].values
row_count = regions_data.shape[0]
basis_R_arr = ([base_R] * row_count) * arr_of_regional_inffactors
R_df = pd.DataFrame(basis_R_arr, index=region_names, columns=['Week 0'])

# Create DataBase for the new infections
starting_infections_per_region = 1000
starting_infs = [starting_infections_per_region] * row_count
newinf_df = pd.DataFrame(starting_infs, index=region_names, columns=['Week 0'])

# TODO: write an actual welcome message/introduction
print('Welcome message/introduction')

# main game loop
week = 1
running = True
while running:
    print('\n********************************')
    print(f'This is week {week}')

    # If I understand correctly, this means the measures are taken at the end of the week,
    # to be applied on the calculations of the next week.
    measure_this_week = choose_measure()

    update_infected(week)
    update_r(week)

    display_report()

    measure_this_week = choose_measure()

    R.append(update_R(R[-1], measure_this_week))

    # for measure in measure:
    #   measure.effect()

    week += 1
