from pandas import read_csv
from project.measure import Measure
from project.region import Region


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
    region_names = regions_df.index.values
    for region in region_names:
        region = Region(region, regions_df.loc[region, "Population"],
                        regions_df.loc[region, "inf_factor"], regions_df.loc[region, "death_factor"])
        region_instances.append(region)
    return region_instances
# END initialising methods


# TODO: unused, check if this can be deleted
# def update_infected(current_week: int):
#     """"Calculates how many people got infected and recovered in the past week"""
#     # Assumption is made that people stay sick for two weeks

# START weekly methods
def display_report():
    """"Displays a report to the user containing recent developments of the virus"""
    print(regions[0].df)

    # TODO: unused, check if this can be deleted
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


def choose_measure():
    """"Displays all available measures to the user, and lets them choose one to take"""
    print('Choose one of the following measures:')
    for measure in measures:
        measure.menu()
    print('or #0| to take no action this turn')

    while True:
        measure_chosen = input('Your choice (type a number): ')  # This could probably use a better name
        if int(measure_chosen) in measure_numbers:
            measure_taken = measures[int(measure_chosen)-1]
            measure_taken.activate()
            print(f'You chose: {measure_taken.name}, but note that it is not used yet in this version')
            return measure_taken
        elif int(measure_chosen) == 0:
            print('You decided to take no action, the game will move on')
            return None
        else:
            print(f'Your input: {measure_chosen}, is not recognised, please try again')
# END weekly methods

# TODO: unused, check if this can be deleted
# def update_R():
#     """"Updates R based on the chosen measure"""
#     R_measures = 1
#
#     for measure in measures:
#         if measure.is_active():
#             R_measures *= measure.factor
#
#     return R_measures


# create general setup
measures, measure_numbers = initialise_measures()
regions = initialise_regions()

# TODO: unused, check if this can be deleted
# infected_total = [100]  # keeps track of how many people are infected each week
# infected_new = [infected_total[0]]  # keeps track of how many people got infected during each week
# R = [1.1]

# TODO: write an actual welcome message/introduction
print('Welcome message/introduction')

# main game loop
week = 1
running = True
while running:
    print('\n********************************')
    print(f'This is week {week}')

    # calculates the new infections for this week (leaving only the 'R value' column open)
    for region in regions:
        region.update_infections(week)

    # shows a summary of recent developments of the virus
    display_report()

    # choose a measure and get the corresponding factor
    new_measure = choose_measure()
    if isinstance(new_measure, Measure):
        effect = new_measure.factor
    else:
        effect = 1

    # set the R value for this week
    for region in regions:
        region.update_R(week, effect)

    # TODO: unused, check if this can be deleted
    # R.append(update_R(R[-1], measure_this_week))

    week += 1
