
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        groups = [s.strip() for s in f.readline().split(',')]
        f.readline()
        goals = [s.strip() for s in f.readlines()]
        return groups, goals

def count_designs(goal, groups, memo, index = 0):
    if index == len(goal):
        return 1
    
    remaining = goal[index:]
    if remaining in memo:
        return memo[remaining]

    total = 0
    for group in groups:
        if goal[index:index+len(group)] == group:
            total += count_designs(goal, groups, memo, index + len(group))

    memo[remaining] = total
    return total

if __name__ == "__main__":
    groups, goals = load_input()
    designs = tuple(count_designs(goal, groups, {}) for goal in goals)
    print( f"part1: {sum(count > 0 for count in designs)}" )
    print( f"part2: {sum(designs)}" )
