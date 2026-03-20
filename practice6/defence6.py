import os
from functools import reduce
products = []

for file in os.listdir("sales"):
    path = os.path.join("sales", file)
    with open(path, "r") as f:
        for l in f:
            rec, qty = l.strip().split(",")
            products.append((rec, int(qty)))

total_records=len(products)
total_qty =sum(q for _, q in products)
avg = total_qty / total_records


maxsale = max(products, key=lambda x: x[1])
minsale = min(products, key=lambda x: x[1])

increased = list(map(lambda x: (x[0], x[1]+2), products))
popular = list(filter(lambda x: x[1] > 5, products))
productall = reduce(lambda x, y: x*y, [q for _, q in products])

for i, (name, qty) in enumerate(products, 1):
    print(i, name, qty)

names = [p[0] for p in products]
quantities = [p[1] for p in products]
zipped = list(zip(names, quantities))

sorted_p = sorted(products, key=lambda x: x[1])

with open("result.txt", "w") as f:
    f.write(f"Total records: {total_records}\n")
    f.write(f"Average quantity sold: {avg:.2f}\n")
    f.write(f"Highest quantity sold: {maxsale[1]}\n")
    f.write(f"Lowest quantity sold: {minsale[1]}\n\n")
    f.write("Popular products:\n")
    for name, qty in popular:
        f.write(f"{name} {qty}\n")