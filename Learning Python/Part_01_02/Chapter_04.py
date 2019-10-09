import math
import random
import re

print('Python Objects or Core Datatypes: 15 types')
print('\nNumbers, Strings, Lists, Dictionaries, Tuples')
print('Files, Sets, Boolean, Types, None')
print('Functions, Modules, Classes, Compiled Codes, Stack Tracebacks')

print('\nNumbers')
print('Exponentiation: **, 2**100 = ', 2 ** 100)
print('How many digits in really big number len(str(2**10000)) = ', len(str(2 ** 10000)))
print('\n** Note: Here nested call, works from inside out **')

print('\nFew important modules related to Numbers')
print('\nimport math')
print('math.pi = ', math.pi)
print('math.sqrt(77) = ', math.sqrt(77))

print('\nimport random')
print('random.random() = ', random.random())
print('random.choice([1,2,3,4,5]) = ', random.choice([1, 2, 3, 4, 5]))
print('random.choice([1,2,3,4,5]) = ', random.choice([1, 2, 3, 4, 5]))

print('\nStrings')
print('s = "spam"')
s = 'spam'
print(s, len(s))
print('\nIndexing - Its used to fetch components in a string.')
print('It starts from zero')
print('s[2], s[3], s[0], s[1] = ', s[2], s[3], s[0], s[1])
print('Backward Indexing - Use negative index')
print('s[-2], s[-3], s[-0], s[-1], s[-4] = ', s[-2], s[-3], s[-0], s[-1], s[-4])

print('\nSlicing (Substring) - Indexing using offsets')
print('General form of Slicing = X[I:J]')
print('** Note: Give me everything in X from offset I up to but NOT INCLUDING offset J **')
print('s[1:3] = ', s[1:3])

print('\nDefault values - Left bound is zero and Right bound is len(s)')
print('s[1:], s[0:3], s[:3], s[:-1], s[:] = ', s[1:], s[0:3], s[:3], s[:-1], s[:])
print('** Note: Slicing will be used in LISTS **')

print('\nConcatenation & Repetition')
print('s * 8 = ', s * 8)
print('s + "xyz" = ', s + "xyz")
print('** Note: This is Polymorphism in effect **')

print('\nImmutability')
print('Once strings are created, they cannot be changed in place')
print('Every string operation is defined to produce a new string as its result')
print('s[0] = "z", This will give error')

print('\n** Note: But you can always build a new string and assign it to the same name **')
print('s = "z" + s[:1] , we can make new objects')
s = "z" + s[:1]
print(s)

print('\nEvery python object is classified as Mutable or Immutable')
print('Immutable - numbers, strings, tuples')
print('Mutable - list, dictionaries, sets')

print('\nConvert/Expand string to list')
s = 'spam'
print('L = list(s)')
L = list(s)
print(L)

print('\nConvert/Join list to sting')
print("''.join(L) - Join with empty delimiter")
str = ''.join(L)
print(str)
print("'++'.join(L)")
str = '++'.join(L)
print(str)

print('\nBytearray - This supports inplace changes for text')
print("B = bytearray(b'spam') - Declaration")
B = bytearray(b'spam')
print(B)
print('Printing B will not return spam, it returns integers')
print('** Note: Bytearray is MUTABLE sequence of INTEGERS')

print('\nLets print individual characters, it returns ascii values just like c language')
print('B[0], B[1], B[2], B[3] = ', B[0], B[1], B[2], B[3])
print('This enables us to make inplace changes for text (create mutable strings)')
print("Changing first character of bytearray and printing B\nB[0] = 116")
B[0] = 116
print(B)

print('\nTo get ascii value of a character - Use ord(c) ')
print("ord('s'),ord('p'),ord('a'),ord('m') = ", ord('s'), ord('p'), ord('a'), ord('m'))

print('\nPrinting original characters and not ascii values - Use decode')
print('B.decode()')
print(B.decode())

print('\nAll datatypes/objects have their own methods/functions')
print('These functions are ATTACHED to and ACT upon a specific object')
print('These are triggered with a CALL expression')
print('eg. find method and replace method')

print('\nFind and Replace')
print('find - returns offset of the passed-in substring, or -1 if its not present')
print('obj.find("substring")')
print("s.find('am') = ", s.find('am'))
print("s.find('ma') = ", s.find('ma'))

print("\ns.replace('pa','XYZ') = ", s.replace('pa', 'XYZ'))

print('\nFew other functions - split(), upper(), isalpha(), rstrip() ')
line = 'aaaaa,bbbb,ccc,ddd\n'
print("line = ", line)
print("line.split(',') line.upper() line.isalpha() line.rstrip()", line.split(','), line.upper(), line.isalpha(),
      line.rstrip())

print("\nWe can COMBINE multiple operations/function calls")
print('**Note - Python always runs from LEFT to RIGHT **')
print("\nline.rstrip().upper().split(',') = ", line.rstrip().upper().split(','))
print('Here first the string is stripped, converted to uppercase and then its split')

line = 'aaaaa,bbbb,ccc,ddd'
print('\nFormatting is nothing but advanced substitution')
print("e.g.  '%s and %s = ',s,line")
print('%s and %s = ', s, line)
print("e.g.  '%s and %s = ' %(s,line)")
print('%s and %s = ' % (s, line))
print("e.g.  '{0} and {1} = '.format(s,line)")
print('{0} and {1} = '.format(s, line))
print("e.g.  '{} and {} = ' .format(s,line)")
print('{} and {} = '.format(s, line))
print('With numbers, we can add separators, padding, digits, signs etc')

print('\nIn Python as a rule of thumb')
print('Generic operations that span multiple types are called Built-In functions. eg. len(obj)')
print('Type-specific operations are called Method Calls. eg. obj.upper()')

print('\nGetting Help in Python')
print('dir(obj) - Returns a list of all attributes that is available for the object that is passed into it')
print('dir function simply gives methods names')
print('dir(line) - ', dir(line))

print('\nThese names with double underscores represents')
print('Implementation of the object passed into it, in our case string object')
print('Also these are available for customization')

print('\neg. Concatenation - Python internally converts + to __add__ function call')
print("s + 'NI' is converted to s.__add__('NI')")
print("s + 'NI' = ", s + 'NI')
print("s.__add__('NI') = ", s.__add__('NI'))

print('\nAs mentioned earlier, dir lists method names')
print('To know what each function does, we have to use help(obj.method_name)')
print('help(obj.method_name)')
print('Instead of object, we can even pass datatype')

print('help(s.replace)')
print(help(s.replace))

print('help(str.replace)')
print(help(str.replace))

print('\nWe can also ask help on entire object')
print('Sometimes we will get more information and sometimes no help at all especially in newer version')
print('help(s) ')
print(help(s))

print('\nOther ways to code strings')
print('Escape sequences, Hexadecimal, Binary notations, Multiline, Raw string etc')
print('Trying to print \n without escape sequence')
print('Trying to print \\n with escape sequence')

S = "A\0B\0C"
print(
    'S = "A\\0B\\0C (slash zero)" - This is internally represented as "A\\x00B\\x00C"')  # used \\ to ignore special meaning to \0
print('But when we try to print S it displays as ABC. S - ', S)

print('\nMultiline')  # Refer below code, with output we cannot understand what is happening
S = """ aaaaaaaaaa
bbbbbbbbbbbbbbbbbbbbbb
cccccc

dddd"""
print(S)

print('\nRaw string Literal')
print("r'C:\\text\\new' - ", r'C:\text\new')  # Again here consider only one slash while reading

print('\nUnicode Strings')
print('This is required for processing text in International character sets or non-ASCII text')
print('Remember ASCII is simple version of Unicode')
print('Unicode strings are sequences of Unicode code points')
print('Which means they dont necessarily map to single bytes when encoded')
print('Non Unicode strings are sequences of 8 bit bytes that print using ASCII characters')

print('\nIn Unicode notion of bytes doesnt apply')
print('Unicode processing is mostly used during transferring of text data')
print('Text is encoded to bytes when stored in a file, and its decoded into characters when read back into memory')
print('One can safely defer Unicode topics until they have mastered string basics')

print('\nHow memory changes when stored in different format')
print('s s.encode("utf8") s.encode("utf16") - ', s, s.encode("utf8"), s.encode("utf16"))
print('Printing length for above statements - ', len(s), len(s.encode("utf8")), len(s.encode("utf16")))

print('\nPattern Matching')
print('import re')

print("""\nre.match('Hello[ \t]*(.*)world', 'Hello       Python world')""")
print("""This expression will Search substring that begins with the word “Hello,” followed by
zero or more tabs or spaces, followed by arbitrary characters to be saved as a matched
group, terminated by the word “world.” \n""")
match = re.match('Hello[ \t]*(.*)world', 'Hello       Python world')
print(match.group(1))

print('\nPicks out three groups separated by slashes')
print("""re.match('[/:](.*)[/:](.*)[/:](.*)', '/usr/home:lumberjack')""")
match = re.match('[/:](.*)[/:](.*)[/:](.*)', '/usr/home:lumberjack')
group = match.groups()
print(group)

print('\nAnother example')
print("""re.split('[/:]', '/usr/home:lumberjack')""")
split = re.split('[/:]', '/usr/home:lumberjack')
print(split)

print('\nLists')
print('They are positional ordered Collections of')
print('Arbitrarily Typed Objects with no Fixed Size')
print("They are Mutable")
print('eg. Lists of Folders, Employees, Emails etc')

print('In List operations, the outputs are Lists as well')
print('They can Grow and Shrink on demand (unlike arrays)')
L = [123, 'spam', 1.557]
print("L = [123, 'spam', 1.557]")
print("L L[0] L[:-1] L+[4, 5, 6] L*2 L = ", L, L[0], L[:-1], L + [4, 5, 6], L * 2, L)

print('\nAdding and Deleting elements in List')
print('L L.append("L") L', L, L.append("L"), L)  # Looks like parameter substitution is occuring from opposite side
print('L L.pop(1) L', L, L.pop(1), L)
print('L.pop(1.23) - This gives error as pop() expects only Integer values')
M = ['bb', 'aa', 'cc']
print("M = ['bb', 'aa', 'cc'] M.sort()", M, M.sort())
print("M = ['bb', 'aa', 'cc'] M.reverse()", M, M.reverse())

print('\nAutomatic Bounds Checking\nPython doesnt allow us to reference items that are not present')
print('It has automatic bound checking')

print('\nNesting')
print('Python support arbitrary nesting')
print('e.g. List contains a dictionary that contains another list and so on')
print('Multidimensional Arrays - e.g.Matix')
M = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
print('M = \n[[1,2,3],\n[4,5,6],\n[7,8,9]] = ', M)
print('M[1], M[1],[2] = ', M[1], M[1], [2])

print('\nComprehensions')
print('Its a powerful way to build new list by running an expression on each item in a sequence')
print('They are applied from left to right')
print('Comprehensions are coded in square brackets')
print('Comprehension = Expression + Looping Construct')

print('\ne.g Get Column Values')
print('col2 = [row[1] for row in M] = ', [row[1] for row in M])

print('\ne.g Add 1 to each item for Column 2')
print('[row[1] + 1 for row in M] = ', [row[1] + 1 for row in M])

print('\ne.g Filter out the odds')
print('Here we are using Conditional(if)  Statement in Comprehension')
print('[row[1] for row in M if row[1] % 2 == 0] = ', [row[1] for row in M if row[1] % 2 == 0])
print("[[x, x / 2, x * 2] for x in range(−6, 7, 2) if x > 0] = ", [[x, x / 2, x * 2] for x in range(-6, 7, 2) if x > 0])

print('\ne.g Repeat Characters in a string')
print('[c * 2 for c in "spam"] = ', [c * 2 for c in 'spam'])

print('\ne.g Get Diagonal of the Matrix')
print('[M[i][i] for i in [0, 1, 2]] = ', [M[i][i] for i in [0, 1, 2]])
