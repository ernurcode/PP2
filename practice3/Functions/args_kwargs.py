def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3, 4))








def print_info(**data):
    for key, value in data.items():
        print(key, ":", value)

print_info(name="Ernur", age=17)
print_info(city="Astana", job="Student")
