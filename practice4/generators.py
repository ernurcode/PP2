def gen(n):
    for i in range(1,n):
        yield i*i
n = int(input())
n = gen(n)
for i in n:
    print(i)



def gen(n):
    for i in range(n+1):
        if i%2==0:
            yield i
n = int(input())
h = gen(n)
l=list(h)
print(",".join(map(str, l)))



def gen(n):
    for i in range(n+1):
        if i%3==0 and i%4==0:
            yield i
n = int(input())
for i in gen(n):
    print(i)


def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2
a = int(input())
b = int(input())
for sq in squares(a, b):
    print(sq)


def countdown(n):
    for i in range(n, -1, -1):
        yield i
n = int(input())
for num in countdown(n):
    print(num)