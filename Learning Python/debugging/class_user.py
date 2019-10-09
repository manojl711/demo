class User:
    active_users = 0  # Class attribute

    # Adding class method
    @classmethod
    def display_active_users(cls):
        return f'There are currently {cls.active_users} active users'

    # Using class method to convert string to multiple params
    # and then create an instance
    @classmethod
    def from_string(cls, data_string):
        (first, last, age) = data_string.split(',')
        return cls(first, last, age)  # This is similar to User('Tom','Jones','89')

    def __init__(self, first, last, age=''):
        self.first = first
        self.last = last
        self.age = age
        User.active_users += 1

    def full_name(self):
        print(f'{self.first} {self.last}')

    def initials(self):
        print(f'{self.first[0]}.{self.last[0]}.')

    def likes(self, thing):
        print(f'{self.first} likes {thing}')

    def logout(self):
        User.active_users -= 1
        print(f'{self.first} logged out')


# Note: Now here we create new class Moderator
class Moderator(User):
    def __init__(self, first, last, age, community):
        super().__init__(first, last, age)  # Here super is used to copy attributes
        self.community = community  # Community is unique to this class

    def remove_post(self):
        return f'{self.full_name()} removed a post from {self.community}'


jasmine = Moderator('Jasmine', 'O Conor', 61, 'Piano')
print(jasmine.full_name())
print(jasmine.community)
