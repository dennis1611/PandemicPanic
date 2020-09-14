population = 17000000
infected = [population * 0.0001]
R = [1.1]


def initialise_measures():
    """"Creates and returns a list of all measures"""
    # TODO: replace by real measures, when class is made & measures are chosen
    measures = ['measure 1', 'measure 2', 'measure 3']
    return measures


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
while True:
    print(f'\n This is week {week}')
    update_infected()

    display_report()

    choose_measure()

    week += 1
