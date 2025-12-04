import math

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        times = [int(n) for n in f.readline().split(':')[1].split()]
        distances = [int(n) for n in f.readline().split(':')[1].split()]
        return list(zip(times, distances))
        
def multiply(values):
    total = 1
    for v in values:
        total *= v
    return total

def quadratic(a, b, c):
    center = math.sqrt(b**2 - (4*a*c))
    return (
        (-b + center) / (2*a),
        (-b - center) / (2*a)
    )

def ways_to_win(race):
    time, record = race

    # Note: record +1, because we need to beat the record.
    
    # (time - x) * x = record + 1
    # -x^2 + time*x - record = 0
    
    a, b = quadratic(-1, time, -(record+1))

    # Find the valid integer ranges (inclusive)
    return math.floor(b) - math.ceil(a) + 1

def join_races(races):
    # I could have just loaded my input correctly. Sue me.
    t = ""
    d = ""
    for time, distance in races:
        t += str(time)
        d += str(distance)
    return int(t), int(d)

if __name__ == "__main__":
    races = load_input()
    print(f"part1: {multiply(ways_to_win(race) for race in races)}")
    print(f"part2: {ways_to_win(join_races(races))}")
