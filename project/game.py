"""
Main game loop.
.exe should activate this file.
"""

import matplotlib.pyplot as plt

from project.models.initialization import initialise_measures, \
    initialise_regions, \
    initialise_borders
from project.models.adjacency import adjust_adjacent_regions
from project.views.choose_mode import choose_mode
from project.views.measures_terminal import choose_measure
from project.views.report_terminal import display_report
from project.models.measure import Measure
# Screen is imported in an if VISUAL statement below


# TODO: write an actual welcome message/introduction
print('Welcome message/introduction')

# let the player choose to play in terminal mode or in visual mode
VISUAL = choose_mode()

# create general setup
measures = initialise_measures()
regions = initialise_regions(visual=VISUAL, measures=measures)
borders = initialise_borders()
STAR_LINE = '*' * 70

# Dictionary to locally store abbreviations
regions_dict = {}
for region in regions:
    regions_dict[region.name] = region.abbreviation

# extended setup only for visual mode
if VISUAL:
    # import the Screen class
    from project.views.screen import Screen
    # create a Screen
    window = Screen(len(regions), len(measures), regions_dict, measures)
    # set measures as attribute of each region instance (initialised as None)
    for region in regions:
        region.region_measures = measures


# main game loop
# pylint: disable=invalid-name
week = 1
running = True
while running:
    print('\n' + STAR_LINE)
    print(f'This is week {week}')
    print(STAR_LINE)

    # calculates the new infections for this week (leaving only the 'R value' column open)
    for region in regions:
        region.update_infections(week)

    # adjust new infections based on adjacent regions
    adjust_adjacent_regions(borders, regions, week)

    # shows a summary (in the terminal) of recent developments of the virus
    display_report(regions)
    print(STAR_LINE)

    # get new_measure / active measures

    # get factor(s) based on new_measure / active measures

    # update R based on factor

    if not VISUAL:
        # choose a measure, (de)activate it, and get the corresponding factor
        new_measure = choose_measure(measures)
        if isinstance(new_measure, Measure):
            effect = new_measure.update_return_factor()
        else:
            effect = 1

        # set the R value for this week
        for region in regions:
            region.update_R(week, effect)
    elif VISUAL:
        # update window
        # noinspection PyUnboundLocalVariable
        window.start_turn(regions, week)
        active_measures = window.end_turn(regions)

        for region in regions:
            factor = region.calculate_measures_factor(active_measures[region.name])
            region.update_R(week, factor)

    # end of week
    week += 1
    if week > 52:
        running = False

score = 0
for region in regions:
    score += region.df["Total deaths"][52]
if not VISUAL:
    print("The game has ended!")
elif VISUAL:
    # plotting (for balancing)
    to_plot_cols = ["Currently infected", "Total deaths"]  # column from df to plot
    for to_plot in to_plot_cols:
        plt.figure()
        for region in regions:
            region.df[to_plot].plot()
        plt.legend([region.abbreviation for region in regions])
        plt.title(to_plot)
        plt.xlabel("week")
        plt.ylabel("inhabitants")
        plt.show()
    # display the ending window
    window.end_game(score)
