# Finding elements - using index or by item
# Counting elements
# Test membership or for non-membership
# Remove elements using del (uses index) and remove (uses value)
# Insert item to a list
# Convert List to Strings
# Concatenating of List (In place extension) +, += and extend
# Reversing and Sorting a List
# Sort using key
# Use of sorted()
# Use reversed(), this returns an iterator

###################################################################


# Finding elements - using index or by item
# index(item)
print('\nIndexing')
w = "The quick brown fox jumps over the lazy dog".split()
print(w)
print("w.index('fox')")
i = w.index('fox')
print('Index of fox is ', i)

print('\nCounting')
# Counting elements
c = w.count('the')
print("w.count('the')")
print('Count of word the is ', c)

print('\nMembership')
# Test membership or for non-membership
print('37 in [1,78,9,37,88,43] ', 37 in [1, 78, 9, 37, 88, 43])
print('78 not in [1,78,9,37,88,43] ', 78 not in [1, 78, 9, 37, 88, 43])

print('\nRemoving Elements')
# Remove elements using del (uses index) and remove (uses value)
# using del
# del seq[index]
w = "The quick brown fox jumps over the lazy dog".split()
print(w)
print('del w[3]')
del w[3]
print(w)

# using remove
# seq.remove(item)
w = "The quick brown fox jumps over the lazy dog".split()
print("w.remove('fox')")
w.remove('fox')
print(w)

# del uses index to remove, remove uses item
# equivalent of remove using del is
# del seq[seq.index(item)]
w = "The quick brown fox jumps over the lazy dog".split()
print("del w[w.index('fox')]")
del w[w.index('fox')]
print(w)

print('\nInserting Elements')
# Insert item to a list
# seq.insert(index, item)
i = "I accidentally the whole universe".split()
print(i)
print("i.insert(2,'destroyed')")
i.insert(2, 'destroyed')
print(i)

print('\nConvert List to Strings')
# Convert List to Strings
i = "I accidentally the whole universe".split()
print(i)
print("i = ' '.join(i) ")
i = ' '.join(i)  # Use blank to concatenate to get a sentence
print(i)

print('\nConcatenation')
# Concatenating of List (In place extension) +, += and extend
# Remember, concatenation will not result in 2 lists present inside a single list
# Concatenation will result in one single list

# + results in new list
m = [1, 2, 3]
n = [4, 5, 6]
c = m + n
# will not yield in [[1, 2, 3],[4, 5, 6]]
# but will result in [1,2,3,4,5,6]

print(c, m, n)

# += modifies the assignee in-place
c += [11, 22, 33]
print(c)

# extend is similar to +=
c.extend([55, 66, 77])
print(c)

print('\nReverse and Sort')
# Reversing and Sorting a List
# k.reverse() - reverses in-place
a = [4, 3, 5, 6, 2, 7, 1, 0, 9, 8]
a.reverse()
print(a)

# k.sort() - sorts in-place
a.sort()
print(a)

print('\nSort using Key')
# Sort using key
h = 'not perplexing do handwriting family where I illegibly know doctors'.split()
print(h)
print("h.sort(key=len)")  # here lists are ordered w.r.t length
h.sort(key=len)
print(h)
print("h.sort(reverse=True)")
h.sort(reverse=True)
print(h)  # see the first char of the word

print('\nSorted and Reversed')
# Use of sorted() - This sorts any iterable series and returns a list
x = [4, 9, 2, 1]
print(x)
print("y = x.sorted()")
y = sorted(x)
print(x, y)

# Use reversed(), this returns a reverse iterator
print("y = x.sorted()")
y = reversed(x)  # this gives iterator and not a list
print(x, y)

# to evaluate a reverse iterator use list constructor
y = list(y)
print(y)
