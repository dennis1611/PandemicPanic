import pandas as pd


def display_report(regions):
    """"
    Displays a report to the user containing recent developments of the virus.
    This function takes the sum/average of all regions.
    """
    # these two make the DataFrame display entirely, and on one line:
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)

    # create global dataframe with same shape as region df's
    df_global = pd.DataFrame().reindex_like(regions[0].df)

    # take the sum of all infections and deaths, but average of R based on inh.
    sum_inh = 0
    for i, region in enumerate(regions):
        inh = region.inhabitants
        sum_inh += inh
        # += does not work when values are still NaN's, therefore distinction
        if not i > 0:
            df_global['New infections'] = region.df["New infections"]
            df_global['Currently infected'] = region.df["Currently infected"]
            df_global['New deaths'] = region.df["New deaths"]
            df_global['Total deaths'] = region.df["Total deaths"]
            df_global['New recoveries'] = region.df["New recoveries"]
            df_global['Total recoveries'] = region.df["Total recoveries"]
            df_global['R value'] = region.df["R value"] * inh
        else:
            df_global['New infections'] += region.df["New infections"]
            df_global['Currently infected'] += region.df["Currently infected"]
            df_global['New deaths'] += region.df["New deaths"]
            df_global['Total deaths'] += region.df["Total deaths"]
            df_global['New recoveries'] += region.df["New recoveries"]
            df_global['Total recoveries'] += region.df["Total recoveries"]
            df_global['R value'] += region.df["R value"] * inh
    df_global['R value'] = df_global["R value"] / sum_inh

    # only show the last 18 weeks
    print(df_global.tail(18))
