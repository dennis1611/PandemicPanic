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


# START weekly methods
def update_infected(current_week: int):
    """"Calculates how many people got infected and recovered in the past week"""
    # Assumption is made that people stay sick for two weeks
    # TODO: replace separate calculations by dataframe




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

    print(regions_classes[0].df)


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


def update_R():
    """"Updates R based on the chosen measure"""
    R_measures = 1

    for measure in measures_classes:
        if measure.is_active():
            R_measures *= measure.factor

    return R_measures
# END weekly methods


# create general setup
infected_total = [100]  # keeps track of how many people are infected each week
infected_new = [infected_total[0]]  # keeps track of how many people got infected during each week
R = [1.1]

measures_classes, measure_numbers = initialise_measures()
regions_classes = initialise_regions()

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

    display_report()



    for region_class in regions_classes:
        region_class.add_data(update_R(), week)

    measure_this_week = choose_measure()
    # R.append(update_R(R[-1], measure_this_week))

    # for measure in measure:
    #   measure.effect()

    week += 1
