l = ["000", "111", "222", "333"]
for i,n in enumerate(l):
    print(i, n)

a = [1, 2, 3, 4]
b = ["a", "b", "c", "d"]
for x,y in zip(a,b):
    print(x,y)

x = "123"
y = int(x)
z = float(x)
print(type(x), type(y), type(z))