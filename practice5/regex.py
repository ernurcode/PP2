import re

s = input()
pattern = r"ab*"
if re.fullmatch(pattern, s):
    print("Match found")
else:
    print("No match")



s = input()
pattern = r"ab{2,3}"
if re.fullmatch(pattern, s):
    print("Match found")
else:
    print("No match")


s = input()
matches = re.findall(r"[a-z]+_[a-z]+", s)
print(matches)


s = input()
matches = re.findall(r"[A-Z][a-z]+", s)
print(matches)


s = input()
pattern = r"a.*b$"
if re.fullmatch(pattern, s):
    print("Match found")
else:
    print("No match")


s = input()
result = re.sub(r"[ ,\.]", ":", s)
print(result)


s = input()
components = s.split('_')
camel_case = components[0] + ''.join(x.title() for x in components[1:])
print(camel_case)


s = input()
split_list = re.findall(r"[A-Z]?[a-z]+", s)
print(split_list)


s = input()
result = re.sub(r"([A-Z])", r" \1", s).strip()
print(result)


s = input()
snake_case = re.sub(r'([A-Z])', r'_\1', s).lower().lstrip('_')
print(snake_case)