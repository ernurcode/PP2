numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers)) 

greater_than_three = list(filter(lambda x: x > 3, numbers))

odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))

print(evens)
print(greater_than_three)
print(odd_numbers)