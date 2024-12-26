
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield tuple( int(n) for n in line.split(',') )

def create_map(size, v):
    return [ [v]*size[0] for _ in range(size[1]) ]

def get_size(map):
    return len(map[0]), len(map)

def print_map(map):
    for row in map:
        print("".join(row))

def place_points(map, points, count):
    for _,(x,y) in zip(range(count), points):
        map[y][x] = '#'
    return map

def v_hash(point):
    x,y = point
    return (x << 8) | y

def v_add(point, dir):
    return point[0]+dir[0], point[1]+dir[1]

def valid_directions(pos, bounds):
    x,y = pos
    if x > 0:
        yield x-1, y
    if y > 0:
        yield x, y-1
    if x < bounds[0] - 1:
        yield x+1, y
    if y < bounds[1] - 1:
        yield x, y+1

def neighbours(map, point):
    bounds = get_size(map)
    for x,y in valid_directions(point, bounds):
        if map[y][x] != '#':
            yield x,y

def heuristic(vector, goal):
    return abs(goal[0] - vector[0]) + abs(goal[1] - vector[1])

def reconstruct_path(explored, hash):
    path = []
    while hash != None:
        hash = explored[hash][2]
        path.append(hash)
    return path

def best_path(map):
    size = get_size(map)
    start = (0,0)
    goal = v_add(size, (-1,-1))

    frontier = { v_hash(start): heuristic(start, goal) }
    explored = { v_hash(start): (start, 0, None) }
    while len(frontier):
        # Extract the best known node
        src_hash, _ = min(frontier.items(), key = lambda k: k[1] )
        del frontier[src_hash]
        src, src_cost, _ = explored[src_hash]
        
        for dst in neighbours(map, src):

            dst_cost = src_cost + 1
            dst_hash = v_hash(dst)

            if (not dst_hash in explored) or (dst_cost < explored[dst_hash][1]):

                explored[dst_hash] = (dst, dst_cost, src_hash)
                if not dst_hash in frontier:
                    frontier[dst_hash] = dst_cost + heuristic(dst, goal)

                if dst[0] == goal[0] and dst[1] == goal[1]:
                    return reconstruct_path(explored, dst_hash)
    return None
            
def blocking_point(map, sequence):
    path = best_path(map)
    for point in sequence:
        map[point[1]][point[0]] = '#'
        if v_hash(point) in path:
            # we blocked our path. Check again
            path = best_path(map)
            if path == None:
                return point
    return None

def format_point(point):
    return ",".join(str(n) for n in point)

if __name__ == "__main__":
    sequence = load_input()
    size, count = (71,71), 1024
    map = place_points(create_map(size, '.'), sequence, count)
    print( f"part1: {len(best_path(map))-1}" )
    print( f"part2: {format_point(blocking_point(map, sequence))}" )
