
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return ((line.strip().split('-')) for line in f.readlines())

def hash_node(name):
    return (ord(name[0]) << 8) | ord(name[1])

def get_node_name(node):
    return chr((node >> 8) & 0xFF) + chr((node) & 0xFF)

def build_links(pairs):
    links = {}
    for node_a,node_b in pairs:
        a = hash_node(node_a)
        b = hash_node(node_b)

        if a not in links:
            links[a] = []
        links[a].append(b)
        if b not in links:
            links[b] = []
        links[b].append(a)
    
    for set in links.values():
        set.sort()
    return links

def find_triples(links):
    for a in sorted(links.keys(), reverse=True):
        for b in links[a]:
            # a is counting down, so we stop once we hit a to prevent duplicates
            if b > a:
                break

            for c in links[b]:
                # nested triangular search
                if c > b:
                    continue

                if c in links[a]:
                    yield a,b,c

def target_set(set):
    # Nodes that match "t*"
    match, mask = hash_node("t\x00"), hash_node("\xFF\x00")
    for node in set:
        if (node & mask) == match:
            return True
    return False

def max_subsets(links, sequence, whitelist):
    best_sequence = sequence

    for _ in range(len(whitelist)):
        node = whitelist.pop()

        sublist = list(n for n in whitelist if n in links[node])
        candidate = max_subsets(links, sequence + [node], sublist )
        if len(candidate) > len(best_sequence):
            best_sequence = candidate

    return best_sequence

def format_sequence(nodes):
    return ",".join( get_node_name(n) for n in sorted(nodes) )

if __name__ == "__main__":
    pairs = load_input()
    links = build_links(pairs)
    print( f"part1: {sum(target_set(s) for s in find_triples(links))}" )
    print( f"part2: {format_sequence(max_subsets(links, [], list(links.keys())))}" )
