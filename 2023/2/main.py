
COLORS = ("red", "green", "blue")

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f:
            game, samples = line.split(':')
            game_id = int(game.split(' ')[1])
            
            sets = []
            for sample in samples.split(';'):
                rgb = [0,0,0]
                for pair in sample.split(','):
                    n,c = pair.strip().split(' ')
                    rgb[ COLORS.index(c) ] = int(n)
                sets.append(rgb)

            yield game_id, sets

def is_game_possible( bag, sets ):
    return all( all(a >= b for a,b in zip(bag, set)) for set in sets )

def minimum_cube_set( sets ):
    return tuple( max(set[i] for set in sets) for i in range(3) )

def power( bag ):
    return bag[0] * bag[1] * bag[2]

if __name__ == "__main__":
    games = list(load_input())
    print(f"part1: {sum( game_id for game_id, sets in games if is_game_possible((12, 13, 14), sets) )}")
    print(f"part2: {sum( power(minimum_cube_set(sets)) for game_id, sets in games )}")
