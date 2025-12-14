
def load_input(fname = "input.txt"):
    nodes = {}
    with open(fname, 'r') as f:
        for line in f.readlines():
            src, dsts = line.split(':')
            dsts = dsts.split()
            nodes[src] = dsts
    return nodes

def reverse_map(node_dst):
    node_src = { n: [] for n in node_dst }
    for node, dsts in node_dst.items():
        for dst in dsts:
            if dst not in node_src:
                # Some nodes (like "out" are not listed.)
                node_src[dst] = []
            node_src[dst].append(node)
    return node_src

def count_paths_from(nodes, dst, src, memo):
    # Search starting from the destination
    if not dst in memo:
        if dst == src:
            memo[dst] = 1
        else:
            memo[dst] = sum(
               count_paths_from(nodes, path, src, memo) for path in nodes[dst]
            )
    return memo[dst]

def pairs(items):
    items = iter(items)
    prior = next(items)
    for item in items:
        yield prior, item
        prior = item

def product(items):
    total = 1
    for item in items:
        total *= item
    return total

def count_paths(nodes, path):
    return product( count_paths_from(nodes, b, a, {}) for a,b in pairs(path) )

if __name__ == "__main__":
    nodes = reverse_map(load_input())
    print(f"part1: {count_paths(nodes, ["you", "out"])}")
    print(f"part2: {count_paths(nodes, ["svr", "fft", "dac", "out"])}")
