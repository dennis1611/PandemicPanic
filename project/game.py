"""
Main game loop.
.exe should activate this file.
"""

from project.models.initialization import initialise_measures, initialise_regions
from project.views.measures_terminal import choose_measure
from project.views.report_terminal import display_report
from project.screen import Screen
from project.measure import Measure


# TODO: write an actual welcome message/introduction
print('Welcome message/introduction')

visuals = False
print('do you want to play in "terminal mode" or in "visual mode"?')
running = True
while running:
    user_input = input()
    if user_input.lower()[0] == "t":
        visuals = False
        running = False
    elif user_input.lower()[0] == "v":
        visuals = True
        running = False
    else:
        print("please try again")


# create general setup
measures = initialise_measures()
regions = initialise_regions()
starline = '*' * 70

# Dictionary to locally store abbreviations
regions_dict = {}
for region in regions:
    regions_dict[region.name] = region.abbreviation


if visuals:
    window = Screen(len(regions), len(measures), regions_dict, regions)
    for region in regions:
        region.region_measures = measures


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
    display_report(regions)
    print(starline)

    if not visuals:
        # choose a measure, (de)activate it, and get the corresponding factor
        new_measure = choose_measure(measures)
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
    elif visuals:
        # update window
        # noinspection PyUnboundLocalVariable
        window.start_turn(regions)
        active_measures = window.end_turn(regions)
        print(active_measures)

        for region in regions:
            print(active_measures[region.name])
            factor = region.set_measures_factor(active_measures[region.name])
            print(factor)
            region.update_R_visual(week, factor)

    week += 1
