
def load_rules(f):
    rules = []
    for line in f:
        if line == "\n":
            break
        items = line.split('|')
        rules.append( (int(items[0]), int(items[1])) )
    return rules

def load_sequences(f):
    sequences = []
    for line in f:
        sequences.append( [int(x) for x in line.split(',')] )
    return sequences

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        rules = load_rules(f)
        sequences = load_sequences(f)
    return rules, sequences

def verify_rule(sequence, rule):
    first, second = rule
    second_seen = False
    for i in sequence:
        if i == first and second_seen:
            return False
        if i == second:
            second_seen = True
    return True

def verify_sequence(sequence, rules):
    return all( verify_rule(sequence, rule) for rule in rules )

def get_middle_page(sequence):
    return sequence[len(sequence) // 2]

def fix_sequence(sequence, rules):
    solved = False
    while not solved:
        solved = True
        for rule in rules:
            first, second = rule
            if first in sequence and second in sequence:
                first_i = sequence.index(first)
                second_i = sequence.index(second)
                if first_i > second_i:
                    sequence[first_i] = second
                    sequence[second_i] = first
                    solved = False
    return sequence

def split_sequences(sequences, rules):
    fixed = []
    broken = []
    for s in sequences:
        (fixed if verify_sequence(s, rules) else broken).append(s)
    return fixed, broken

if __name__ == "__main__":
    rules, sequences = load_input()
    fixed, broken = split_sequences(sequences, rules)
    print( f"part1: {sum( get_middle_page(s) for s in fixed) }" )
    print( f"part2: {sum( get_middle_page(fix_sequence(s, rules)) for s in broken) }" )
