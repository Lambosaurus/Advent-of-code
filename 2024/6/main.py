

TILE_EMPTY      = 0x00
TILE_UP         = 0x01
TILE_RIGHT      = 0x02
TILE_DOWN       = 0x04
TILE_LEFT       = 0x08
TILE_GUARD      = TILE_UP | TILE_RIGHT | TILE_DOWN | TILE_LEFT
TILE_OBSTACLE   = 0x10

VECTORS = {
    TILE_UP:    (-1,  0, TILE_RIGHT),
    TILE_RIGHT: ( 0,  1, TILE_DOWN),
    TILE_DOWN:  ( 1,  0, TILE_LEFT),
    TILE_LEFT:  ( 0, -1, TILE_UP),
}

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        map = [list(l.strip()) for l in f.readlines()]

        for r, row in enumerate(map):
            for c in range(len(row)):
                col = decode_tile(row[c])
                row[c] = col

                if col & TILE_GUARD:
                    gr,gc,gv = r,c,col
        
        return map, (gr, gc, gv)

def copy_map(map):
    return [list(row) for row in map]

def visualize_tile(c):
    if c == TILE_OBSTACLE:
        return '#'
    if c == TILE_EMPTY:
        return '.'
    if c & (TILE_DOWN | TILE_UP) == 0:
        return '-'
    if c & (TILE_LEFT | TILE_RIGHT) == 0:
        return '|'
    return '+'

def decode_tile(c):
    if c == '#':
        return TILE_OBSTACLE
    if c == '.':
        return TILE_EMPTY
    return TILE_UP

def print_map(map):
    for row in map:
        print("".join(visualize_tile(t) for t in row))

def simulate_guard(map, guard, depth = 0):
    map = copy_map(map)
    rows, cols = len(map), len(map[0])
    r,c,v = guard
    dr,dc,nv = VECTORS[v]
    loops = 0
    while True:
        map[r][c] |= v

        nr,nc = r + dr, c + dc
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            # Moved out of bounds
            return map, loops
        
        if map[nr][nc] & TILE_OBSTACLE:
            # We hit a wall. Get rotated.
            v = nv
            dr,dc,nv = VECTORS[v]
        elif map[nr][nc] & v:
            # We've done this before
            return map, loops + 1
        else:

            # Not an obstacle. But what if it was?
            if depth and map[nr][nc] == TILE_EMPTY:
                map[nr][nc] = TILE_OBSTACLE
                loops += simulate_guard(map, (r,c,v), depth-1)[1]
                map[nr][nc] = TILE_EMPTY

            r,c = nr,nc

def count_occupied(map):
    return sum( sum( int((col & TILE_GUARD) > 0) for col in row ) for row in map )

if __name__ == "__main__":
    map, guard = load_input()
    print( f"part1: {count_occupied(simulate_guard(map, guard)[0])}" )
    print( f"part2: {simulate_guard(map, guard, 1)[1]}" )
