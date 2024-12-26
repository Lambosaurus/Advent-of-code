
def load_schematic(f):
    lines = [f.readline() for _ in range(7)]
    polarity = lines[0][0]
    cols = []
    for c in range(5):
        for r in range(6):
            if lines[r+1][c] != polarity:
                cols.append(5 - r)
                break

    is_lock = polarity == '#'
    return is_lock, cols

def load_input(fname = "input.txt"):
    keys = []
    locks = []
    with open(fname, 'r') as f:
        while True:
            is_lock, schematic = load_schematic(f)
            (locks if is_lock else keys).append(schematic)
            if f.readline() != '\n':
                break
    return keys, locks

def test_key(key, lock):
    for k,l in zip(key, lock):
        if k > l:
            return False
    return True

def test_all_keys(keys, locks):
    total = 0
    for key in keys:
        for lock in locks:
            total += test_key(key, lock)
    return total

if __name__ == "__main__":
    keys, locks = load_input()
    print( f"part1: {test_all_keys(keys, locks)}" )

