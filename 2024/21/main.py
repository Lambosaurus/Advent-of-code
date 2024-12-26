
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [ line.strip() for line in f.readlines() ]
    
N_KEYPAD = [ "789", "456", "123", " 0A" ]
DIR_KEYPAD = [ " ^A", "<v>" ]

def find_key(keypad, key):
    for r, row in enumerate(keypad):
        for c, col in enumerate(row):
            if col == key:
                return r,c
            
def v_sub(a, b):
    return a[0]-b[0], a[1]-b[1]

def to_path(coordinate, col_first = False):
    r,c = coordinate
    row = ('v' * r) if r > 0 else ('^' * -r) 
    col = ('>' * c) if c > 0 else ('<' * -c)
    return f"{col}{row}A" if col_first else f"{row}{col}A"

def valid_paths(keypad, srckey, dstkey):

    # Quick exit on this common case.
    if srckey == dstkey:
        yield 'A'
        return

    start = find_key(keypad, srckey)
    goal = find_key(keypad, dstkey)
    
    delta = v_sub(goal, start)

    # Doesnt matter. Direct path.
    if delta[0] == 0 or delta[1] == 0:
        yield to_path(delta)
        return
    
    nullkey = find_key(keypad, ' ')
    
    # If start[col] coincides with nullkey[col], then we should go row first
    if not ( start[1] == nullkey[1] and goal[0] == nullkey[0] ):
        yield to_path(delta, False)

    # If start[row] coincides with nullkey[row], then we should go col first
    if not ( start[0] == nullkey[0] and goal[1] == nullkey[1] ):
        yield to_path(delta, True)

def create_memo(depth = 0):
    return [ {} for _ in range(depth + 1) ]

def shortest_path(keypad, sequence, depth, memo, srckey = 'A'):

    path_length = 0

    for dstkey in sequence:

        move_hash = srckey + dstkey
        if move_hash in memo[depth]:
            sublength = memo[depth][move_hash]
        else:
            subsequences = valid_paths(keypad, srckey, dstkey)
            if depth:
                sublength = min(shortest_path(DIR_KEYPAD, s, depth-1, memo) for s in subsequences)
            else:
                sublength = min(len(s) for s in subsequences)
            memo[depth][move_hash] = sublength
        
        path_length += sublength
        srckey = dstkey
    
    return path_length

def complexity_score(code, path):
    return int(code[:-1]) * path

if __name__ == "__main__":
    codes = load_input()
    memo = create_memo(25)
    print( f"part1: {sum(complexity_score(code, shortest_path(N_KEYPAD, code, 2, memo)) for code in codes)}" )
    print( f"part2: {sum(complexity_score(code, shortest_path(N_KEYPAD, code, 25, memo)) for code in codes)}" )
