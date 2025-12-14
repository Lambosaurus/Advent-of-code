
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield tuple(int(n) for n in line.split(','))

def distance_sq(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2

def shortest_links(coords):
    distances = []
    for i, a in enumerate(coords):
        for j in range(i+1, len(coords)):
            b = coords[j]
            distances.append((distance_sq(a, b), i, j))
    distances.sort(key=lambda x: x[0])
    return distances

def do_joins(coords, limit):
    
    # Start off with each item in its own group
    groups = list(range(len(coords)))
    members = [[i] for i in groups]

    for _, a, b in shortest_links(coords)[:limit]:
        
        ga, gb = groups[a], groups[b]

        if ga == gb:
            continue

        for i in members[gb]:
            groups[i] = ga
        members[ga] += members[gb]
        members[gb] = []
        
        if len(members[ga]) == len(groups):
            break

    return members, coords[a], coords[b]

def join_some(coords, links = 10):
    members, a, b = do_joins(coords, links)
    sizes = sorted((len(m) for m in members), reverse=True)
    return sizes[:3]

def join_all(coords):
    _, a, b = do_joins(coords, -1)
    return a[0] * b[0]

def product(items):
    total = 1
    for item in items:
        total *= item
    return total

if __name__ == "__main__":
    coords = list(load_input())
    print(f"part1: {product(join_some(coords, 1000))}")
    print(f"part2: {join_all(coords)}")
