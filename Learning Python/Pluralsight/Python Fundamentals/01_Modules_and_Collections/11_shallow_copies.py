a = [[1, 2], [3, 4]]
print('a = {0}'.format(a))
print('id(a) = {0}'.format(id(a)))

# print('Galactic position x = {pos[0]}, y = {pos[1]}, z = {pos[2]}'.format(pos=pos))

print('\nFirst Level')
for i in a:
    print('id({0}) = {1}'.format(i, id(i)))

print('\nSecond Level')
for i in a:
    for j in i:
        print('id({0}) = {1}'.format(j, id(j)))

print('\nShallow Copy, b = a[:]')
b = a[:]

print('b = {0}'.format(b))
print('id(b) = {0}'.format(id(b)))  # this will be different, but all below items in b have same addresses as a's items
print('id(a) is not equal to id(b): id(a) = {0}, id(b) = {1}, a is b = {2}'.format(id(a), id(b), a is b))

# print('Galactic position x = {pos[0]}, y = {pos[1]}, z = {pos[2]}'.format(pos=pos))

print('\nFirst Level')
for i in b:
    print('id({0}) = {1}'.format(i, id(i)))

print('\nSecond Level')
for i in b:
    for j in i:
        print('id({0}) = {1}'.format(j, id(j)))

# the items of a and b have similar addresses
print('id(a[0]) is equal to id(b[0]): id(a[0]) = {0}, id(b[0]) = {1}, a[0] is b[0] = {2}'.format(
    id(a[0]), id(b[0]), a[0] is b[0])
)

# this is true for all items in a and b
# for example
print('id(a[1][1]) is equal to id(b[1][1]): id(a[1][1]) = {0}, id(b[1][1]) = {1}, a[1][1] is b[1][1] = {2}'.format(
    id(a[1][1]), id(b[1][1]), a[1][1] is b[1][1])
)

print('\nHow sometimes replace doesnt affect b value, but append changes the value of b')
# Now lets replace and append few values in a
# replace
a[0] = [8, 9]  # Here b value is not changed
print('Replace: when a[0] = [8,9]')
print('a[0] = {0}, b[0] = {1}'.format(a[0], b[0]))

# append
a[1].append(77)  # Here b value not changed
print('Append: when a[1].append(77)')
print('a[1] = {0}, b[1] = {1}'.format(a[1], b[1]))

print('List a = {0}\nList b = {1}'.format(a, b))
