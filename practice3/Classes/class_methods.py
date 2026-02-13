class Car:
    def __init__(self, brand):
        self.brand = brand
        self.speed = 0

    def accelerate(self, value):
        self.speed += value

    def info(self):
        print(self.brand, "speed:", self.speed)

car1 = Car("Toyota")
car1.accelerate(20)
car1.accelerate(30)
car1.info()




class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds")

acc = BankAccount("Ernur")
acc.deposit(100)
acc.withdraw(30)
print(acc.balance)
