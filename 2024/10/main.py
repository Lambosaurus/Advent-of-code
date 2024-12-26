
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [[int(ch) for ch in row.strip()] for row in f.readlines()]

def find_trailheads(map):
    for r, row in enumerate(map):
        for c, col in enumerate(row):
            if col == 0:
                yield r,c

def get_size(map):
    return len(map), len(map[0])

def directions(bounds, pos):
    r,c = pos
    if r > 0:
        yield r-1, c
    if c > 0:
        yield r, c-1
    if r < bounds[0] - 1:
        yield r+1, c
    if c < bounds[1] - 1:
        yield r, c+1

def valid_branches(map, pos, height):
    bounds = get_size(map)
    return ((r,c) for r,c in directions(bounds, pos) if map[r][c] == height)

def point_hash(point):
    r,c = point
    return (r << 8) | c

def rate_trails(map, trailhead):
    explored = { point_hash(trailhead): [trailhead, 1] }
    for height in range(1, 10):
        frontier = {}
        for pos, count in explored.values():
            for dir in valid_branches(map, pos, height):
                hash = point_hash(dir)
                if not hash in frontier:
                    frontier[hash] = [dir, 0]
                frontier[hash][1] += count
        explored = frontier
    return [count for _, count in explored.values()]


if __name__ == "__main__":
    map = load_input()
    ratings = [rate_trails(map, p) for p in find_trailheads(map)]
    print( f"part1: { sum( len(peak) for peak in ratings )}" )
    print( f"part2: { sum( sum(peak) for peak in ratings )}" )