import os
import hashlib
from collections import defaultdict

def hash_file(path):
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def find_duplicates(directory):
    hash_map = defaultdict(list)

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = hash_file(filepath)
            if file_hash:
                hash_map[file_hash].append(filepath)

    duplicates_found = False
    for paths in hash_map.values():
        if len(paths) > 1:
            duplicates_found = True
            print("🔁 Duplicate group:")
            for p in paths:
                print(f"   → {p}")
            print()

    if not duplicates_found:
        print("✅ No duplicate files found.")

# 🔍 Set to your project directory
if __name__ == "__main__":
    find_duplicates("C:/Users/VrdellaIT/Ashik/e_commerce")
