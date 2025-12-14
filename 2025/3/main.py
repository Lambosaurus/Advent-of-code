

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield line.strip()

def max_digit(bank):
    index = 0
    digit = bank[0]
    for i in range(1, len(bank)):
        if bank[i] > digit:
            digit = bank[i]
            index = i
    return index, digit

def joltage(bank, n):
    digits = []
    for i in range(n):
        pos, d = max_digit(bank[:len(bank)-n+i+1])
        bank = bank[pos+1:]
        digits.append(d)
    return int(''.join(digits))

if __name__ == "__main__":
    banks = list(load_input())
    print(f"part1: {sum(joltage(b, 2) for b in banks)}")
    print(f"part2: {sum(joltage(b, 12) for b in banks)}")
