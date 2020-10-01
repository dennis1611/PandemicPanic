import pandas as pd


def display_report(regions):
    """"Displays a report to the user containing recent developments of the virus"""
    # these two make the DataFrame display entirely, and on one line:
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)
    print(regions[0].df)  # TODO: only displays information of Groningen, need to show others too
