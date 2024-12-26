

def load_input(fname = "input.txt"):
    list_a = []
    list_b = []
    with open(fname, 'r') as f:
        for line in f:
            a,b = (int(s) for s in line.split('   '))
            list_a.append(a)
            list_b.append(b)
    return list_a, list_b

def count(sequence):
    return sum(int(s) for s in sequence)

def compare_differences(list_a, list_b):
    list_a.sort()
    list_b.sort()
    return sum( abs(b - a) for a,b in zip(list_a, list_b) )

def compare_occurrances(list_a, list_b):
    return sum( a * count(b == a for b in list_b) for a in list_a )

if __name__ == "__main__":

    list_a, list_b = load_input()
    print(f"part1: {compare_differences(list_a, list_b)}")
    print(f"part2: {compare_occurrances(list_a, list_b)}")
