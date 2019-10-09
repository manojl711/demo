# list repetition - Repeats the list
# s = [constant] * size
# Most often used in initializing a list of known size  with a constant
# Remember, List repetition is Shallow!!
# Multiple references to one instance of the constant in the produced list
# In other words, repetition will repeat the references without copying the value.

c = [21, 37]
d = [[0, 1]]  # this is list within a list

r = c * 4
print(r)

r = d * 9
print(r)

print('r[0] is r[1] is r[2] is r[3] is r[8] is r[-1] = {0}'.format(r[0] is r[1] is r[2] is r[3] is r[8] is r[-1]))

# Now append an item in one of the element in r
# this will be reflected in all the repetition
r[5].append(77)
print(r)
print('r[0] is r[1] is r[2] is r[3] is r[8] is r[-1] = {0}'.format(r[0] is r[1] is r[2] is r[3] is r[8] is r[-1]))
