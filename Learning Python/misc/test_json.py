# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 12:32:27 2018
json
@author: mlingaiah
"""

import json

n = [2, 3, 5, 7, 9, 11]
filename = 'C:/Users/mlingaiah/Desktop/json_test.json'

# Saving data structures to json file
with open(filename, 'w') as fp:
    json.dump(n, fp)

alpha = {'a': 1,
         'b': 2,
         'c': 3,
         'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
         'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15,
         'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21,
         'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26
         }

with open(filename, 'a') as fp:
    json.dump(alpha, fp)

# Loading data from json file
filename = 'C:/Users/mlingaiah/Desktop/json_test.json'

with open(filename, 'r') as fp:
    n_from_json = json.load(fp)

print(n_from_json[-1])

for key, value in alpha.items():
    print('Key ', key.upper())
    print('Value ', value)
    # print('\n')

print(alpha)
