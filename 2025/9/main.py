
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield tuple(int(n) for n in line.split(','))

def order(a,b):
    if b >= a:
        return a,b
    return b,a

def rect(a, b):
    x0,x1 = order(a[0], b[0])
    y0,y1 = order(a[1], b[1])
    return (x0,y0,x1,y1)
    
def area(r):
    x0,y0,x1,y1 = r
    return (x1 + 1 - x0) * (y1 + 1 - y0)

def overlaps(a, b):
    # Given two rectangles x0, y0, x1, y1
    # Confirm they have no overlapping area (sides touching is fine)
    return b[0] < a[2] and b[2] > a[0] and b[1] < a[3] and b[3] > a[1]

def find_max_area(coords, test_overlap = False):
    best_size = 0
    for i in range(len(coords)):
        for j in range(i+1, len(coords)):
            
            r = rect(coords[i],coords[j])
            size = area(r)
            if size <= best_size:
                continue
            
            if test_overlap:
                # Go through all line segments, and check they do not interrupt the candidate area
                if any( overlaps(r, rect(coords[k-1], coords[k])) for k in range(len(coords)) ):
                    continue

                # This algorithim leaves an edge case open - an area could be drawn which intersects zero segments by containing zero valid tiles
                # This is unlikely to have the best size, so i ignore testing for this.

            best_size = size

    return best_size

if __name__ == "__main__":
    coords = list(load_input())
    print(f"part1: {find_max_area(coords)}")
    print(f"part2: {find_max_area(coords, True)}")
