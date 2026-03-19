import os, shutil
os.makedirs("dir1", exist_ok=True)
os.makedirs("dir2", exist_ok=True)
with open("dir1/test.txt", "w", encoding="utf8") as f:
    f.write("New TEXT")
shutil.copy("dir1/test.txt", "dir2/test_copy")
shutil.move("dir1/test.txt", "dir2/test_name_another")
for files in os.listdir("dir2"):
    if files.endswith(".txt"):
        print(files)