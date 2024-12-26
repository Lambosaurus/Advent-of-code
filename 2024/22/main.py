
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [ int(line) for line in f.readlines() ]


def prng_next(n):
    prune_mask = (1 << 24) - 1
    n = (n ^ (n <<  6)) & prune_mask
    n = (n ^ (n >>  5))
    n = (n ^ (n << 11)) & prune_mask
    return n

def prng(n, count):
    for _ in range(count):
        n = prng_next(n)
    return n

def hash_sequence(sequence):
    v = 0
    for s in sequence:
        v |= s + 10
        v <<= 5
    return v

def compute_profits(n, count):
    profits = {}
    sequence = []
    last_price = 0
    for i in range(count):
        
        price = n % 10
        delta = price - last_price

        if i > 3:
            sequence = sequence[1:] + [delta]
            
            hash = hash_sequence(sequence)
            if hash not in profits:
                profits[hash] = price

        else:
            sequence += [delta]

        last_price = price
        n = prng_next(n)
    return profits

def max_profit(secrets, count):
    totals = {}
    for n in secrets:
        profits = compute_profits(n, count)

        for hash, price in profits.items():
            if hash not in totals:
                totals[hash] = 0
            totals[hash] += price
    return max(totals.values())

if __name__ == "__main__":
    secrets = load_input()
    print( f"part1: {sum(prng(n, 2000) for n in secrets)}" )
    print( f"part2: {max_profit(secrets, 2000)}" )
