
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [int(n) for n in f.read().split(' ')]

def new_memo(steps):
    return [{} for _ in range(steps)]

def count_stones_memo(n, steps, memo):

    if steps == 0:
        return 1
    steps -= 1
    
    if n in memo[steps]:
        return memo[steps][n]
    
    strn = str(n)
    if n == 0:
        count = count_stones_memo(1, steps, memo)
    elif len(strn) & 1 == 0:
        half = len(strn)//2
        count = count_stones_memo(int(strn[:half], 10), steps, memo) + count_stones_memo(int(strn[half:], 10), steps, memo)
    else:
        count = count_stones_memo(n * 2024, steps, memo)
    
    memo[steps][n] = count
    return count


if __name__ == "__main__":
    stones = load_input()
    memo = new_memo(75)
    print( f"part1: {sum( count_stones_memo(s, 25, memo) for s in stones )}" )
    print( f"part2: {sum( count_stones_memo(s, 75, memo) for s in stones )}" )