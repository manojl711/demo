# Python name scopes
# LEGB - Local, Enclosing, Global and Built-ins module
# for loops, with-blocks do not introduce new nested scopes

count = 0


def show_count():
    print(count)


def set_count(c):
    count = c


# Here the value of the count is not changed
# count in set_count is local to set_count function
# count in show_count refers to global, and it will be always 0
show_count()
set_count(10)
show_count()


# To fix this assign count var in set_count function to global using global keyword
def set_count2(c):
    global count
    count = c


set_count2(10)
show_count()
