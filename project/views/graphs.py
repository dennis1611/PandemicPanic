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
    plt.figure(figsize=(18, 6))
    # also plot graph with infections per 100k people

    cols_to_plot = ['New infections', 'Currently infected', 'Total deaths']
    titles = ['Newly infected per 100k inhabitants', 'Infected per 100k inhabitants', 'Total deaths']
    for num, col in enumerate(cols_to_plot):
        plt.subplot(1, 3, num + 1)

        if col == "Currently infected":
            plt.axhline(100, label="measures too strict", c="g", ls="--", )
            plt.axhline(1000, label="hospitals are full", c="r", ls="--")
            for region in regions:
                plt.plot(region.df[col].tolist() / region.inhabitants * 100000, label=region.abbreviation)

        elif col == "New infections":
            for region in regions:
                plt.plot(region.df[col].tolist() / region.inhabitants * 100000, label=region.abbreviation)

        elif col == "Total deaths":
            for region in regions:
                region.df["Total deaths"].plot()

        plt.title(titles[num])
        plt.xlabel("Week")
        plt.ylabel("# of people")
        plt.legend(loc=2)
        plt.grid()
        plt.ticklabel_format(axis="y", style="plain", scilimits=(0, 0))
        plt.legend([region.abbreviation for region in regions], loc=2)

    plt.show()
