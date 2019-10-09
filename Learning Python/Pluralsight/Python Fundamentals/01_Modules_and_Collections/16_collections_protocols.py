# Protocol - Its a set of operations or methods that a type must support if its to implement that protocol
# In other words, To implement a protocol, objects must support certain operations
# Most collections implement container, sized and iterable
# All except set and dict are sequences


# PROTOCOL      Implementing Collections                    Comments
# container     str, list, range, tuple, bytes, set, dict   container protocol requires membership testing in and not in
# sized         str, list, range, tuple, bytes, set, dict   requires len(s)
# iterable      str, list, range, tuple, bytes, set, dict   iter(s) or for loop
# sequence      str, list, range, tuple, bytes              retrive items by index, value. count items and reverse
# Mutable sequence
# Mutable set
# Mutable mapping
