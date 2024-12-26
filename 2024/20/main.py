
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [ list(line.strip()) for line in f.readlines() ]

def get_size(map):
    return len(map[0]), len(map)

def print_map(map):
    for row in map:
        print("".join(row))

def extract_tile(map, tile):
    for r,row in enumerate(map):
        for c,col in enumerate(row):
            if col == tile:
                map[r][c] = '.'
                return r,c

def v_add(a, b):
    return a[0]+b[0], a[1]+b[1]

def v_hash(v):
    return (v[0] << 8) | v[1]

def v_compare(a, b):
    return a[0] == b[0] and a[1] == b[1]

def valid_directions(pos, bounds):
    r,c = pos
    if r > 0:
        yield r-1, c
    if c > 0:
        yield r, c-1
    if r < bounds[0] - 1:
        yield r+1, c
    if r < bounds[1] - 1:
        yield r, c+1

def compute_path(map):
    bounds = get_size(map)
    start = extract_tile(map, 'S')
    goal = extract_tile(map, 'E')
    pos = start

    steps = 0
    path = {}
    path[v_hash(pos)] = (pos, steps)

    while not v_compare(pos, goal):

        for r,c in valid_directions(pos, bounds):
            dir_hash = v_hash((r,c))
            if map[r][c] == '#' or dir_hash in path:
                continue
            pos = r,c
            steps += 1
            path[dir_hash] = (pos, steps)
            break

    return path

def new_kernel(steps):
    for dr in range(-steps, steps+1):
        r_steps = abs(dr)
        c_step_max = steps - r_steps
        for dc in range(-c_step_max, c_step_max+1):
            c_steps = abs(dc)
            cost = r_steps + c_steps
            yield (dr,dc), cost

def find_skips(path, steps):
    kernel = tuple(new_kernel(steps))
    for src, src_steps in path.values():
        for dir, skip_cost in kernel:
            dst = v_add(dir, src)
            dst_hash = v_hash(dst)
            if dst_hash in path:
                _, dst_steps = path[dst_hash]
                time_saved = src_steps - dst_steps - skip_cost
                if time_saved > 0:
                    yield time_saved

if __name__ == "__main__":
    map = load_input()
    path = compute_path(map)
    print( f"part1: { sum( s >= 100 for s in find_skips(path, 2) ) }" )
    print( f"part2: { sum( s >= 100 for s in find_skips(path, 20) ) }" )
