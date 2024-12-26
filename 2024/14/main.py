def parse_v2(text):
    return tuple(int(s) for s in text.split('=')[1].split(','))

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            yield tuple(parse_v2(s) for s in line.split(' '))

def predict_robot(size, pos, velocity, t):
    x,y = pos
    dx,dy = velocity
    x += dx * t
    y += dy * t
    x %= size[0]
    y %= size[1]
    return x,y

def predict_robots(size, robots, t):
    return (predict_robot(size, pos, vel, t) for pos,vel in robots)

def contained_points(rect, positions):
    xl,yl,xh,yh = rect
    return sum(int(x >= xl and x <= xh and y >= yl and y <= yh) for x,y in positions)

def get_safety_factor(size, robots, t):
    positions = list(predict_robots(size, robots, t))

    xmid = size[0] // 2
    ymid = size[1] // 2
    sectors = [
        (0      ,0      ,xmid-1,    ymid-1),
        (xmid+1 ,0      ,size[0],   ymid-1),
        (0      ,ymid+1 ,xmid-1,    size[1]),
        (xmid+1 ,ymid+1 ,size[0],   size[1]),
    ]

    product = 1
    for sector in sectors:
        product *= contained_points(sector, positions)
    return product

def new_map(size, v):
    return [ [v] * size[0] for _ in range(size[1]) ]

def map_robots(size, positions):
    map = new_map(size, 0)
    for x,y in positions:
        map[y][x] += 1
    return map

def print_map(map):
    for row in map:
        print( "".join( '.' if c == 0 else str(c) for c in row ) )

def find_maximum(x_axis, y_func): 
    x_axis = iter(x_axis)
    best_x = next(x_axis)
    best_y = y_func(best_x)
    for x in x_axis:
        y = y_func(x)
        if y > best_y:
            best_y = y
            best_x = x
    return best_x, best_y

def find_grouping(size, robots, sector = (30,31,71,72), maxt = 10000):
    t,score = find_maximum(range(maxt),
        lambda t: contained_points(sector, predict_robots(size, robots, t))
    )
    #print_map( map_robots(size, predict_robots(size, robots, t)) )
    return t
        
if __name__ == "__main__":
    robots = list(load_input())
    size = (101,103)
    print( f"part1: {get_safety_factor(size, robots, 100)}" )
    print( f"part2: {find_grouping(size, robots)}" )
    

