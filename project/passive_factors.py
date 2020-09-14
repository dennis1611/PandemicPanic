import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv

data = read_csv('data_prov.csv', skiprows=[0, 1, 2, 4], delimiter=";", index_col=0, skipinitialspace=True, decimal=',',
                skipfooter=1, engine='python')

names = list(data)
 # Unnamed kolommen weghalen
for name in names:
    if "Unnamed" in name:
        data.pop(name)

# Rename columns
columns = ['Bevolking', '0 tot 5 (%)', '5 tot 10 (%)', '10 tot 15 (%)', '15 tot 20 (%)', '20 tot 25 (%)',
           '25 tot 45 (%)', '45 tot 65 (%)', '65 tot 80 (%)', '80 tot 120 (%)', 'Dichtheid']
data.columns = columns

# Array van namen van regio's
regios = data.index.values

# Aparte DataFrame maken voor bevolking en dichtheid
Bevolkingsaantallen = data.filter(items=['Bevolking'])

# Aparte DataFrame maken voor percentages
percentages = data.filter(regex="(%)")


# Functie om factoren voor de dichtheid te bepalen
def dichtheidsfactoren(Algemene_dataset):
    df = Algemene_dataset.filter(items=['Dichtheid'])

    # BELANGFACTOR: ALS DE DICHTHEID EEN TE GROTE/KLEINE ROL SPEELT IN DE SIMULATIE PAS JE DEZE AAN (hoger = meer invloed)
    belang = 0.4

    # Gemiddelde bepalen
    avg = float(df.mean(axis=0))

    # Lijst van factoren aanmaken
    factors_dict = {}
    factors_list = []

    # Voor elk gebied de factor berekenen
    for i in range(len(df)):
        # Dichtheid vinden in DataFrame
        regio_dichtheid = df.iloc[i, 0]

        # Factor berekenen en toevoegen
        factor = (regio_dichtheid / avg) ** belang
        factors_dict[regios[i]] = factor
        factors_list.append(factor)

    return factors_list

print(dichtheidsfactoren(data))