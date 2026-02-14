class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def run(self):
        print("Dog runs")

d = Dog()
d.speak()
d.run()