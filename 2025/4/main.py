

def load_input(fname = "input.txt"):
    map = []
    with open(fname, 'r') as f:
        for line in f.readlines():
            map.append(list(line.strip()))
    return map

def print_map(map):
    for row in map:
        print(''.join(row))

def is_roll(map, r, c):
    if r < 0 or r >= len(map):
        return False
    row = map[r]
    if c < 0 or c >= len(row):
        return False
    return row[c] == '@'

def adjacent_rolls(map, r, c):
    rp, rm, cp, cm = r+1, r-1, c+1, c-1
    return sum( is_roll(map, rn, cn) for rn, cn in  [
        (rp, cp), (rp, c), (rp, cm),
        (r , cp),          (r , cm),
        (rm, cp), (rm, c), (rm, cm),
    ])

def count(items):
    return sum(1 for n in items)

def accessable_tiles(map):
    for r, row in enumerate(map):
        for c, tile in enumerate(row):
            if tile == '@' and adjacent_rolls(map, r, c) < 4:
                yield r,c

def removable_tiles(map):
    removed = 0
    while 1:
        block = 0
        for r, c in accessable_tiles(map):
            map[r][c] = 'x'
            block += 1
        removed += block
        if block == 0:
            return removed
        
if __name__ == "__main__":
    map = load_input()
    print(f"part1: {count(accessable_tiles(map))}")
    print(f"part2: {removable_tiles(map)}")
