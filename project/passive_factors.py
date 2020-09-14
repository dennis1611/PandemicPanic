from pandas import read_csv

# Collect Dutch Provinces data including age ranges and population density
prov_data = read_csv('Data_provinces.csv', skiprows=[0, 1, 2, 4], delimiter=";",
                     index_col=0, skipinitialspace=True, decimal=',', skipfooter=1, engine='python')

# Collect Dutch COROP-areas data including age ranges and population density
cor_data = read_csv('Data_corops.csv', skiprows=0, delimiter=";",
                    index_col=1, skipinitialspace=True, decimal=',', skipfooter=1, engine='python')

# Decide which areas you want to use; COROP or Provinces (both work)
data = cor_data

# Remove the first column which includes unneeded information
data = data.iloc[:, 1:]

# Rename columns
data.columns = ['Population', '0 tot 5 (%)', '5 tot 10 (%)', '10 tot 15 (%)', '15 tot 20 (%)', '20 tot 25 (%)',
                '25 tot 45 (%)', '45 tot 65 (%)', '65 tot 80 (%)', '80 tot 120 (%)', 'Density']

# Create an array of region names from the document
regions = data.index.values

# Make a seperate DataFrame for the population counts per area
Populations = data.filter(items=['Population'])

# Function to determine the multiplying factors per region on basis of the population density
def densityfactors(general_dataset):
    df = general_dataset.filter(items=['Density'])

    # IMPORTANCE FACTOR: determines the influence of the density on the amount of infections (higher =  more influence)
    importance = 0.4

    # Calculate the mean density
    avg = float(df.mean(axis=0))

    # Create a list and a dictionary to store the values - to change the output between the two, change the "return"
    factors_dict = {}
    factors_list = []

    # Determine the density factor per region
    for i in range(len(df)):
        # Find the region's density in the DataFrame
        region_density = df.iloc[i, 0]

        # Calculate the factor and add it do the list and dictionary
        factor = (region_density / avg) ** importance
        factors_dict[regions[i]] = factor
        factors_list.append(factor)

    return factors_dict


# Function to determine the multiplying factors per region on basis of the population density
def agefactors(general_dataset):
    # Create the 'Youth' DataFrame that inculdes data regarding citizens between ages 15 and 25
    youth = general_dataset.filter(items=['15 tot 20 (%)', '20 tot 25 (%)'])

    # Make new column that combines the 15 to 20 and 20 to 25 age ranges
    youth["total_youth (%)"] = youth['15 tot 20 (%)'] + youth['20 tot 25 (%)']

    # Make a new DataFrame with only the combined column in it
    df = youth.filter(items=['total_youth (%)'])

    # IMPORTANCE FACTOR: determines the influence of the density on the amount of infections (higher =  more influence)
    importance = 2.0

    # Calculate the average percentage of youth in all regions
    avg = float(df.mean(axis=0))

    # Create a list and a dictionary to store the values - to change the output between the two, change the "return"
    factors_dict = {}
    factors_list = []

    # Determine the age factor per region
    for i in range(len(df)):
        # Find the region's youth percentage in the DataFrame
        percent_youth = df.iloc[i, 0]

        # Calculate the factor and add it to the list and dictionary
        factor = (percent_youth / avg) ** importance
        factors_dict[regions[i]] = factor
        factors_list.append(factor)
    return factors_dict
