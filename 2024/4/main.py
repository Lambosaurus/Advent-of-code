
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        return [l.strip() for l in f.readlines()]

def check_vector(text, word, row, col, dr, dc):
    for ch in word:
        if text[row][col] != ch:
            return False
        row += dr
        col += dc
    return True

def check_vector_bidir(text, word, row, col, dr, dc):
    # Check forwards direciton
    if check_vector(text, word, row, col, dr, dc):
        return True
    # Now check backwards
    span = len(word) - 1
    return check_vector(text, word, row + dr * span, col + dc * span, -dr, -dc)

def count(sequence):
    return sum(int(s) for s in sequence)

def count_words(text, word):
    rows = len(text)
    cols = len(text[0])
    span = len(word) - 1

    total_words = 0
    
    for dr,dc in ((0,1), (1,1), (1,0), (1,-1)):
        r_min = span if dr < 0 else 0
        r_max = rows - (span if dr > 0 else 0)
        c_min = span if dc < 0 else 0
        c_max = cols - (span if dc > 0 else 0)
        total_words += count(
            check_vector_bidir(text, word, r, c, dr, dc)
                for r in range(r_min,r_max)
                for c in range(c_min,c_max)
        )
            
    return total_words

def check_cross(text, word, row, col, span):
    return check_vector_bidir(text, word, row-span, col-span,  1, 1) \
       and check_vector_bidir(text, word, row+span, col-span, -1, 1)

def count_crosses(text, word):
    rows = len(text)
    cols = len(text[0])
    span = len(word) // 2

    return count(
        check_cross(text, word, r, c, span)
            for r in range(span, rows-span)
            for c in range(span, cols-span)
    )

if __name__ == "__main__":
    text = load_input()
    print(f"part1: {count_words(text, "XMAS")}")
    print(f"part2: {count_crosses(text, "MAS")}")
