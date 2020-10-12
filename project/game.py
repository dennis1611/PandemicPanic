"""
Main game loop.
.exe should activate this file.
"""

from project.models.initialization import initialise_measures, initialise_regions
from project.views.choose_mode import choose_mode
from project.views.measures_terminal import choose_measure
from project.views.report_terminal import display_report
from project.views.screen import Screen
from project.models.measure import Measure


# TODO: write an actual welcome message/introduction
print('Welcome message/introduction')

# let the player choose to play in terminal mode or in visual mode
visual = choose_mode()

# create general setup
measures = initialise_measures()
regions = initialise_regions()
starline = '*' * 70

# Dictionary to locally store abbreviations
regions_dict = {}
for region in regions:
    regions_dict[region.name] = region.abbreviation

# extended setup only for visual mode
if visual:
    # create a Screen
    window = Screen(len(regions), len(measures), regions_dict, regions)
    # set measures as attribute of each region instance (initialised as None)
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

    if not visual:
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
            region.update_R(week, effect, False)
    elif visual:
        # update window
        # noinspection PyUnboundLocalVariable
        window.start_turn(regions, week)
        active_measures = window.end_turn(regions)
        print(active_measures)

        for region in regions:
            print(active_measures[region.name])
            factor = region.calculate_measures_factor(active_measures[region.name])
            print(factor)
            region.update_R(week, factor, True)

    # end of week
    week += 1
    if week > 52:
        running = False

score = 100
if not visual:
    print("The game has ended!")
elif visual:
    # display the ending window
    window.end_game(score)
