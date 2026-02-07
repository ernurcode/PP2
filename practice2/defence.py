students = {"Ernur":100, "Nazar":70, "Alibek":90}
for x in students:
    gpa = 0
    if students[x] > 80:
        gpa = 4.0
    elif students[x] < 80:
        gpa = 3.54
    print(x, gpa)