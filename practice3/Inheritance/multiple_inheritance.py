class Father:
    def skills1(self):
        print("Programming")

class Mother:
    def skills2(self):
        print("Design")

class Child(Father, Mother):
    def hobbies(self):
        print("Football")

ch = Child()
ch.skills1()
ch.skills2()
ch.hobbies()







class Parent1:
    def skill1(self):
        print("Cooking")

class Parent2:
    def skill2(self):
        print("Painting")

class Child2(Parent1, Parent2):
    def skill3(self):
        print("Dancing")

c = Child2()
c.skill1()
c.skill2()
c.skill3()