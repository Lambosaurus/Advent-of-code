import random

def load_state(f):
    states = {}
    line = f.readline()
    while line != "\n":
        id, value = line.split(": ")
        states[id] = bool(int(value))
        line = f.readline()
    return states

def load_gates(f):
    gates = {}
    for line in f.readlines():
        expr, id = line.strip().split(" -> ")
        a, op, b = expr.split(" ")
        gates[id] = (op, a, b)
    return gates

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        states = load_state(f)
        gates = load_gates(f)
        return states, gates
    
def read_state(states, gates, key):
    if key in states:
        return states[key]
    op,a,b = gates[key]

    if op == "OR":
        r = read_state(states, gates, a) or read_state(states, gates, b)
    elif op == "AND":
        r = read_state(states, gates, a) and read_state(states, gates, b)
    else: # op == "XOR"
        r = read_state(states, gates, a) != read_state(states, gates, b)
    
    states[key] = r
    return r

def register_size(states, gates, prefix):
    for i in range(128):
        key = f"{prefix}{i:02}"
        if not ((key in states) or (key in gates)):
            return i

def read_register(states, gates, prefix, bits = None):
    if bits == None:
        bits = register_size(states, gates, prefix)
    r = 0
    for i in range(bits):
        if read_state(states, gates, f"{prefix}{i:02}"):
            r |= 1 << i
    return r

def write_register(states, prefix, r, bits):
    for i in range(bits):
        states[f"{prefix}{i:02}"] = (r & (1 << i)) != 0
        
def evaluate_adder_single(gates, bits, x, y, carry_bit = True):
    states = {}
    write_register(states, 'x', x, bits)
    write_register(states, 'y', y, bits)
    
    if carry_bit:
        z = read_register(states, gates, 'z', bits + 1)
        return x + y == z
    else:
        z = read_register(states, gates, 'z', bits)
        return ((x + y) & ((1 << bits) - 1)) == z

def evaluate_adder(gates, bits, carry_bit = True, tests = 100):
    for _ in range(tests):
        x = random.randint(0, (1 << bits) - 1)
        y = random.randint(0, (1 << bits) - 1)
        if not evaluate_adder_single(gates, bits, x, y, carry_bit):
            return False
    return True

def apply_swaps(gates, swaps):
    gates = dict(gates)
    for a,b in swaps:
        tmp = gates[a]
        gates[a] = gates[b]
        gates[b] = tmp
    return gates

def find_gate(gates, output = None, input_a = None, input_b = None, operation = None):
    if output == None:
        for output in gates:
            op,a,b = gates[output]
            if operation != None and op != operation:
                continue
            if input_a != None and not (a == input_a or b == input_a):
                continue
            if input_b != None and not (a == input_b or b == input_b):
                continue
            break
    op,a,b = gates[output]
    print(f"{a} {op} {b} -> {output}")
    return op,a,b,output

def debug_adder(gates):
    bits = register_size(states, gates, 'z') - 1
    for i in range(bits):
        if not evaluate_adder(gates, i + 1, i == (bits - 1)):

            xi,yi,zi = (f"{prefix}{i:02}" for prefix in "xyz")
            print(f"Error at bit {i}")
            op,a,b,o = find_gate(gates,output=zi)
            find_gate(gates,output=a)
            find_gate(gates,output=b)
            op,a,b,o = find_gate(gates,input_a=xi,input_b=yi,operation="XOR")
            find_gate(gates,input_a=o)
            op,a,b,o = find_gate(gates,input_a=xi,input_b=yi,operation="AND")
            find_gate(gates,input_a=o)

            return False
    return True

def format_swaps(swaps):
    swaps = [s for pair in swaps for s in pair]
    return ",".join(sorted(swaps))

def check_swaps(gates, swaps):
    gates = apply_swaps(gates, swaps)
    return debug_adder(gates)

SWAPS = []

if __name__ == "__main__":
    states, gates = load_input()
    print( f"part1: {read_register(states, gates, 'z')}" )
    print( f"part2: {format_swaps(SWAPS) if check_swaps(gates, SWAPS) else 'swap sequence not valid'}")

