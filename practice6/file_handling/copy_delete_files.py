import os
import shutil
with open("p6_example.txt", "a", encoding="utf8") as f:
    f.write("\nNew text appended")
with open("p6_example.txt", "r", encoding="utf-8") as f:
    print(f.read())

shutil.copy("p6_example.txt", "p6_copy.txt")
shutil.copy("p6_example.txt", "p6_backup.txt")

if os.path.exists("p6_copy.txt"):
    os.remove("p6_copy.txt")
