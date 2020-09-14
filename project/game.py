def update_infected():
    # += infected * R / 2, -= people who recovered (maybe  - infected[i-3] or something)
    pass

def display_report():
    pass

def choose_measure():
    update_R()

def update_R():
    pass

population = 17000000
infected = population * 0.0001  # ideally save as list
R = 1.1

week = 0
while True:
    update_infected()

    display_report()

    choose_measure()

    week += 1

