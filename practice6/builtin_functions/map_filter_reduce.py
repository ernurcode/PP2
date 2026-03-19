from functools import reduce
l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
squared = list(map(lambda x: x*x, l))
even_nums = list(filter(lambda x: x%2==0, l))
sum = reduce(lambda x,y : x+y, l)
print(squared)
print(even_nums)
print(sum)