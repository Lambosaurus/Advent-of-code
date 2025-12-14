
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield line


if __name__ == "__main__":
    lines = list(load_input())
    print(f"part1: {0}")
    print(f"part2: {0}")
