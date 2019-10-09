# Chapter 02: How Python Run Programs
# Chapter 03: How You Run Programs
import os
import sys
import importlib
from MBot import mir3_functions as mir3

print('# Chapter 02: How Python Run Programs')
print('# Chapter 03: How You Run Programs')

print('\nGet Current working directory')
print('import os')
print('os.getcwd()')
print(os.getcwd())

print('\nGet Platform such as win32/win64. It tells what kind of computer you are working on')
print('import sys')
print('sys.platform')
print(sys.platform)

print('\nRunning scripts')
print('python script01.py')
print('C:\python33\python script01.py')

print('\nChoosing version while running scripts')
print('py -3 script01.py')

print('\nIn Unix make sure to write the first line as')
print('#!/usr/local/bin/python')

print('\nForce python to run the file again in same session without stopping and restarting session. Use reload')
print('import importlib')
print('importlib.reload(module)')

print('\nTo get list all names inside a module')
print('dir() or dir(module_name)')
a = 5
m = 'mj'
print(dir())

print('\nLaunch files/other script using exec statement')
print('exec(open("script_name.py").read())')
print('Calling Factorial Program')
# Below statement triggers python script
# exec(open('C:\\Users\\mlingaiah\\PycharmProjects\\Python_Crash_Course\\Learning Python\\factorial.py').read())

print('\nShow python search paths for modules')
print('sys.path')
print(sys.path)

print('\nTo get help - Use help(object) for help about object')
print('help(mir3)')
print(help(mir3))
print('\nhelp(importlib)')
print(help(importlib))
