# tuple - heterogeneous immutable sequence
# list - heterogeneous mutable sequence

# list(iterable) constructor - used to create list from iterable series of objects
# from str to list
t = list('Michael Jackson')  # using 'list' constructor to create a list
print(t)

# trailing comma - important maintainability feature
a = [5]
print(type(a))

a = [5, ]  # Used in Django settings file
print(type(a))

# negative indexing
# always use -ve indexing instead of seq[len(seq-1)]
# -ve 0 and 0 indexing are same
pangram = 'pack my box with five dozens of liquor jugs'
words = pangram.split()
print(words)
print(words[0], words[-0], words[-1], words[-3])

# slicing
# slice = seq[start: stop]
# here 'stop' is not included
print(words[0:4])
print(words[-4:-1])

# Note: start and stop are optional
print(words[:4])
print(words[4:])

# This is called Half-open ranges
# Half open ranges gives complementary slices
# s[:x] + s[x:] == s

# Omitting start and stop gives full slice
# full_slice = seq[:]
print(words[:])

# This seq[:] is an important idiom for Copying Lists
full_slice = words[:]
print(full_slice is words)  # contains different addresses
print(full_slice == words)  # contains same data

# There are other methods of copying a list
# Full Slice > t = seq[:]
# copy() method > u = seq.copy()
# list() constructor > v = list(seq)


# using copy()
u = words.copy()
print(u)

# using list()
v = list(words)  # this is best method as we can pass any iterable series as source and not just list
print(v)

# All these techniques of copy are Shallow copies
# Shallow Copy means - They create a new list containing
# the same object references as the source list
# but dont copy the referred to objects

print(v is words)
print(v == words)
v.append('Manoj')
print(words)
print(v)
