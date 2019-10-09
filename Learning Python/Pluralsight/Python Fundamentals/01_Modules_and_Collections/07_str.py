# strings can be concatenated with just a space separator
a = 'abc' 'efg'
print(a)

# when concatenating multiple strings, its better to use join
# because its more efficient

# always join using a delimiter, later it will be easy to separate them
colors = ';'.join(['red', 'blue', 'green', 'yellow'])
print(colors)
colors = colors.split(';')
print(colors)

# using empty seperator in join can be used to convert list to strings
mywords = ['high', 'way', 'police', 'car']
print(''.join(mywords))

# partition is used to seperate
# it divides into 3 parts: prefix, separator, suffix
print('unforgetable'.partition('forget'))

# partition is used in tuple unpacking
departure, separator, arrival = "London:Edinburgh".partition(':')
print(departure, separator, arrival)

# we can use '_' underscore as a dummy/unused variable for separator
origin, _, destination = 'Bengaluru:Mysuru'.partition(':')
print(origin, _, destination)

# using format string
pos = (65.2, 32.1, 44.9)
pos2 = (33.1, 0.5, 110)
print('Galactic position x = {pos[0]}, y = {pos[1]}, z = {pos[2]}'.format(pos=pos))
print('Galactic position x = {pos[0]}, y = {pos[1]}, z = {pos[2]}'.format(pos=pos2))

import math

print('Math constants: pi = {m.pi}, e = {m.e}'.format(m=math))

phonetic = dict(a='alpha', b='bravo', c='charlie', d='delta', e='echo', f='foxtrot')
for key, value in phonetic.items():
    print('{key} => {item}'.format(key=key, item=value))
