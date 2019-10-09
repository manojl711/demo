class Test:
    m = 1
    n = 2


print(Test.m, Test.n)


class C2:
    def __init__(self):
        self.x = 30
        self.z = 40
        print('C2')


class C3:
    def __init__(self):
        self.w = 50
        self.z = 60
        print('C3')


class C1(C2, C3):
    x = 5

    def __init__(self):
        self.x = 10
        self.y = 20
        print('C1')


I1 = C1()
I2 = C1()

print(I1.x, I1.y)
print(C1.x, C1.y)


# print(I2.x, I2.y, I2.w, I2.z)


class Animal:
    def speak(self):
        {
            print('Animal Sound')
        }


class Dog(Animal):
    def speak(self):
        {
            print('bow bow')
        }


class Cat(Animal):
    def speak(self):
        {
            print('meow meow')
        }


class Duck(Animal):
    def speak(self):
        {
            print('quack quack')
        }


class Sheep(Animal):
    def speak(self):
        {
            print('baa baa')
        }


class Cow(object):
    def speak(self):
        {
            print('moo moo')
        }


a = Cow()
b = Cat()
c = Dog()

a.speak()
b.speak()
c.speak()
