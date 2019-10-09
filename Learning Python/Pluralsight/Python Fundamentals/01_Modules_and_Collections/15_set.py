# set - its an unordered collection of unique, immutable objects
# its similar to dict but here each item is a single object
p = {1, 2, 3, 4, 7}
print(type(p))
print(p)

# to create empty set use set() constructor
# s = {} will create empty dict and not empty set
s = {}
print(type(s))
s = set()
print(type(s))

# In set duplicates are discarded, its commonly used to remove duplicates
s = set('MADAM')
print(s)

# sets are iterable, but order is arbitrary just like dict
s = {14, 8, 12, 20, 0, 3, 5}
for i in s:
    print(i)

# Membership are the fundamental operation of the set (in and not in)
s = {14, 8, 12, 20, 0, 3, 5}
print(14 in s)
print(15 in s)
print(33 not in s)
print(20 not in s)

# Adding elements add(item) - This inserts single item
k = {81, 104}
k.add(50)
print(k)

# Multiple elements are added using update() method
k.update([3, 4, 5, 6])
print(k)

# Removing elements
# remove(item) - requires item to be present, else raises KeyError
k.remove(5)
print(k)
# discard(item) - always succeeds
k.discard(2000)
print(k)

# Copying - s.copy() method
f = k.copy()
print(f)
# or we can use set() constructor
g = set(f)
print(g)
# Its a shallow copy

# Set Algebra
# People with various phenotypes
blue_eyes = {'Olivia', 'Harry', 'Lily', 'Jack', 'Amelia'}
blond_hair = {'Harry', 'Jack', 'Amelia', 'Mia', 'Joshua'}
smell_hcn = {'Harry', 'Amelia'}
taste_ptc = {'Harry', 'Lily', 'Amelia', 'Lola'}
o_blood = {'Mia', 'Joshua', 'Lily', 'Olivia'}
b_blood = {'Amelia', 'Jack'}
a_blood = {'Harry'}
ab_blood = {'Joshua', 'Lola'}

# Union - s.union(t) - commutative
print(blue_eyes.union(blond_hair))
print(blue_eyes.union(blond_hair) == blond_hair.union(blue_eyes))

# Intersection - s.intersection(t) - commutative
print(blue_eyes.intersection(blond_hair))
print(blue_eyes.intersection(blond_hair) == blond_hair.intersection(blue_eyes))

# Difference - s.difference(t) - non commutative
# A - B != B - A
blond_hair.difference(blue_eyes)
print(blond_hair.difference(blue_eyes) == blue_eyes.difference(blond_hair))

# Symmetric Difference - s.symmetric_difference(t) - commutative
# Its inverse of Intersection
blond_hair.symmetric_difference(blue_eyes)
print(blond_hair.symmetric_difference(blue_eyes) == blue_eyes.symmetric_difference(blond_hair))


# 3 predicate methods are provided in sets
# These tells us about the relationships between sets
# Subset - s.issubset(t)
print(smell_hcn.issubset(blond_hair))


# Superset - s.issuperset(t)
print(taste_ptc.issuperset(smell_hcn))


# Disjoint - s.isdisjoint(t)
print(a_blood.isdisjoint(o_blood))

# Sets can be used to build elegant solutions
