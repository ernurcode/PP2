def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2))
print(sum_all(1, 2, 3, 4, 5))





def greet_all(*names):
    for n in names:
        print("Hello,", n)

greet_all("Ernur", "Ali", "Dana")
