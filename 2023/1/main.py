

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f:
            yield line.strip()


def first_digit(line: str) -> str:
    for c in line:
        if c >= '0' and c <= '9':
            return c

def get_calibration(line: str):
    return int(first_digit(line) + first_digit(reversed(line)))

def get_word_index(line: str, word: str) -> int:
    try:
        return line.index(word)
    except:
        return 0x7FFFFFFF
    
def reverse_str(s: str) -> str:
    return "".join(reversed(s))

def get_calibration_spelled(line: str) -> int:
    # What was I even thinking?
    # I cant even process how dumb this is.

    names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    digits = "0123456789"
    options = list(enumerate(names)) + list(enumerate(digits))
    
    first_digit, pos = min(options, key=lambda o: get_word_index(line, o[1]))
    
    line = reverse_str(line)
    last_digit, pos = min(options, key=lambda o: get_word_index(line, reverse_str(o[1])))

    return first_digit * 10 + last_digit


if __name__ == "__main__":
    lines = list(load_input())
    print(f"part1: {sum(get_calibration(line) for line in lines)}")
    print(f"part2: {sum(get_calibration_spelled(line) for line in lines)}")
