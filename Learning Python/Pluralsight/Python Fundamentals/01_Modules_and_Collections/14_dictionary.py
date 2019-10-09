# dict - its an unordered mapping from unique, immutable keys  to mutable keys
# it contains comma separated key values pairs
# values are accessed by keys
# keys must be unique
# Internally dictionary maintains pairs of references to the key objects and value objects

# Create dict
# Using dict() constructor
# dict() constructor accepts iterable series of key-value (2 tuples)
names_and_ages = [('Manoj', 34), ('Neeraj', 31), ('Rashmi', 29), ('Kushaal', 2)]
d = dict(names_and_ages)
print(d)

# Create dict using keyword arguments passed into dict()
phonetic = dict(a='alpha', b='bravo', c='charlie', d='delta', e='echo', f='foxtrot')
print(phonetic)

# Copying dict
# dict copy is shallow by default
# copy using copy() method - d.copy()
d = dict(red=123, blue=456, green=789)
e = d.copy()
print(d, e)

# pass existing dict to dict() constructor - This is the commonly used technique to copy a dict
# dict(d)
f = dict(e)
print(f, e)

# Extend or updating a dict with definitions from another dictionary
# Use update() method, by passing the content of the dict which is to be merged in
g = dict(yellow=111, cyan=222)
f.update(g)
print(f)

# Inserting duplicate values - Duplicates are replaces the values
dup = dict(red='rrr', blue=456, black=000)
f.update(dup)
print(f)

# dict Iteration
# color (entire dict) - Get corresponding value with square bracket operator - d[key]
colors = dict(red='rrr', blue=456, green=789, yellow=111, cyan=222, black=0)
for key in colors:
    print('{key} => {value}'.format(key=key, value=colors[key]))

# color.values() - Iteration using values - d.values()
# Here there is no efficient way to retrieve a key froma a value
# so we print only values
for value in colors.values():
    print('{value}'.format(value=value))

# colors.keys() - Iteration using keys - d.keys()
# this not often used, as defalut iteration of dict is by key
for key in colors.keys():
    print('{key} => {value}'.format(key=key, value=colors[key]))

# color.items() - Iteration using both keys and values - key, values and d.items()
# often this method is used
for key, value in colors.items():
    print('{key} => {value}'.format(key=key, value=value))

# Membership - in and not in operators, Only work on keys
print('red' in colors)
print('white' in colors)
print('pink' not in colors)

# Removal - del d[key]
colors = dict(red='rrr', blue=456, green=789, yellow=111, cyan=222, black=0)
del colors['green']
print(colors)

# Mutability - Keys are immutable, but values are immutable. Note: Dict itself is mutable
m = {'H': [1, 2, 3],
     'He': [3, 4],
     'Li': [6, 7],
     'Be': [10, 11]}
print(m)
m['H'] += [4, 5, 6, 7]  # here dict is not modified, but list is being extended
print(m)

# We can add new items to dict
m['C'] = [11, 12, 14, 13]
print(m)

# Pretty Printing - pprint
# Be careful not to rebind the module reference!
# Remember! If we didnt bind the pprint funciton to a different name pp,
# then the function reference would overwrite the module reference
# preventing further access to contents of the module
# Arguably its a poor design to have a module containing functions of the same name

from pprint import pprint as pp

pp(m)
