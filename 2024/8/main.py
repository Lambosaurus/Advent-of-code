import math

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def extract_signals(map):
    signals = {}
    for r, row in enumerate(map):
        for c, col in enumerate(row):
            if col != '.':
                if not col in signals:
                    signals[col] = []
                signals[col].append((r,c))
    return signals

def get_size(map):
    return len(map), len(map[0])

def create_map(size, v):
    return [ [v] * size[1] for _ in range(size[0]) ]

def overlay_signals(map, signals):
    for key, items in signals.items():
        for r,c in items:
            map[r][c] = key
    return map

def print_map(map):
    for row in map:
        print("".join(row))

def in_bounds(bounds, v):
    return v[0] >= 0 and v[0] < bounds[0] and v[1] >= 0 and v[1] < bounds[1]

def antinode_pair(bounds, a, b):
    ra,ca = a
    rb,cb = b
    dr = rb - ra
    dc = cb - ca
    for coord in ( (ra-dr, ca-dc), (rb+dr, cb+dc) ):
        if in_bounds(bounds, coord):
            yield coord

def reduce_vector(r,c):
    gcd = math.gcd(r,c)
    if gcd > 1:
        return r/gcd,c/gcd
    return r,c

def antinode_array(bounds, a, b):
    ra,ca = a
    rb,cb = b
    dr,dc = reduce_vector(rb - ra, cb - ca)

    r,c = a
    while in_bounds(bounds, (r,c)):
        yield r,c
        r -= dr
        c -= dc

    r,c = b
    while in_bounds(bounds, (r,c)):
        yield r,c
        r += dr
        c += dc

def compute_antinodes(bounds, signals, antinode_generator):
    map = create_map(bounds, '.')
    for key,coords in signals.items():
        coords = signals[key]
        for i, a in enumerate(coords):
            for b in coords[i+1:]:
                for r,c in antinode_generator(bounds, a, b):
                    map[r][c] = '#'
    return map

def count_tiles(map, v = '#'):
    return sum( sum( col == v for col in row ) for row in map )

if __name__ == "__main__":
    map = load_input()
    signals = extract_signals(map)
    bounds = get_size(map)
    print( f"part1: { count_tiles(compute_antinodes(bounds, signals, antinode_pair)) }" )
    print( f"part2: { count_tiles(compute_antinodes(bounds, signals, antinode_array)) }" )