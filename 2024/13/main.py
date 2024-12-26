import re

def to_ints(strings):
    return tuple( int(n) for n in strings )

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        while True:
            da = to_ints(re.match(r"Button A: X\+([0-9]+), Y\+([0-9]+)", f.readline()).groups())
            db = to_ints(re.match(r"Button B: X\+([0-9]+), Y\+([0-9]+)", f.readline()).groups())
            goal = to_ints(re.match(r"Prize: X=([0-9]+), Y=([0-9]+)", f.readline()).groups())

            yield da,db,goal

            if f.readline() != "\n":
                break

def get_cost(da, db, goal, a):
    # First check that [a * da + b * db = goal] holds true for integer math.
    x = a * da[0]
    if (goal[0] - x) % db[0] != 0:
        return None
    b = (goal[0] - x) // db[0]
    if (a * da[1]) + (b * db[1]) != goal[1]:
        return None
    return (a * 3) + (b * 1)

def compute_a(da, db, goal):
    # Given [a * da + b * db = goal], this solves for a.
    ax,ay = da
    bx,by = db
    x,y = goal

    ayx = ay / ax
    b = (y - (x * ayx)) / (by - (bx * ayx))
    a = (x - (b * bx)) / ax
    return a

def get_min_cost(game, offset = 0):
    da, db, goal = game
    if offset:
        goal = (goal[0] + offset, goal[1] + offset)
    return get_cost(da, db, goal, round(compute_a(da, db, goal)))

def sum_valid(values):
    return sum( (v if v != None else 0) for v in values )

if __name__ == "__main__":
    games = list(load_input())
    print( f"part1: {sum_valid(get_min_cost(g) for g in games )}" )
    print( f"part2: {sum_valid(get_min_cost(g, 10000000000000) for g in games )}" )

