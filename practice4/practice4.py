import json, math

with open("d.json", "r") as f:
    p = json.load(f)

res = (p["a"] + p["b"])*2 / 3
res1 = math.ceil(res)

with open("result.json", "w") as f:
    json.dump(res1, f)