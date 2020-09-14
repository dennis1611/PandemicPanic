import numpy as np
from project import Regions


# create general setup
# population = 17000000
infected = 100  # [population * 0.0001]
R = [1.1]


# create regions
country = []

regions_data = np.genfromtxt("Regions_data.txt", dtype=str)

try:
    # if multiple regions are present and activated this code runs
    for reg in range(len(regions_data)):
        country.append(Regions.region(regions_data[reg, 0], int(regions_data[reg, 1]), 0))
except:
    # if there is only 1 region present, an exception will occur, making this code run
    # exception occurs since the array is only 1D instead of 2D
    country.append(Regions.region(regions_data[0], int(regions_data[1]), infected))
    # todo: have a random region start with a random amount of infections


# create measures
def initialise_measures():
    """"Creates and returns a list of all measures"""
    # TODO: replace by real measures, when class is made & measures are chosen
    return ['measure 1', 'measure 2', 'measure 3']


measures = initialise_measures()


# START weekly methods
def update_infected():
    # += infected * R / 2, -= people who recovered (maybe  - infected[i-3] or something)
    pass


def display_report():
    pass


def choose_measure():
    print('Choose one of the following measures:')
    for measure in measures:
        print(measure)

    while True:
        measure_chosen = input()
        if measure_chosen in measures:
            print(f'You chose: {measure_chosen}, but note that it is not used yet in this version')
            break
        else:
            print(f'Your input: {measure_chosen}, is not recognised, please try again')

    update_R()


def update_R():
    pass
# END weekly methods


week = 0
running = True
while running:

    print(f'\n This is week {week}')
    update_infected()

    display_report()

    choose_measure()

    week += 1

    # basically the display report.
    print("*"*50)
    print("Region\t\t", "Healthy", "Sick", "Dead", sep="\t")
    for reg in range(len(country)):
        print(country[reg].name, country[reg].healthy, country[reg].infected, country[reg].dead, sep="\t")
    print("*" * 50)

    break  # TODO: remove break after testing


print()
print("Normal end.")
