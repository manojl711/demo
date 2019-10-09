# select a pandas Series from a DataFrame
# Pandas have 2 datatypes - dataframe and series
# Series is one column of a dataframe
# Dataframe is table with rows and cols

import pandas as pd

# read_table assumes tab seperated by cols
# ufo = pd.read_table('data/ufo.csv',sep=',')
ufo = pd.read_csv('data/ufo.csv')  # read_csv is the shortcut to read comma seperated values

print('\n')
print(type(ufo))
print(ufo.shape)
print(ufo.head())

# To select a series
print(type(ufo['City']))
print(ufo['City'].head())

# Each column in a dataframe is created as an attribute of that dataframe
# Hence we can access a series using a dor operator
print(type(ufo.City))
print(ufo.City.head())

# How to create a new pandas series (eg. to create a new column that has both City and State
print(ufo.City + ufo.State)
# or for more readability
print(ufo.City + ', ' + ufo.State)

# Now if you think by using dot operator to create a new series, you are wrong
# it will not work
# the below statement gives error
# ufo.Location = ufo.City + ', ' + ufo.State

# For this to work, use [] braces
ufo['Location'] = ufo.City + ', ' + ufo.State
print('\n')
print(ufo.shape)
print(ufo.head())
