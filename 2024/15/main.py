
def load_map(f):
    map = []
    while True:
        line = f.readline()
        if line == "\n":
            return map
        map.append(list(line.strip()))

def load_moves(f):
    moves = []
    for line in f.readlines():
        moves.extend( line.strip() )
    return moves

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        map = load_map(f)
        moves = load_moves(f)
        return map, moves
    
VECTORS = {
    '>': (0,  1),
    'v': (1,  0),
    '<': (0, -1),
    '^': (-1, 0),
}

def print_map(map):
    for row in map:
        print("".join(row))

def find_robot(map):
    for r, row in enumerate(map):
        for c, col in enumerate(row):
            if col == '@':
                return r,c

def vector_add(a, b):
    return a[0] + b[0], a[1] + b[1]

def chained_tiles(tile, pos, dir):
    # Returns a list of tiles affected by a push action to the target tile.
    if tile == '.':
        return ()
    if dir[0]:
        if tile == '[':
            return pos, vector_add(pos, (0,1))
        if tile == ']':
            return pos, vector_add(pos, (0,-1))
    return pos,

def tile_pushable(map, pos, dir):
    tile = map[pos[0]][pos[1]]
    if tile == '#':
        return False
    for src in chained_tiles(tile, pos, dir):
        dst = vector_add(src, dir)
        if not tile_pushable(map, dst, dir):
            return False
    return True

def push_tile(map, pos, dir):
    tile = map[pos[0]][pos[1]]
    
    for src in chained_tiles(tile, pos, dir):
        dst = vector_add(src, dir)
        push_tile(map, dst, dir)
        map[dst[0]][dst[1]] = map[src[0]][src[1]]
        map[src[0]][src[1]] = '.'

def move_robot(map, pos, move):
    dir = VECTORS[move]
    if tile_pushable(map, pos, dir):
        push_tile(map, pos, dir)
        pos = vector_add(pos, dir)
    return pos

def simulate_robot(map, moves):
    robot = find_robot(map)
    for move in moves:
        robot = move_robot(map, robot, move)
    return map

def gps_coordinates(map):
    for r,row in enumerate(map):
        for c,col in enumerate(row):
            if col in "O[":
                yield (r * 100) + c

def wide_map(map):
    subs = {
        '#': "##",
        'O': "[]",
        '.': '..',
        '@': '@.',
    }
    return [  list("".join(subs[col] for col in row)) for row in map ]

if __name__ == "__main__":
    map, moves = load_input()
    wmap = wide_map(map)
    print( f"part1: {sum(gps_coordinates(simulate_robot(map, moves)))}" )
    print( f"part2: {sum(gps_coordinates(simulate_robot(wmap, moves)))}" )
    