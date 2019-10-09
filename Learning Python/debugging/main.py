def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a / b


while (1):

    n1 = int(input('Enter First Number: '))
    n2 = int(input('Enter Second Number: '))
    op = input('Enter operator: ')

    if op == '+':
        res = add(n1, n2)
    elif op == '-':
        res = sub(n1, n2)
    elif op == '*':
        res = mul(n1, n2)
    elif op == '/':
        res = div(n1, n2)
    else:
        print('Wrong operator, Use only +, -, * , /')

    print(res)

    val = input('Press y to quit ')
    if val == 'y':
        break

print('Bye')
