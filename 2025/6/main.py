
def extract_ranges(symbols):
    # Find the ranges 
    #        "aaaa bb ccc dd eeeee"
    # given: "+    +  +   +  +    "
    prev = None
    for i, s in enumerate(symbols):
        if s == ' ':
            continue
        if prev != None:
            yield prev, i-1
        prev = i
    yield prev, i+1

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        lines = f.readlines()
        symbols = lines[-1]
        values = lines[:-1]
        
        for start, stop in extract_ranges(symbols.strip('\n')):
            yield symbols[start], [ row[start:stop] for row in values ]

def transpose(values):
    for i in range(len(values[0])):
        yield ''.join(v[i] for v in values)

def solve(op, values):
    values = (int(v) for v in values)
    if op == '+':
        return sum(values)
    else: # op == '*':
        total = 1
        for v in values:
            total *= v
        return total

if __name__ == "__main__":
    problems = list(load_input())
    print(f"part1: {sum(solve(op, values) for op, values in problems)}")
    print(f"part2: {sum(solve(op, transpose(values)) for op, values in problems)}")
