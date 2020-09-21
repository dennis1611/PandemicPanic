from project import measure
from project.game import *
import pandas as pd
from pandas import read_csv
from project.measure import *

import pandas as pd

import numpy as np

desired_width=320

pd.set_option('display.width', desired_width)

np.set_printoptions(linewidth=desired_width)

pd.set_option('display.max_columns',15)

region_data = regions_df  # FIXME: do not simply use variables out of another file like this
region_names = region_data.index.values

arr_of_regional_inffactors = region_data.loc[:, "inf_factor"].values

row_count = regions_df.shape[0]  # FIXME: do not simply use variables out of another file like this

basis_R_arr = ([3] * row_count) * arr_of_regional_inffactors

R_df = pd.DataFrame(basis_R_arr, index = region_names, columns = ["Base_week"])

M1 = Measure("First test measure", 1, "This is the test measure", 0.7)

def update_R_df(week_n):
    new_R_to_multiply = 1

    colum_name = "Week " + str(week_n)

    measure = M1

    if measure.is_active:
        new_R_to_multiply = measure.factor * new_R_to_multiply

    R_df[colum_name] = R_df.iloc[:, week_n - 1] * new_R_to_multiply

    return R_df

for i in range(1, 10):
    update_R_df(i)

print(update_R_df(1))