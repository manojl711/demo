# tuple can contain nested tuples
s = ((1, 2), (3, 4), (5, 6))
print(s)
print(s[1])
print(s[0][1])

# Sometimes tuple can contain a single element
# When tuple has only one element its considered as int or string but not as tuple

t = (5)
print(type(t))

t = ('manoj')
print(type(t))

# To avoid being wrongly assigned to different types
# use comma at the end (trailing comma separator)

t = (5,)
print(type(t))

t = ('manoj',)
print(type(t))

# for empty tuple, just use empty parenthesis
t = ()
print(type(t))

# in some cases even the parenthesis are omitted
t = 1, 2, 3, 4, 5, 6
print(t)
print(type(t))


# here we will show tuple unpacking.
# returning multiple values as tuple is often used
# its collected using destructing operation, this allows us to unpack data structures into named references

def minmax(items):
    return min(items), max(items)  # returning multiple values as tuple


print(minmax([1, 2, 3, 4, 5, 6, 7]))

lower, upper = minmax([1, 2, 3, 4, 5, 6, 7])  # destructing operation
print(lower, upper)

# Python's idiomatic swap uses tuple unpacking technique:)

a = 5
b = 6
print(a, b)

a, b = b, a  # Python's idiomatic swap
print(a, b)

# tuple(iterable) constructor - used to create tuples from iterable series of objects

# from list to tuple
t = tuple([1, 2, 3, 4, 5, 6, 7])  # using 'tuple' constructor to create a tuple
print(t)

# from str to tuple
t = tuple('Michael Jackson')  # using 'tuple' constructor to create a tuple
print(t)
