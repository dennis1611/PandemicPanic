"""
File that plots graphs of how the game was played in a new window.
"""

import matplotlib.pyplot as plt


def plot_graphs(regions):
    """
    Generates various graphs of how the game was played,
    showed in a separate window.
    """

    # which columns from region.df to plot
    to_plot_cols = ["Currently infected", "Total deaths"]
    num = 1
    plt.figure(figsize=(18, 6))
    for to_plot in to_plot_cols:
        plt.subplot(1, 3, num)
        for region in regions:
            region.df[to_plot].plot()
        plt.legend([region.abbreviation for region in regions], loc=2)
        plt.title(to_plot)
        plt.xlabel("Week")
        plt.ylabel("# of people")
        plt.ticklabel_format(axis="y", style="plain", scilimits=(0, 0))
        plt.grid()
        num += 1
    # also plot graph with infections per 100k people
    plt.subplot(1, 3, 3)
    for region in regions:
        plt.plot(region.df["Currently infected"].tolist() / region.inhabitants * 100000, label=region.abbreviation)
    plt.title("Infected per 100k")
    plt.xlabel("Week")
    plt.ylabel("# of people")
    plt.axhline(100, label="measures too strict", c="g", ls="--", )
    plt.axhline(2000, label="hospitals are full", c="r", ls="--")
    plt.legend(loc=2)
    plt.grid()
    plt.show()
