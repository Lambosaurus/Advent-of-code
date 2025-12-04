

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        line = f.readline()
        return [[int(n) for n in block.split('-')] for block in line.split(',')]

def n_part_id(s, n):
    digits = len(s)
    if digits % n != 0:
        return False
    
    size = digits // n
    segment = s[:size]
    for i in range(1, n):
        if s[i*size:(i+1)*size] != segment:
            return False
    return True

def two_part_id(id):
    s = str(id)
    return n_part_id(s, 2)

def any_part_id(id):
    s = str(id)
    digits = len(s)

    for parts in range(2, digits+1):
        if n_part_id(s, parts):
            return True
    return False

def find_ids(ranges, predicate):
    for start, stop in ranges:
        for id in range(start, stop + 1):
            if predicate(id):
                yield id

if __name__ == "__main__":
    ranges = load_input()
    print(f"part1: {sum(id for id in find_ids(ranges, two_part_id))}")
    print(f"part2: {sum(id for id in find_ids(ranges, any_part_id))}")
