import time


def banner(message, border='-'):
    line = border * len(message)
    print(line)
    print(message)
    print(line)


# Default positional parameters - Always use it
# By using positional parameters, we can change the order of passing arguments

banner('This is python', '%')
banner('Magic is magic', '#')
banner(border='.', message='My name is Manoj')


# Remember default arguments are set only once
# We can see this with current time as default parameter

def show_default(arg=time.ctime()):
    print(arg)


# Here we can see the seconds/time is not changed
show_default()
time.sleep(3)
show_default()


def add_spam(menu=[]):
    menu.append('spam')
    return menu


# Here the empty menu list created once. Every add_spam call is appending spam to the already created empty list
# The list is not getting empty with every function call
print(add_spam())
print(add_spam())
print(add_spam())
print(add_spam())


# To fix this, we need to manually empty the list using None
# Or always use a immutable objects such as integers or strings as default values
# We are using None object as a Sentinel (Guard)
def add_spam2(menu=None):
    if menu is None:
        menu = []
    menu.append('spam')
    return menu


print('add_spam2')
print(add_spam2())
print(add_spam2())
print(add_spam2())
print(add_spam2())
