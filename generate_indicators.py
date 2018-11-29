import pandas
import numpy

# Create the framework
years = [ y for y in range(1980, 2014) ]
OECD = ['Australia', 'Austria', 'Belgium', 'Canada', 'Chile', 'Czech Republic',
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Iceland', 'Ireland', 'Israel', 'Italy', 'Japan', 'Latvia', 'Lithuania',
        'Luxembourg', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland',
        'Portugal', 'Slovakia', 'Slovenia', 'South Korea', 'Spain', 'Sweden',
        'Switzerland', 'Turkey', 'United Kingdom', 'United States']

dataset = pandas.DataFrame(columns = years, data = numpy.zeros( (len(OECD), len(years)) ))
dataset.insert(0, "Country", OECD)

dataset = pandas.melt( dataset, id_vars = ["Country"], var_name = "Year", value_name = "Zero" )
dataset = dataset.drop("Zero", axis = 1)

# Add EU membership

_1958 = ['Belgium', 'France', 'Germany', 'Italy', 'Luxembourg', 'Netherlands']
_1973 = ['Denmark', 'Ireland', 'United Kingdom']
_1981 = ['Greece']
_1986 = ['Portugal', 'Spain']
_1995 = ['Austria', 'Finland', 'Sweden']
_2004 = ['Cyprus', 'Czechia', 'Estonia', 'Hungary', 'Latvia', 'Lithuania', 'Malta', 'Poland', 'Slovakia', 'Slovenia']
_2007 = ['Bulgaria', 'Romania']
_2013 = ['Croatia']

eu_membership = dataset[ ( dataset["Country"].isin(_1958) ) ]
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_1973) ) ] ] )
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_1981) ) ] ] )
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_1986) ) & ( dataset["Year"] > 1985 ) ] ] )
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_1995) ) & ( dataset["Year"] > 1994 ) ] ] )
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_2004) ) & ( dataset["Year"] > 2003 ) ] ] )
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_2007) ) & ( dataset["Year"] > 2006 ) ] ] )
eu_membership = pandas.concat( [ eu_membership, dataset[ ( dataset["Country"].isin(_2013) ) & ( dataset["Year"] > 2012 ) ] ] )

eu_membership.insert(2, "EU", [1 for i in range( eu_membership.shape[0] )] )

# Add Eurozone membership

_1999 = ['Austria', 'Belgium', 'Finland', 'France', 'Germany', 'Ireland', 'Italy', 'Luxembourg', 'Netherlands', 'Portugal', 'Spain']
_2001 = ['Greece']
_2007 = ['Slovenia']
_2008 = ['Cyprus', 'Malta']
_2009 = ['Slovakia']
_2011 = ['Estonia']
_2014 = ['Latvia']
_2015 = ['Lithuania']

euro_membership = dataset[ ( dataset["Country"].isin(_1999) ) & ( dataset["Year"] > 1998) ]
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2001) ) & ( dataset["Year"] > 2000 ) ] ] )
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2007) ) & ( dataset["Year"] > 2006 ) ] ] )
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2008) ) & ( dataset["Year"] > 2007 ) ] ] )
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2009) ) & ( dataset["Year"] > 2008 ) ] ] )
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2011) ) & ( dataset["Year"] > 2010 ) ] ] )
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2014) ) & ( dataset["Year"] > 2013 ) ] ] )
euro_membership = pandas.concat( [ euro_membership, dataset[ ( dataset["Country"].isin(_2015) ) & ( dataset["Year"] > 2014 ) ] ] )

euro_membership.insert(2, "Euro", [1 for i in range( euro_membership.shape[0] )] )

# Add Schengen membership

_1995 = ['Belgium', 'France', 'Germany', 'Luxembourg', 'Netherlands', 'Portugal', 'Spain']
_1997 = ['Italy', 'Austria']
_2000 = ['Greece']
_2001 = ['Denmark', 'Finland', 'Iceland', 'Norway', 'Sweden']
_2007 = ['Czech Republic', 'Estonia', 'Hungary', 'Latvia', 'Lithuania', 'Malta', 'Poland', 'Slovakia', 'Slovenia']
_2008 = ['Switzerland']
_2011 = ['Liechtenstein']

schengen_membership = dataset[ ( dataset["Country"].isin(_1995) ) & ( dataset["Year"] > 1994) ]
schengen_membership = pandas.concat( [ schengen_membership, dataset[ ( dataset["Country"].isin(_1997) ) & ( dataset["Year"] > 1996 ) ] ] )
schengen_membership = pandas.concat( [ schengen_membership, dataset[ ( dataset["Country"].isin(_2000) ) & ( dataset["Year"] > 1999 ) ] ] )
schengen_membership = pandas.concat( [ schengen_membership, dataset[ ( dataset["Country"].isin(_2001) ) & ( dataset["Year"] > 2000 ) ] ] )
schengen_membership = pandas.concat( [ schengen_membership, dataset[ ( dataset["Country"].isin(_2007) ) & ( dataset["Year"] > 2006 ) ] ] )
schengen_membership = pandas.concat( [ schengen_membership, dataset[ ( dataset["Country"].isin(_2008) ) & ( dataset["Year"] > 2007 ) ] ] )
schengen_membership = pandas.concat( [ schengen_membership, dataset[ ( dataset["Country"].isin(_2011) ) & ( dataset["Year"] > 2010 ) ] ] )

schengen_membership.insert(2, "Schengen", [1 for i in range( schengen_membership.shape[0] )] )

# Merge, and Replace Nan with 0
dataset = pandas.merge( dataset, eu_membership, on = ["Country", "Year"], how="outer" )
dataset = pandas.merge( dataset, euro_membership, on = ["Country", "Year"], how="outer" )
dataset = pandas.merge( dataset, schengen_membership, on = ["Country", "Year"], how="outer" )

dataset = dataset.fillna(0)

# Export
dataset.to_csv("Unaltered Data/Membership_Indicators.csv")
