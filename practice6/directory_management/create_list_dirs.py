import os
os.makedirs("one/two/three", exist_ok=True)
for root, sub, inner in os.walk("one"):
    print("folder:", root)
    print("Directories:", sub)
    print("Files:", inner)