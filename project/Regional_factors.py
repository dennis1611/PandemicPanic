from pandas import read_csv

# Collect Dutch Provinces data including age ranges and population density
prov_data = read_csv('Data_provinces.csv', skiprows=[0, 1, 2, 4], delimiter=";",
                     index_col=0, skipinitialspace=True, decimal=',', skipfooter=1, engine='python')

# Collect Dutch COROP-areas data including age ranges and population density
cor_data = read_csv('Data_corops.csv', skiprows=0, delimiter=";",
                    index_col=1, skipinitialspace=True, decimal=',', skipfooter=1, engine='python')

# Decide which areas you want to use; COROP or Provinces (both work)
data = prov_data

# Data preparation
# Remove the first column which includes unneeded information
data = data.iloc[:, 1:]

# Rename columns
data.columns = ['Population', '0 to 5 (%)', '5 to 10 (%)', '10 to 15 (%)', '15 to 20 (%)', '20 to 25 (%)',
                '25 to 45 (%)', '45 to 65 (%)', '65 to 80 (%)', '80 to 120 (%)', 'Density']

# Create an array of region names from the document
regions = data.index.values

# Make a separate list for the population counts per area
Populations = data['Population'].tolist()

regional_data = data.filter(items=['Population'])


def densityfactors(general_dataset, importance=0.4):
    # Function to determine the multiplying factors per region on basis of the population density
    # IMPORTANCE FACTOR: determines the influence of the density on the amount of infections (higher =  more influence)

    df = general_dataset.filter(items=['Density'])

    # Calculate the mean density
    avg = float(df.mean(axis=0))

    # Create a list and a dictionary to store the values - to change the output between the two, change the "return"
    factors_dict = {}
    factors_list = []

    # Determine the density factor per region
    for j in range(len(df)):
        # Find the region's density in the DataFrame
        region_density = df.iloc[j, 0]

        # Calculate the factor and add it do the list and dictionary
        factor = (region_density / avg) ** importance
        factors_dict[regions[j]] = factor
        factors_list.append(factor)

    return factors_list


def youth_infection_factors(general_dataset, importance=2.0):
    # Function to determine the multiplying factors per region on basis of the population density
    # IMPORTANCE FACTOR: determines the influence of the density on the amount of infections (higher =  more influence)

    # Create the 'Youth' DataFrame that includes data regarding citizens between ages 15 and 25
    youth = general_dataset.filter(items=['15 to 20 (%)', '20 to 25 (%)'])

    # Make new column that combines the 15 to 20 and 20 to 25 age ranges
    youth["total_youth (%)"] = youth['15 to 20 (%)'] + youth['20 to 25 (%)']

    # Make a new DataFrame with only the combined column in it
    df = youth.filter(items=['total_youth (%)'])

    # Calculate the average percentage of youth in all regions
    avg = float(df.mean(axis=0))

    # Create a list and a dictionary to store the values - to change the output between the two, change the "return"
    factors_dict = {}
    factors_list = []

    # Determine the age factor per region
    for j in range(len(df)):
        # Find the region's youth percentage in the DataFrame
        percent_youth = df.iloc[j, 0]

        # Calculate the factor and add it to the list and dictionary
        factor = (percent_youth / avg) ** importance
        factors_dict[regions[j]] = factor
        factors_list.append(factor)
    return factors_list


def senior_death_factors(general_dataset, importance=1.3):
    # IMPORTANCE FACTOR: determines the influence of the density on the amount of deaths (higher =  more influence)

    # Create the 'Seniors' DataFrame that includes data regarding citizens between ages 65 and 120
    seniors = general_dataset.filter(items=['65 to 80 (%)', '80 to 120 (%)'])

    # Make new column that combines the 65 to 80 and 80 to 120 age ranges
    seniors["total_seniors (%)"] = seniors['65 to 80 (%)'] + seniors['80 to 120 (%)']

    # Make a new DataFrame with only the combined column in it
    df = seniors.filter(items=['total_seniors (%)'])

    # Calculate the average percentage of seniors in all regions
    avg = float(df.mean(axis=0))

    # Create a list and a dictionary to store the values - to change the output between the two, change the "return"
    factors_dict = {}
    factors_list = []

    # Determine the senior factor per region
    for j in range(len(df)):
        # Find the region's senior percentage in the DataFrame
        percent_senior = df.iloc[j, 0]

        # Calculate the factor and add it to the list and dictionary
        factor = (percent_senior / avg) ** importance
        factors_dict[regions[j]] = factor
        factors_list.append(factor)
    return factors_list


def total_infectionfactor(general_dataset):
    total_inf_factor = []

    youth = youth_infection_factors(general_dataset)
    density = densityfactors(general_dataset)

    for j in range(len(regions)):
        total_inf_factor.append(youth[j] * density[j])

    return total_inf_factor


def total_deathfactor(general_dataset):
    total_death_factor = []

    seniors = senior_death_factors(general_dataset)

    for j in range(len(regions)):
        total_death_factor.append(seniors[j])

    return total_death_factor


# Create final DF with all regional data
columns_names = ['death_factor', 'inf_factor']
datasets = [total_deathfactor(data), total_infectionfactor(data)]

for i in range(len(datasets)):
    regional_data.insert(1, columns_names[i], datasets[i])

# generate a csv file in the same directory based on regional_data
regional_data.to_csv('regional_data.csv')
