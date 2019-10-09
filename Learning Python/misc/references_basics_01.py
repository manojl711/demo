# Address and its contents
# Pointers * and & in C
# Address = id(var_name)
# Contents = first import ctypes and then print(ctypes.cast(id(var_name), ctypes.py_object).value)

x = 42
print(x, id(x))
y = 50
print(y, id(y))
x = y
print(x, y, id(x), id(y))
y = [1, 2, 3]
print(x, y, id(x), id(y))


class ABC:
    p = 1
    q = 2
    r = 'Manoj'
    pass


a = ABC()
print(a, ABC)
print(id(ABC), id(a))
print(id(ABC), id(a.p), id(a.q), id(a.r))
print(id(ABC), id(ABC.p), id(ABC.q), id(ABC.r))
ABC.p = 10
a.p = 5
print(id(ABC), id(a.p), id(a.q), id(a.r))
print(id(ABC), id(ABC.p), id(ABC.q), id(ABC.r))

foo = 1
bar = foo
baz = bar
fii = 1

print(id(foo))
print(id(bar))
print(id(baz))
print(id(fii))

import ctypes

a = 300
print(id(a))
print(ctypes.cast(id(a), ctypes.py_object).value)
