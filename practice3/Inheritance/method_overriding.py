class Vehicle:
    def move(self):
        print("Vehicle is moving")

class Bike(Vehicle):
    def move(self):
        print("Bike is pedaling")

v = Vehicle()
b = Bike()
v.move()
b.move()



class Animal:
    def speak(self):
        print("Animal sound")

class Cat(Animal):
    def speak(self):
        print("Meow")

a = Animal()
c = Cat()

a.speak()
c.speak()