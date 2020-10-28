"""
Main game Controller.
"""

import matplotlib.pyplot as plt

from project.models.initialization import initialise_measures, \
    initialise_regions, \
    initialise_borders
from project.models.adjacency import adjust_adjacent_regions
from project.views.choose_mode import choose_mode
from project.views.measures_terminal import choose_measure
from project.views.report_terminal import display_report
from project.views.graphs import plot_graphs
from project.models.measure import Measure
from project.models.score import Score
# Screen is imported in an if VISUAL statement below


print('Welcome to PandemicPanic! '
      'Please find the readme for instructions of this game.')

# let the player choose to play in terminal mode or in visual mode
VISUAL = choose_mode()

# create general setup
measures = initialise_measures()
regions = initialise_regions(visual=VISUAL)
borders = initialise_borders()
scorekeeper = Score(measures)
STAR_LINE = '*' * 70

# extended setup only for visual mode
if VISUAL:
    # import the Screen class
    from project.views.screen import Screen
    # create a Screen
    window = Screen(len(regions), len(measures), measures)

# main game loop

# pylint: disable=invalid-name
week = 1
running = True
ended_early = True
while running:
    print('\n' + STAR_LINE)
    print(f'This is week {week}')
    print(STAR_LINE)

    # 1; calculate new infections for this week (leaving only the 'R value' column open)
    for region in regions:
        region.update_infections(week)

    # 2; adjust new infections based on adjacent regions
    adjust_adjacent_regions(borders, regions, week)

    # 3; shows a summary (in the terminal) of recent developments of the virus
    display_report(regions)
    print(STAR_LINE)

    # 4; get new_measure / active measures
    # 5; get factor(s) based on new_measure / active measures
    # 6; update R based on factor
    if not VISUAL:
        # choose a measure, (de)activate it, and get the corresponding factor
        new_measure = choose_measure(measures)
        if isinstance(new_measure, Measure):
            effect = new_measure.update_return_factor()
        else:
            effect = 1

        for region in regions:
            # set the R value for this week
            region.update_R(week, effect)
    elif VISUAL:
        # update window
        window.start_turn(regions, week)
        active_measures, running = window.end_turn(regions)

        for region in regions:
            # get the factor to multiply base-R with, and update measure statuses
            factor = region.calculate_measures_factor(active_measures[region.name])
            # set the R value for this week
            region.update_R(week, factor)

    # 7; update score tracker (global_measures only used for terminal mode)
    scorekeeper.penalize_measure(regions, week, global_measures=measures)

    # end of week
    week += 1
    if week > 52:
        running = False
        ended_early = False

# end of main game, ending starts here

# update score tracker and get ending information
scorekeeper.reward_survivors(regions, week-1)
final_deaths = sum([region.get_data_row(week-1).loc["Total deaths"] for region in regions])

# show the ending and score to the player
if not VISUAL:
    print("The game has ended!")
    print(f'Your score is {scorekeeper.get_score()}')
elif VISUAL:
    if ended_early:
        window.end_game(-1, int(final_deaths))
    else:
        window.end_game(scorekeeper.get_score(), int(final_deaths))

# show graphs of how the game was played in new window
plot_graphs(regions)
