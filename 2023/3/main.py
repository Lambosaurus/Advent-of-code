

def load_input(fname = "input.txt"):
    map = []
    with open(fname, 'r') as f:
        for line in f:
            map.append(line.strip())
    return map

def get_number(row, start):
    end = start
    while end < len(row) and row[end].isnumeric():
        end += 1
    if end == start:
        return None
    return row[start:end]

def is_symbol(map, r, c):
    if r < 0 or r >= len(map):
        return False
    row = map[r]
    if c < 0 or c >= len(row):
        return False
    tile = row[c]
    return not( tile == '.' or tile.isnumeric() )

def adjacent_symbols(map, r, c, length):
    cmin = c - 1
    cmax = c + length
    rmin = r - 1
    rmax = r + 1
    candidates  = [ (r, cmin), (r, cmax) ] # ahead and behind
    candidates += [ (rmin, c2) for c2 in range(cmin, cmax+1) ] # top
    candidates += [ (rmax, c2) for c2 in range(cmin, cmax+1) ] # bottom

    for r,c in candidates:
        if is_symbol(map, r, c):
            yield r,c

def enumerate_symbols(map):
    for r, row in enumerate(map):
        c = 0
        while c < len(row):
            number = get_number(row, c)
            if number is None:
                c += 1
                continue
            
            for sr, sc in adjacent_symbols(map, r, c, len(number)):
                yield sr, sc, int(number)
                break

            c += len(number) + 1 # Numbers must also be separated by 1 char.

def valid_numbers(map):
    return (n for r,c,n in enumerate_symbols(map))

def gear_ratios(map):

    gear_map = {}

    for r,c,n in enumerate_symbols(map):
        if map[r][c] == '*':
            z = (r << 8) | c
            if not z in gear_map:
                gear_map[z] = []
            gear_map[z].append(n)

    for ns in gear_map.values():
        if len(ns) == 2:
            yield ns[0] * ns[1]

if __name__ == "__main__":
    map = load_input()
    print(f"part1: {sum(valid_numbers(map))}")
    print(f"part2: {sum(gear_ratios(map))}")
