import numpy as np
from pandas import read_csv

from project.region import Region


# START weekly methods
def update_infected(current_week: int):
    """"Calculates how many people got infected and recovered in the past week"""
    # Assumption is made that people stay sick for two weeks
    # TODO: discuss calculations

    if week >= 2:
        # R-number tells how many other people an infected person infects during two weeks, hence the '* 1/2'
        infected_new.append(1/2 * (R[current_week-1] * infected_new[current_week-1] + R[current_week-2] * infected_new[current_week-2]))
        recoveries = infected_new[current_week - 2]
    else:
        infected_new.append(R[current_week-1] * infected_new[current_week-1])
        recoveries = 0

    infected_total.append(infected_total[current_week-1] + infected_new[current_week] - recoveries)


def display_report():
    """"Displays a report to the user containing recent developments of the virus"""
    # TODO: write display report here, based on infected_total[], infected_new[] and R[], not using Region class yet

    # mock report based on Region class
    # *********************************
    # print("*" * 50)
    # print("Region\t\t", "Healthy", "Sick", "Dead", sep="\t")
    # for reg in range(len(regions)):
    #     print(regions[reg].name, regions[reg].healthy, regions[reg].infected, regions[reg].dead, sep="\t")
    # print("*" * 50)


def choose_measure():
    """"Displays all available measures to the user, and lets them choose one to take"""
    print('Choose one of the following measures:')
    for measure in measures:
        print(measure)  # Should probably be measure.menu() eventually
    print('or "no measure" to take no action this turn')

    while True:
        print('Your choice: ', end='')
        measure_chosen = input()
        if measure_chosen in measures:
            print(f'You chose: {measure_chosen}, but note that it is not used yet in this version')
            break
        elif measure_chosen == "no measure":
            print('You decided to take no action, the game will move on')
            break
        else:
            print(f'Your input: {measure_chosen}, is not recognised, please try again')

    update_R()


def update_R():
    """"Updates R based on the chosen measure"""
    R.append(R[0])  # TODO: actually update R
# END weekly methods


# START initialising methods
def initialise_measures():
    """"Creates and returns a list of all measures"""
    # TODO: replace by real measures, when class is made & measures are chosen
    return ['measure 1', 'measure 2', 'measure 3']


def initialise_regions():

    regions_df = read_csv('regional_data.csv', index_col=0)
    regions_classes = []
    region_names = regions_df.index.values
    for region in region_names:
        region = Region(region, regions_df.loc[region, "Population"],
                        regions_df.loc[region, "inf_factor"], regions_df.loc[region, "death_factor"])
        regions_classes.append(region)
    return regions_classes

# END initialising methods


# create general setup
infected_total = [100]  # keeps track of how many people are infected each week
infected_new = [infected_total[0]]  # keeps track of how many people got infected during each week
R = [1.1]

measures = initialise_measures()
regions = initialise_regions()
print(regions)

# main game loop
week = 1
running = True
while running:
    print(f'\n This is week {week}')

    # If I understand correctly, this means the measures are taken at the end of the week,
    # to be applied on the calculations of the next week.

    update_infected(week)

    display_report()

    choose_measure()

    # for measure in measure:
    #   measure.effect()

    week += 1
