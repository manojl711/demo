# id() returns the identity of an object
# In python it a unique id similar to memory address in C

# Two objects with non-overlapping lifetimes may have the same id() value

a = 5
print(id(a))

b = 6
print(id(b))
print(id(a) == id(b))

# b has same address as a
b = a
print(id(b))
print(id(a) == id(b))

p = 'Manoj'
print(id(p))

# Here since the value of q is same as p, the id of q is same (very strange, how python checks data/contents while assinging memory to variables)
q = 'Manoj'
print(id(q))
print(id(p) == id(q))
