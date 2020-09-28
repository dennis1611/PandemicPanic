"""
Main game loop.
.exe should activate this file.
"""

from project.initialization import initialise_measures,initialise_regions
from project.measure import Measure
from project.region import Region
from screen import Screen


# TODO: unused, check if this can be deleted
# def update_infected(current_week: int):
#     """"Calculates how many people got infected and recovered in the past week"""
#     # Assumption is made that people stay sick for two weeks

# START weekly methods
def display_report():
    """"Displays a report to the user containing recent developments of the virus"""
    print(regions[0].df) #TODO: only displays information of Groningen, need to show others too

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


def choose_measure(window):
    """"Displays all available measures to the user, and lets them choose one to take"""

    '''
    print('Choose one of the following measures:')
    for measure in measures:
        measure.menu()
    print('or #0| to take no action this turn')
    '''

    while True:
        measure_chosen = window.click_measure()#input('Your choice (type a number): ')  # This could probably use a better name
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
#print('Welcome message/introduction')

# main game loop
week = 1
running = True
window = Screen()
while running:
    #print('\n********************************')
    print(f'This is week {week}')

    # calculates the new infections for this week (leaving only the 'R value' column open)
    for region in regions:
        region.update_infections(week)

    # shows a summary of recent developments of the virus
    display_report()

    #update window
    window.start_turn(regions)


    # choose a measure and get the corresponding factor
    new_measure = choose_measure(window)
    if isinstance(new_measure, Measure):
        effect = new_measure.factor
    else:
        effect = 1

    #effect = 1 #todo get rid of this

    # set the R value for this week
    for region in regions:
        region.update_R(week, effect)


    # TODO: unused, check if this can be deleted
    # R.append(update_R(R[-1], measure_this_week))

    week += 1

    window.check_quit()



