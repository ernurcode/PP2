import re

with open("raw.txt", "r", encoding="utf-8") as f:
    t = f.read()

p = [int(x.replace(" ", "")) for x in re.findall(r"Стоимость\s*\n\s*([\d\s]+)", t)]
n = [m.splitlines()[0].strip() for m in re.findall(r"\d+\.\s*(.+?)(?:\n\d+|$)", t, flags=re.DOTALL)]

total = sum(p)

dt = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})", t)
dt = dt.group(1) if dt else ""

pay = re.search(r"Банковская карта|Наличные", t)
pay = pay.group(0) if pay else ""

for i in range(len(p)): 
    print(f"{i+1}. {n[i]} — {p[i]}")

print(f"Total: {total} Tenge")
print(f"Date & Time: {dt}")
print(f"Payment Method: {pay}")