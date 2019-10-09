# Scope of variables in Instance and Classes
# Attributes attached to Instances pertain 'ONLY to those SINGLE Instances'
# But, Attributes attached to Classes are 'SHARED by ALL their Subclasses and Instances'
# todo have to check for subclasses

class Test:
    a = 0
    b = 0


I1 = Test()
I2 = Test()

# I1
print('I1 = ', I1.a, I1.b)

# I2
print('I2 = ', I2.a, I2.b)

# Class
print('Test = ', Test.a, Test.b)

# Changing Values of I1
print('After Changing Values of I1')
I1.a = 10
I1.b = 10
print('I1 = ', I1.a, I1.b)
print('I2 = ', I2.a, I2.b)
print('Test = ', Test.a, Test.b)

# Changing Values of I2
print('After Changing Values of I2')
I2.a = 30
I2.b = 30
print('I1 = ', I1.a, I1.b)
print('I2 = ', I2.a, I2.b)
print('Test = ', Test.a, Test.b)

# Changing Values of Test
print('After Changing Values of Test')
Test.a = 1000
Test.b = 1000
print('I1 = ', I1.a, I1.b)
print('I2 = ', I2.a, I2.b)
print('Test = ', Test.a, Test.b)

# Creating new attributes in I1
print('Creating new attributes in I1')
I1.c = 5
I1.d = 5
print('I1 = ', I1.c, I1.d)
# print('I2 = ', I2.c, I2.d)   # We get error
# print('Test = ', Test.c, Test.d) # We get error

# Creating new attributes in I2
print('Creating new attributes in I2')
I2.e = 6
I2.f = 6
# print('I1 = ', I1.e, I1.f)   # We get error
print('I2 = ', I2.e, I2.f)
# print('Test = ', Test.e, Test.f) # We get error


# Creating new attributes in Test
print('Creating new attributes in Test')
Test.p = 700
Test.q = 700
print('I1 = ', I1.p, I1.q)  # We get error
print('I2 = ', I2.p, I2.q)
print('Test = ', Test.p, Test.q)  # We get error


# Lets Try it with same variable names


class Test2:
    a = 0
    b = 0


I3 = Test2()
I4 = Test2()

I3.a = 1
I3.b = 1

I4.a = 2
I4.b = 2

# Same variable a,b has been assigned different values
print('I3 = ', I3.a, I3.b)
print('I4 = ', I4.a, I4.b)
print('Test2 = ', Test2.a, Test2.b)

# Now lets change values in Instances

I3.a = 3
I3.b = 3

I4.a = 4
I4.b = 4

print('I3 = ', I3.a, I3.b)
print('I4 = ', I4.a, I4.b)
print('Test2 = ', Test2.a, Test2.b)

# Now lets change values in Class

Test2.a = 77
Test2.b = 77

print('I3 = ', I3.a, I3.b)
print('I4 = ', I4.a, I4.b)
print('Test2 = ', Test2.a, Test2.b)

# This indicates all 3 (I3, I4 and Test2) are in different namespaces
