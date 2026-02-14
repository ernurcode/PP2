class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, I am", self.name)

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

    def info(self):
        print(self.name, "grade:", self.grade)

s = Student("Ernur", 11)
s.greet()
s.info()