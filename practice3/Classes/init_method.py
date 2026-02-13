class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        return self.name + " is " + str(self.age)

s1 = Student("Ernur", 17)
s2 = Student("Ali", 18)

print(s1.info())
print(s2.info())
