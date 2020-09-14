from pandas import read_csv

# Provincie data verzamelen en in een DataFrame stoppen
prov_data = read_csv('Data_provincies.csv', skiprows=[0, 1, 2, 4], delimiter=";",
                     index_col=0, skipinitialspace=True, decimal=',', skipfooter=1, engine='python')

# COROP data verzamelen en in een DataFrame stoppen
cor_data = read_csv('Data_coroppen.csv', skiprows=0, delimiter=";",
                    index_col=1, skipinitialspace=True, decimal=',', skipfooter=1, engine='python')

# Bepalen welke dataset je wilt gebruiken: de code is zo geschreven dat het allebei werkt
data = cor_data

# Eerste kolom weghalen; onnodige informatie
data = data.iloc[:, 1:]

# Rename columns
columns = ['Bevolking', '0 tot 5 (%)', '5 tot 10 (%)', '10 tot 15 (%)', '15 tot 20 (%)', '20 tot 25 (%)',
           '25 tot 45 (%)', '45 tot 65 (%)', '65 tot 80 (%)', '80 tot 120 (%)', 'Dichtheid']
data.columns = columns

# Array van namen van regio's
regios = data.index.values

# Aparte DataFrame maken voor bevolkingsaantallen (handig voor het aantal besmettingen)
Bevolkingsaantallen = data.filter(items=['Bevolking'])


# Functie om factoren voor de dichtheid te bepalen
def dichtheidsfactoren(algemene_dataset):
    df = algemene_dataset.filter(items=['Dichtheid'])

    # BELANGFACTOR: ALS DE DICHTHEID EEN TE GROTE/KLEINE ROL SPEELT PAS JE DEZE AAN (hoger = meer invloed)
    belang = 0.4

    # Gemiddelde bepalen
    avg = float(df.mean(axis=0))

    # Lijst van factoren aanmaken (de data is als dict{} of als list[] verkrijgbaar, verander bij return)
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

    return factors_dict


# Functie om factoren voor de jeugd te bepalen
def leeftijdsfactoren(algemene_dataset):
    # 'Jeugd' DataFrame aanmaken beestaande uit kolommen van tussen de 15 en 25
    jeugd = algemene_dataset.filter(items=['15 tot 20 (%)', '20 tot 25 (%)'])
    jeugd["totale_jeugd (%)"] = jeugd['15 tot 20 (%)'] + jeugd['20 tot 25 (%)']

    df = jeugd.filter(items=['totale_jeugd (%)'])

    # ALS DE JEUGDVERHOUDING EEN TE GROTE/KLEINE ROL SPEELT PAS JE DEZE AAN (hoger = meer invloed)
    belang = 2.0

    # Gemiddelde bepalen
    avg = float(df.mean(axis=0))

    # Lijst van factoren aanmaken (de data is als dict{} of als list[] verkrijgbaar, verander bij return)
    factors_dict = {}
    factors_list = []

    # Voor elk gebied de factor berekenen
    for i in range(len(df)):
        # Percentage jeugd vinden in DataFrame
        procent_jeugd = df.iloc[i, 0]

        # Factor berekenen en toevoegen
        factor = (procent_jeugd / avg) ** belang
        factors_dict[regios[i]] = factor
        factors_list.append(factor)
    return factors_dict
