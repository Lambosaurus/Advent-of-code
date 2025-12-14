import re

def load_input(fname = "input.txt"):
    shapes = []
    regions = []
    with open(fname, 'r') as f:
        
        for i in range(6):
            f.readline() # header
            shapes.append([
                f.readline().strip() for _ in range(3)
            ])
            f.readline() # whitespace

        for line in f.readlines():
            x,y,items = re.match(r"(\d+)x(\d+): (.+)", line).groups()
            size = int(x), (int(y))
            items = tuple(int(n) for n in items.split())
            regions.append((size, items))

    return shapes, regions

def shape_area(shape):
    return sum( sum(c == '#' for c in r) for r in shape )

def can_fit(shapes, region):
    size, items = region
    
    area = size[0] * size[1]
    max_area = sum(items) * 9
    min_area = sum(n * shape_area(shapes[i]) for i,n in enumerate(items))

    if area < min_area:
        return False
    if area >= max_area:
        return True
    
    print("uh oh")
    return False


if __name__ == "__main__":
    shapes, regions = load_input()
    print(f"part1: {sum(can_fit(shapes, region) for region in regions)}")
    print(f"part2: {0}")
