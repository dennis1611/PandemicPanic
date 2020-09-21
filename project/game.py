from pandas import read_csv

from project.region import Region


# START weekly methods
def update_infected(current_week: int):
    """"Calculates how many people got infected and recovered in the past week"""
    # Assumption is made that people stay sick for two weeks
    # TODO: replace separate calculations by dataframe

    if current_week >= 2:
        # R-number tells how many other people an infected person infects during two weeks, hence the '* 1/2'
        infected_new.append(int(1/2 * (R[current_week-1] * infected_new[current_week-1] + R[current_week-2] * infected_new[current_week-2])))
        recoveries = int(infected_new[current_week - 2])
    else:
        infected_new.append(int(R[current_week-1] * infected_new[current_week-1]))
        recoveries = 0

    infected_total.append(int(infected_total[current_week-1] + infected_new[current_week] - recoveries))


def display_report():
    """"Displays a report to the user containing recent developments of the virus"""
    print('********************************')
    a = infected_total
    b = infected_new
    c = R
    print('Total number of infected people:')
    for x in range(len(a)):
        print(a[x])
    print()

    print('Number of new infected people:')
    for y in range(len(b)):
        print(b[y])
    print()

    print('R number:')
    for z in range(len(c)):
        print(c[z])
    print('\n********************************')


def choose_measure():
    """"Displays all available measures to the user, and lets them choose one to take"""
    print('Choose one of the following measures:')
    for measure in measures:
        print(measure)  # Should probably be measure.menu() eventually
    print('or "no measure" to take no action this turn')

    while True:
        measure_chosen = input('Your choice: ')
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


# create general setup
infected_total = [100]  # keeps track of how many people are infected each week
infected_new = [infected_total[0]]  # keeps track of how many people got infected during each week
R = [1.1]

measures = initialise_measures()
regions = initialise_regions()

# main game loop
week = 1
running = True
while running:
    print('\n********************************')
    print(f'This is week {week}')

    # If I understand correctly, this means the measures are taken at the end of the week,
    # to be applied on the calculations of the next week.

    update_infected(week)

    display_report()

    choose_measure()

    # for measure in measure:
    #   measure.effect()

    week += 1
