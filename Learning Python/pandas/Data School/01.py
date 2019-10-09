# Pandas - Python Library for
# Data Analysis
# Data Manipulation
# Data Visualization

# Read Tabular data into pandas
import pandas as pd

orders = pd.read_table('data/chipotle.tsv')
print('\n')
print(orders.shape)
print(orders.head())

# movie_users = pd.read_table('http://bit.ly/movieusers')  Read data from URL
movie_users = pd.read_table('data/u.user')
print('\n')
print(movie_users.shape)
print(movie_users.head())

# How to seperate data into different cols
movie_users = pd.read_table('data/u.user', sep='|')
print('\n')
print(movie_users.shape)
print(movie_users.head())  # Its considering 1st row as Header

# How to tell there are no headers
movie_users = pd.read_table('data/u.user', sep='|', header=None)
print('\n')
print(movie_users.shape)
print(movie_users.head())  # Default numbers are used as headers

# How to assign headers
user_cols = ['user_id', 'age', 'gender', 'occupation', 'zipcode']
movie_users = pd.read_table('data/u.user', sep='|', header=None, names=user_cols)
print('\n')
print(movie_users.shape)
print(movie_users.head())  # Default numbers are used as headers
