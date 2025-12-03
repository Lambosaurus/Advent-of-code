

def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f:
            numbers = line.split(':')[1]
            yield [[int(n) for n in block.strip().split()] for block in numbers.split('|')]

def count_winners(card):
    winners, numbers = card
    return sum( int(n in winners) for n in numbers )

def score(card):
    n = count_winners(card)
    if n == 0:
        return 0
    return 1 << (n - 1)

def score_instances(cards):
    instances = [1] * len(cards)

    for i, card in enumerate(cards):
        n = count_winners(card)
        for j in range(n):
            instances[i + 1 + j] += instances[i]

    return sum(instances)


if __name__ == "__main__":
    cards = list(load_input('input.txt'))
    print(f"part1: {sum(score(card) for card in cards)}")
    print(f"part2: {score_instances(cards)}")
