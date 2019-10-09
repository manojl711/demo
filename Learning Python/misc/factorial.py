# Recursion example

def fact(number):
    if number == 1:
        return 1
    return number * fact(number - 1)


n = int(input('Enter a number less than 10 : '))
factorial = fact(n)
print('Factorial of ', str(n), ' = ', str(factorial))


class Duck:
    def quack(self):
        print("Quaaaaaack!")

    def feathers(self):
        print("The duck has white and gray feathers.")


class Person:
    def quack(self):
        print("The person imitates a duck.")

    def feathers(self):
        print("The person takes a feather from the ground and shows it.")

    def name(self):
        print("John Smith")


def in_the_forest(obj):
    obj.quack()
    obj.feathers()


donald = Duck()
john = Person()
in_the_forest(donald)
in_the_forest(john)
