# Why do some pandas commands end with parentheses (and others don't)

import pandas as pd

movies = pd.read_csv('http://bit.ly/imdbratings')  # read_csv is the shortcut to read comma separated values

print(movies.head())

print(movies.sort_values(['genre', 'content_rating', 'duration'], ascending=['False', 'True', 'False'], inplace=True))

print(movies[['genre', 'content_rating', 'duration']].head())
