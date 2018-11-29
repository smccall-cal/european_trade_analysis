import pandas
import numpy

# Load the IMF trade dataset
dataset = pandas.read_csv("Unaltered Data/IMF DOTS.csv")

# Restrict the dataset to relevant, and consistent, metric
measurement_of_interest = "Goods, Value of Exports, Free on board (FOB), US Dollars"            # Since we're interested in exports
dataset = dataset[ dataset["Indicator Name"] == measurement_of_interest ]                       # Filter the dataset
dataset = dataset[ dataset["Attribute"] == "Value" ]                                            # Filter the dataset

# Restrict the dataset to relevant time period
columns = list( dataset.columns )
columns = [ col for col in columns if ('M' in col) and (col > '1980') and (col < '2013') ]      # 396 months, from Jan 1980 to Dec 2013, inclusive
columns = ['Country Name', 'Counterpart Country Name'] + columns                                # Adds back identificatory information

cleaned = {}
for col in columns:
    cleaned[ col ] = dataset[ col ]

dataset = pandas.DataFrame(data = cleaned)                                                      # Faster than dropping all the irrelvant columns
dataset = dataset.rename(index = str, columns = {"Country Name" : "Exporter", "Counterpart Country Name" : "Importer"})

# Save progress (protect against crashing)
dataset.to_csv("IMFDOTS_Progress.csv")

# Restrict the dataset to relevant countries (OECD exporters)
OECD = ['Australia', 'Austria', 'Belgium', 'Canada', 'Chile', 'Czech Republic',                 # List from the OECD website
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Iceland', 'Ireland', 'Israel', 'Italy', 'Japan', 'Latvia', 'Lithuania',
        'Luxembourg', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland',
        'Portugal', 'Slovakia', 'Slovenia', 'South Korea', 'Spain', 'Sweden',
        'Switzerland', 'Turkey', 'United Kingdom', 'United States']

dataset = dataset[ dataset["Exporter"].isin(OECD) ]                                             # All exporting countries (i) are in OECD
dataset = dataset[ dataset["Importer"].isin(OECD) ]                                             # All exporting and importing countries (i, j) are in OECD

# Rearrange for standard Stata format ( i, j, t ) indexing
dataset = pandas.melt(dataset, id_vars = ["Exporter", "Importer"], var_name = "Month", value_name = "Export Vol")
dataset.insert(2, "Year", dataset["Month"])

dataset["Year"] = dataset["Year"].apply( lambda s: int( s[:4] ) )
dataset["Month"] = dataset["Month"].apply( lambda s: int( s[5:] ) )

# Save progress (protect against crashing)
dataset.to_csv("IMFDOTS_Progress.csv")

# Merge in indicator (explanatory) variables
indicators = pandas.read_csv("Unaltered Data/Membership_Indicators.csv")
indicators = indicators.drop("Unnamed: 0", axis = 1)

exporter_i = indicators.rename(index = str, columns = {"Country" : "Exporter", "Schengen" : "Schengen EX", "Euro" : "Euro EX", "EU": "EU EX"} )
importer_i = indicators.rename(index = str, columns = {"Country" : "Importer", "Schengen" : "Schengen IM", "Euro" : "Euro IM", "EU": "EU IM"} )

dataset = pandas.merge(dataset, exporter_i, on=["Exporter", "Year"], how = "inner")
dataset = pandas.merge(dataset, importer_i, on=["Importer", "Year"], how = "inner")

# Save progress (protect against crashing)
dataset.to_csv("IMFDOTS_Progress.csv")

# Unilateral control Variables
controls = pandas.read_csv("Unaltered Data/OECD.csv")

# Fix units
true_values = controls["Value"] * ( 10 ** controls["PowerCode Code"] )                          # Adjust for differences in units
controls["Value"] = true_values

# Rearrange OECD controls
population = controls[ controls["Subject"] == "Population levels" ]
GDP_capita = controls[ controls["Subject"] == "GDP per capita" ]

population = population.rename(index = str, columns = {"Value": "Population Levels"})
GDP_capita = GDP_capita.rename(index = str, columns = {"Value": "Real GDP Per Capita"})

controls = pandas.merge(population, GDP_capita, on=["Country", "Year"], how = "outer")

# Remove Extraneous Columns
columns = ['Country', 'Year', "Population Levels", "Real GDP Per Capita_x" ]

cleaned = {}
for column in columns:
    cleaned[ column ] = controls[ column ]

controls = pandas.DataFrame(data = cleaned)                                                    # Faster than dropping all the irrelvant columns

# Merge the unilateral controls into the dataset
exporter_controls = controls.rename(index = str, columns = {"Country" : "Exporter", "Population Levels" : "Population EX", "Real GDP Per Capita_x": "RGDPcapita EX"} )
importer_controls = controls.rename(index = str, columns = {"Country" : "Importer", "Population Levels" : "Population IM", "Real GDP Per Capita_x": "RGDPcapita IM"} )

dataset = pandas.merge( dataset, exporter_controls, on=["Exporter", "Year"], how = "inner" )
dataset = pandas.merge( dataset, importer_controls, on=["Importer", "Year"], how = "inner" )

# Finally, restrict to complete data
dataset = dataset.dropna()
dataset = dataset.drop_duplicates()
# Export the dataset(s)
dataset.to_csv("IMFDOTS_OECD.csv")

"""
dataset = pandas.read_csv("IMFDOTS_Progress.csv")
dataset = dataset.drop( "Unnamed: 0", axis = 1)
"""
