import re

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return f.read()
    
def get_pairs(text):
    return ((int(a), int(b)) for a,b in re.findall( r"mul\(([0-9]+),([0-9]+)\)", text ))

def sum_products(pairs):
    return sum( a*b for a,b in pairs )

def get_enabled_pairs(text):
    enabled = True
    while True:
        match = re.search( r"mul\(([0-9]+),([0-9]+)\)|don't\(\)|do\(\)", text )
        if match == None:
            break
        
        start, end = match.span()
        item = text[start:end]
        if item == "do()":
            enabled = True
        elif item == "don't()":
            enabled = False
        elif enabled:
            a,b = match.groups()
            yield int(a), int(b)

        text = text[end:]


if __name__ == "__main__":
    text = load_input()
    print( f"part1: {sum_products(get_pairs(text))}" )
    print( f"part2: {sum_products(get_enabled_pairs(text))}" )
