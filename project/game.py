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


# main game loop
# pylint: disable=invalid-name
week = 1
running = True
ended_early = True
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

        active_measures, running = window.end_turn(regions)

        for region in regions:
            factor = region.calculate_measures_factor(active_measures[region.name])
            region.update_R(week, factor)

    # update score tracker (global_measures argument only used for terminal mode)
    scorekeeper.penalize_measure(regions, week, global_measures=measures)

    # end of week
    week += 1
    if week > 52:
        running = False
        ended_early = False

# end of main game, ending starts here
scorekeeper.reward_survivors(regions, week-1)
final_deaths = 0
for region in regions:
    final_deaths += region.get_data_row(week-1).loc["Total deaths"]

if not VISUAL:
    print("The game has ended!")
    print(f'Your score is {scorekeeper.get_score()}')
elif VISUAL:
    # display the ending window
    if ended_early:
        window.end_game(-1, int(final_deaths))
    else:
        window.end_game(scorekeeper.get_score(), int(final_deaths))

# plotting (for balancing)
to_plot_cols = ["Currently infected", "Total deaths"]  # column from df to plot
num = 1
plt.figure(figsize=(18,6))
for to_plot in to_plot_cols:
    # plt.figure()
    plt.subplot(1, 3, num)
    for region in regions:
        region.df[to_plot].plot()
    plt.legend([region.abbreviation for region in regions], loc=2)
    plt.title(to_plot)
    plt.xlabel("Week")
    plt.ylabel("# of people")
    plt.ticklabel_format(axis="y", style="plain", scilimits=(0,0))
    plt.grid()
    num += 1
plt.subplot(1, 3, 3)
for region in regions:
    plt.plot(region.df["Currently infected"].tolist() / region.inhabitants * 100000, label=region.abbreviation)
plt.title("Infected per 100k")
plt.xlabel("Week")
plt.ylabel("# of people")
plt.axhline(100, label="measures too strict", c="g", ls="--",)
plt.axhline(2000, label="hospitals are full", c="r", ls="--")
plt.legend(loc=2)
plt.grid()
plt.show()
