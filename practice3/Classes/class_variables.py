class Employee:
    company = "TechCorp"

    def __init__(self, name):
        self.name = name

e1 = Employee("Ernur")
e2 = Employee("Ali")

print(e1.company)
print(e2.company)

Employee.company = "NewTech"

print(e1.company)
print(e2.company)

e1.company = "PrivateCorp"

print(e1.company)
print(e2.company)





class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

r1 = Rectangle(5, 10)
r2 = Rectangle(3, 7)
print(r1.area())
print(r2.area())
