"""
Main game loop.
.exe should activate this file.
"""

from project.initialization import initialise_measures, initialise_regions
from project.measure import Measure
from project.region import Region


def display_report():
    """"Displays a report to the user containing recent developments of the virus"""
    print(regions[0].df)  # TODO: only displays information of Groningen, need to show others too


def choose_measure():
    """"Displays all available measures to the user, and lets them choose one to take"""

    def validate_measure_input(user_input):
        """Returns a boolean whether the user's input to choose a measure is valid"""
        is_int = True
        number_chosen = -1
        try:
            number_chosen = int(user_input)
        except ValueError:
            is_int = False

        # if: the input was an int
        if is_int:
            # case 1 (valid): the input was an int corresponding to a measure
            if number_chosen in measure_numbers:
                return True
            # case 2 (valid): the input was 0
            elif number_chosen == 0:
                return True
            # case 3 (invalid): the input was an int out of bounds
            else:
                print(f'Your input: {number_chosen}, does not correspond to a measure, please try again')
                return False
        # else (invalid): the input was not an int
        else:
            print(f'Your input: {user_input}, is not valid, please enter an integer')
            return False

    print('Choose one of the following measures:')
    for measure in measures:
        measure.menu()
    print('or #0| to take no action this turn')

    while True:
        user_input = input('\nYour choice (type a number): ')
        if validate_measure_input(user_input):
            number_chosen = int(user_input)
            if number_chosen != 0:
                measure_chosen = measures[int(number_chosen) - 1]
                if measure_chosen.is_active() is False:
                    print(f'You chose: {measure_chosen.name}, it will be activated')
                    return measure_chosen
                elif measure_chosen.is_active() is True:
                    print(f'You chose: {measure_chosen.name}, it will be deactivated')
                    return measure_chosen
            elif number_chosen == 0:
                print('You decided to take no action, the game will move on')
                return None


# create general setup
measures, measure_numbers = initialise_measures()
regions = initialise_regions()
starline = '*' * 70

# TODO: write an actual welcome message/introduction
print('Welcome message/introduction')

# main game loop
week = 1
running = True
while running:
    print('\n' + starline)
    print(f'This is week {week}')
    print(starline)

    # calculates the new infections for this week (leaving only the 'R value' column open)
    for region in regions:
        region.update_infections(week)

    # shows a summary of recent developments of the virus
    display_report()
    print(starline)

    # choose a measure, (de)activate it, and get the corresponding factor
    new_measure = choose_measure()
    if isinstance(new_measure, Measure) and new_measure.is_active() is False:
        new_measure.activate()
        effect = new_measure.factor
    elif isinstance(new_measure, Measure) and new_measure.is_active() is True:
        new_measure.deactivate()
        effect = 1 / new_measure.factor
    else:
        effect = 1

    # set the R value for this week
    for region in regions:
        region.update_R(week, effect)

    week += 1
