import numpy as np


def choose_measure(measures):
    """"Displays all available measures to the user, and lets them choose one to take"""
    print('Choose one of the following measures:')
    for measure in measures:
        measure.menu()
    print('or #0| to take no action this turn')

    while True:
        user_input = input('\nYour choice (type a number): ')
        if validate_measure_input(user_input, measures):
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


def validate_measure_input(user_input, measures):
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
        if number_chosen in np.arange(1, len(measures) + 1):
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
