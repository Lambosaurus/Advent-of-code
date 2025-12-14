import re
import math

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        pattern = f.readline().strip()
        f.readline() # whitespace

        nodes = {}
        for line in f.readlines():
            node, left, right = re.match(r"(\w+) = \((\w+), (\w+)\)", line).groups()
            nodes[node] = (left, right)
        return pattern, nodes

def travel(nodes, node, pattern, offset):
    return nodes[node][int(pattern[offset] == 'R')]

def count_steps(nodes, pattern):
    node = "AAA"
    steps = 0
    while node != 'ZZZ':
        node = travel(nodes, node, pattern, steps % len(pattern))
        steps += 1
    return steps

def hash(node, offset):
    return node + str(offset)

def get_loop(nodes, node, pattern):
    step = 0
    offset = 0
    destinations = []
    history = {}
    while 1:
        if node[2] == 'Z':
            destinations.append(step)

        x = hash(node, offset)
        if x in history:

            # Staggeringly critical assumption here!!!
            # All destinations are evenly spaced.
            # This is not at all guaranteed by the problem.
            loop_start = history[x]
            loop_size = (len(history) - loop_start) // len(destinations)
            destination_step = destinations[0]
            return destination_step, loop_size
        else:
            history[x] = step
            node = travel(nodes, node, pattern, offset)
            step += 1
            offset = step % len(pattern)

def align_loops(a, b):
    a_start, a_period = a
    b_start, b_period = b
    
    c_start = a_start
    c_period = math.lcm(a_period, b_period)

    while c_start < b_start:
        c_start += a_period

    while (c_start - b_start) % b_period != 0:
        c_start += a_period

    return c_start, c_period
    
def count_steps_simultaneous(nodes, pattern):
    frontier = (node for node in nodes if (node[2] == 'A'))
    p = 0, 1 # the identify loop.
    for node in frontier:
        p = align_loops(p, get_loop(nodes, node, pattern))
    return p[0]


if __name__ == "__main__":
    pattern, nodes = load_input()
    print(f"part1: {count_steps(nodes, pattern)}")
    print(f"part2: {count_steps_simultaneous(nodes, pattern)}")
