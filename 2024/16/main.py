
DIR_RIGHT = 0
DIR_UP = 1
DIR_LEFT = 2
DIR_DOWN = 3

VECTORS = {
    DIR_RIGHT:  (0,  1),
    DIR_UP:     (1,  0),
    DIR_LEFT:   (0, -1),
    DIR_DOWN:   (-1, 0),
}

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [ list(line.strip()) for line in f.readlines() ]
    
def print_map(map):
    for row in map:
        print("".join(row))

def extract_tile(map, tile):
    for r,row in enumerate(map):
        for c,col in enumerate(row):
            if col == tile:
                map[r][c] = '.'
                return r,c
            
def v_hash(vector):
    r,c,v = vector
    return (v << 16) | (r << 8) | c

def v_add(vector, dir):
    r,c,v = vector
    return r+dir[0],c+dir[1],v

def pos_to_v(pos, v):
    r,c = pos
    return r,c,v

def heuristic(vector, goal):
    steps = abs(goal[0] - vector[0]) + abs(goal[1] - vector[1])
    # Does accounting for turns improve this...?
    return steps

def neighbours(map, vector):
    r,c,v = vector

    dir = VECTORS[v]
    rf = r + dir[0]
    cf = c + dir[1]

    if map[rf][cf] != '#':
        yield (r+dir[0], c+dir[1], v), 1   # Forward
    yield (r, c, (v+1) % 4), 1000          # CW
    yield (r, c, (v-1) % 4), 1000          # CCW

def reconstruct_path(explored, hash, path = None):
    if path == None:
        path = {}

    while True:
        vector, _, children = explored[hash]
        r,c,_ = vector

        path[ v_hash((r,c,0)) ] = (r,c)

        if children == None:
            return path

        hash = children[0]
        for child in children[1:]:
            # This does a lot of overlapping work, and makes a lot of duplicate nodes.
            reconstruct_path(explored, child, path)

def best_path(map):
    start = pos_to_v(extract_tile(map, 'S'), DIR_RIGHT)
    goal = extract_tile(map, 'E')

    frontier = { v_hash(start): heuristic(start, goal) }
    explored = { v_hash(start): (start, 0, None) }
    while len(frontier):
        # Extract the best known node
        src_hash,_ = min(frontier.items(), key = lambda k: k[1] )
        del frontier[src_hash]
        src, src_cost, _ = explored[src_hash]
        
        for dst, step_cost in neighbours(map, src):

            dst_cost = src_cost + step_cost
            dst_hash = v_hash(dst)

            if dst_hash in explored:
                previous_cost = explored[dst_hash][1]
                if previous_cost < dst_cost:
                    continue
                if previous_cost == dst_cost:
                    explored[dst_hash][2].append(src_hash)
                    continue

            explored[dst_hash] = (dst, dst_cost, [src_hash])
            dst_heuristic = dst_cost + heuristic(dst, goal)
            if (not dst_hash in frontier) or dst_heuristic < frontier[dst_hash]:
                frontier[dst_hash] = dst_heuristic

            if dst[0] == goal[0] and dst[1] == goal[1]:
                return dst_cost, reconstruct_path(explored, dst_hash).values()

def plot_path(map, path):
    for r,c in path:
        map[r][c] = 'O'
    return map

if __name__ == "__main__":
    map = load_input()
    cost, paths = best_path(map)
    print( f"part1: {cost}" )
    print( f"part2: {len(paths)}" )
    #print_map(plot_path(map, paths))
    