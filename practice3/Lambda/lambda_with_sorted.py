students = [("Ernur", 85), ("Ali", 92), ("Dana", 78)]
sorted_by_score = sorted(students, key=lambda x: x[1])
sorted_by_name = sorted(students, key=lambda x: x[0])
print(sorted_by_score)
print(sorted_by_name)





words = ["apple", "banana", "kiwi", "orange"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)