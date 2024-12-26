
def load_register(f):
    return int(f.readline().split(':')[1])

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        registers = [load_register(f) for _ in range(3)]
        f.readline()
        program = [int(n) for n in f.readline().split(':')[1].split(',')]
        return registers, program

def decode_combo_operand(operand, registers):
    if operand <= 3:
        return operand
    if operand <= 7:
        return registers[operand-4]
    raise Exception("Invalid operand")

def run_instruction(program, registers, ipr):
    opcode = program[ipr]
    operand = program[ipr + 1]
    output = None
    ipr += 2

    if opcode == 0: # adv
        operand = decode_combo_operand(operand, registers)
        registers[0] //= (1 << operand)
    
    elif opcode == 1: # bxl
        registers[1] ^= operand

    elif opcode == 2: # bst
        operand = decode_combo_operand(operand, registers)
        registers[1] = operand & 7

    elif opcode == 3: # jnz
        if registers[0]:
            ipr = operand
        
    elif opcode == 4: # bxc
        registers[1] ^= registers[2]

    elif opcode == 5: # out
        operand = decode_combo_operand(operand, registers)
        output = operand & 7

    elif opcode == 6: # bdv
        operand = decode_combo_operand(operand, registers)
        registers[1] = registers[0] // (1 << operand)

    elif opcode == 7: # cdv
        operand = decode_combo_operand(operand, registers)
        registers[2] = registers[0] // (1 << operand)

    return ipr, output

def run_program(program, registers):
    ipr = 0
    while ipr < len(program) - 1:
        ipr, output = run_instruction(program, registers, ipr)
        if output != None:
            yield output

def format_output(output):
    return ",".join( str(n) for n in output )

def output_compare(program, output):
    output = iter(output)
    matches = 0
    for n in program:
        result = next(output, None)
        if result != n:
            return matches
        matches += 1
    if next(output, None) != None:
        matches += 1
    return matches

def crack_digit(program, step_bits, check_bits, digit = 1, prefix = 0):
    prefix_bits = (digit - 1) * step_bits

    for i in range(1 << step_bits):
        candidate_prefix = prefix | (i << prefix_bits)
        for j in range(1 << (check_bits - step_bits)):

            n = candidate_prefix | (j << (prefix_bits + step_bits))
            matches = output_compare(program, run_program(program, [n, 0, 0]))
            
            if digit == len(program):
                # Success criteria
                if matches == digit:
                    return n
                
            elif matches >= digit:
                # We got a digit. Now advance.
                child = crack_digit(program, step_bits, check_bits, digit + 1, candidate_prefix)
                if child != None:
                    return child
                break # Do not check this prefix again.
    return None

INSTR_NAMES = [ "adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv" ]
COMBO_NAMES = [ "0", "1", "2", "3", "A", "B", "C" ]

def print_program(program):
    for i in range(0, len(program), 2):
        opcode = program[i]
        operand = program[i+1]
        if not opcode in [1, 3, 4]:
            operand = COMBO_NAMES[operand]
        print(f"{i:02}: {INSTR_NAMES[opcode]} {operand}")

if __name__ == "__main__":
    registers, program = load_input()
    #print_program(program)
    print( f"part1: {format_output(run_program(program, registers))}" )
    print( f"part2: {crack_digit(program, 3, 10)}" )
    