import re

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            lights, buttons, joltage = re.match(r"\[(.+)\] (.+) \{(.+)\}", line).groups()
            lights = sum((c == '#') << i for i,c in enumerate(lights))
            joltage = tuple(int(n) for n in joltage.split(','))
            buttons = tuple(
                sum( (1 << int(n)) for n in m.split(',') )
                for m in re.findall(r"\(([^\)]+)\)", buttons)
            )
            # lights and buttons are expressed as a bitmask.
            yield lights, buttons, joltage

def min_button_presses(goal, buttons):
    # This is just A*

    # Heuristic is the minimum theoretical number of state transitions needed
    max_toggles = max( b.bit_count() for b in buttons )
    def heuristic(state):
        return (state ^ goal).bit_count() / max_toggles

    frontier = { 0: heuristic(0) }
    explored = { 0: (0, None) } # (cost, prior)

    while len(frontier):
        # Get best candidate node
        src_state, _ = min(frontier.items(), key = lambda k: k[1] )
        del frontier[src_state]
        src_cost, _ = explored[src_state]

        for button in buttons:
            dst_cost = src_cost + 1
            dst_state = src_state ^ button

            if dst_state == goal:
                return dst_cost 

            if (not dst_state in explored) or (dst_cost < explored[dst_state][0]):
                explored[dst_state] = (dst_cost, src_state)
                if not dst_state in frontier:
                    frontier[dst_state] = dst_cost + heuristic(dst_state)


def min_joltage_presses(joltage, buttons):
    return 0


if __name__ == "__main__":
    machines = list(load_input('input.txt'))
    print(f"part1: {sum(min_button_presses(l,b) for l,b,j in machines)}")
    print(f"part2: {sum(min_joltage_presses(j,b) for l,b,j in machines)}")
