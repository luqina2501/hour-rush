import os

def load_all_maps(dir = "Map"):
    maps = []
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            path = os.path.join(dir, filename)
            with open(path, "r") as file:
                lines = file.readlines()
                grid = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith("#") or line == "":
                        continue
                    grid += line
                if len(grid) == 36:
                    maps.append(grid)
                else:
                    print(f"Skipped {filename} (invalid size: {len(grid)})")
    return maps