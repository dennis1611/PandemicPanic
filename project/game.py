import numpy as np
from project.region import Region


# create general setup
# population = 17000000
infected_total = [100]  # keeps track of how many people are infected each week
infected_new = [infected_total[0]]  # keeps track of how many people got infected during each week
R = [1.1]


# create regions
country = []

regions_data = np.genfromtxt("regions_data.txt", dtype=str)

try:
    # if multiple regions are present and activated this code runs
    for reg in range(len(regions_data)):
        country.append(Region(regions_data[reg, 0], int(regions_data[reg, 1]), 0))
except:
    # if there is only 1 region present, an exception will occur, making this code run
    # exception occurs since the array is only 1D instead of 2D
    country.append(Region(regions_data[0], int(regions_data[1]), infected_total[0]))
    # todo: have a random region start with a random amount of infections


# create measures
def initialise_measures():
    """"Creates and returns a list of all measures"""
    # TODO: replace by real measures, when class is made & measures are chosen
    return ['measure 1', 'measure 2', 'measure 3']


measures = initialise_measures()


# START weekly methods
def update_infected(current_week: int):
    """"Calculates how many people got infected and recovered in the past week"""

    # TODO: discuss calculations
    # Assumption is made that people stay sick for two weeks

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
    pass


def choose_measure():
    """"Displays all available measures to the user, and lets them choose one to take"""
    print('Choose one of the following measures:')
    for measure in measures:
        print(measure)
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
    R.append(R[0]) # TODO: actually update R
# END weekly methods


week = 1
running = True
while running:

    print(f'\n This is week {week}')
    update_infected(week)

    display_report()

    choose_measure()

    week += 1

    # TODO: move this to the proper display_report method when finished
    # basically the display report.
    print("*"*50)
    print("Region\t\t", "Healthy", "Sick", "Dead", sep="\t")
    for reg in range(len(country)):
        print(country[reg].name, country[reg].healthy, country[reg].infected, country[reg].dead, sep="\t")
    print("*" * 50)
