
def load_input(fname = "input.txt"):
    equations = []
    with open(fname, 'r') as f:
        for line in f:
            result, numbers = line.split(': ')
            result = int(result)
            numbers = [ int(n) for n in numbers.split(' ') ]
            equations.append((result, numbers))
    return equations

def concat_numbers(a, b):
    return int( f"{a}{b}" )

def resolve_equation_r(numbers, result, total, op, ops):
    if op == '+':
        total += numbers[0]
    elif op == '*':
        total *= numbers[0]
    else:
        total = concat_numbers(total, numbers[0])
    
    if total > result:
        # We overshot. Early abort.
        return 1

    if len(numbers) > 1:
        for op in ops:
            dir = resolve_equation_r(numbers[1:], result, total, op, ops)
            if dir == 0:
                return 0
        return -1

    else:
        # No more numbers. Return eq or undershoot
        return 0 if total == result else -1


def resolve_equation_base(numbers, result, ops = "+*|"):
    return resolve_equation_r(numbers, result, 0, '+', ops) == 0


if __name__ == "__main__":
    equations = load_input()
    print( f"part1: { sum( r for r,e in equations if resolve_equation_base(e, r, "+*") ) }" )
    print( f"part2: { sum( r for r,e in equations if resolve_equation_base(e, r, "+*|") ) }" )
