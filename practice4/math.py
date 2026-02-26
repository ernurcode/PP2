import math
d = int(input("Input degree: "))
print(f"Output radian: {d*math.pi/180:.6f}")

h = int(input("Height:"))
b1 = int(input("Base, first value: "))
b2 = int(input("Base, second value: "))
print(f"Expected Output: {((b1+b2)/2)*h}")


import math
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area = (n * s ** 2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area}")


l = int(input("Length of base: "))
h = int(input("Height of parallelogram: "))
print(h*l)