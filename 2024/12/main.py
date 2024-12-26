
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def new_map(size, v):
    rows, cols = size
    return [ [v] * cols for _ in range(rows) ]

def get_size(map):
    return len(map), len(map[0])

def valid_directions(pos, bounds):
    r,c = pos
    if r > 0:
        yield r-1, c
    if c > 0:
        yield r, c-1
    if r < bounds[0] - 1:
        yield r+1, c
    if c < bounds[1] - 1:
        yield r, c+1

def hash_point(pos):
    r,c = pos
    return (r << 8) | c

def directions(pos):
    r,c = pos
    return [
        (r+1,c,'v'),
        (r,c+1,'>'),
        (r-1,c,'^'),
        (r,c-1,'<')
    ]

def build_region(map, pos):
    bounds = get_size(map)
    region = {}

    r,c = pos
    plant = map[r][c]
    map[r][c] = '.'
    edges = { hash_point(pos): pos }

    while len(edges):
        frontier = {}
        for hash, pos in edges.items():
            region[hash] = pos
            for r,c in valid_directions(pos, bounds):
                if map[r][c] == plant:
                    map[r][c] = '.'
                    frontier[hash_point((r,c))] = (r,c)
        edges = frontier
    return region

def get_regions(map):
    rows, cols = get_size(map)
    for r in range(rows):
        for c in range(cols):
            if map[r][c] != '.':
                yield build_region(map, (r,c))

def price_region(region, weighting_factor):
    area = len(region)
    weight = weighting_factor(region)
    return area * weight

def get_side_segments(region):
    for pos in region.values():
        for r,c,v in directions(pos):
            if not hash_point((r,c)) in region:
                yield (pos, v, 1)

def get_perimiter(region):
    return sum( 1 for _ in get_side_segments(region) )

AXES = {
    'v': (0,1),
    '>': (1,0),
    '^': (0,1),
    '<': (1,0),
}

def merge_segments(segments, start):
    for i in range(start, len(segments)):
        p1, d1, l1 = segments[i]
        for j in range(i+1, len(segments)):
            p2, d2, l2 = segments[j]
            if d1 != d2:
                continue
            x,y = AXES[d1]
            if p1[x] != p2[x]:
                continue
            if p1[y] + l1 == p2[y]:
                segments[i] = (p1, d1, l1 + l2)
                segments.pop(j)
                return i
            if p2[y] + l2 == p1[y]:
                segments[i] = (p2, d2, l1 + l2)
                segments.pop(j)
                return i
    return len(segments)

def get_sides(region):
    segments = list(get_side_segments(region))
    index = 0
    while index < len(segments):
        index = merge_segments(segments, index)
    return sum( 1 for _ in segments )

def print_map(map):
    for row in map:
        print("".join(row))

def print_region(region, bounds, plant = 'P'):
    map = new_map(bounds, '.')
    for r,c in region:
        map[r][c] = plant
    print_map(map)

if __name__ == "__main__":
    map = load_input()
    regions = list(get_regions(map))
    print( f"part1: {sum( price_region(r, get_perimiter) for r in regions)}" )
    print( f"part2: {sum( price_region(r, get_sides) for r in regions)}" )

