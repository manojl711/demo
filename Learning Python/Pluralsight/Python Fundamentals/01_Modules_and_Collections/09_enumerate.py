# usualy range is used for list
# eg.
for i in range(5):
    print(i)

# for some reason, when we need a counter - we should use enumerate()
# this returns iterable series of pairs - each pair being a tuple
# first pair is index, second is the item
# enumerate, yields (index,value) tuples

t = [6, 7, 913, 113121, 9389102.12121]
for p in enumerate(t):
    print(p)

# using tuple unpacking
for i, v in enumerate(t):
    print('i = {}, v = {}'.format(i, v))
