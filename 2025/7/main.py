
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        map = []
        for line in f.readlines():
            map.append(list(line.strip()))
        return map

def new_map(rs, cs, fill = 0):
    return [[fill] * cs for r in range(rs)]

def propagate(map):

    counts = new_map(len(map), len(map[0]))
    splits = 0

    for r, row in enumerate(map[:-1]):
        for c, col in enumerate(row):

            if col == 'S':
                counts[r][c] = 1

            if counts[r][c]:
                if map[r+1][c] == '^':
                    counts[r+1][c+1] += counts[r][c]
                    counts[r+1][c-1] += counts[r][c]
                    splits += 1
                else:
                    counts[r+1][c] += counts[r][c]

    return splits, sum(counts[-1])

if __name__ == "__main__":
    map = load_input()
    splits, paths = propagate(map)
    print(f"part1: {splits}")
    print(f"part2: {paths}")