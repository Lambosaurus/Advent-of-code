

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f:
            value = int(line[1:])
            yield -value if line[0] == 'L' else value

def count_zeros(moves, pos = 50):
    count = 0
    for m in moves:
        pos = (pos + m) % 100
        if pos == 0:
            count += 1
    return count

def count_zero_crossings(moves, pos = 50):
    count = 0
    for m in moves:

        if m > 0:
            count += int((pos + m) / 100)
        else:
            count += int(((100 - pos) % 100 - m) / 100)

        pos = (pos + m) % 100
    return count

if __name__ == "__main__":
    moves = list(load_input())
    print(f"part1: {count_zeros(moves)}")
    print(f"part2: {count_zero_crossings(moves)}")
