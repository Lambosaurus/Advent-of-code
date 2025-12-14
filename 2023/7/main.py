
def load_input(fname = "input.txt"):
    with open(fname, 'r') as f:
        for line in f.readlines():
            hand, bid = line.split()
            yield hand, int(bid)

def count_cards(hand, card):
    return sum( c == card for c in hand )

def organise_hand(hand):
    # convert the hand into a dict of [card]: count.
    d = {}
    for c in hand:
        if not c in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

def hand_type_rank(hand, jokers = False):
    groups = organise_hand(hand)

    joker_count = 0
    if jokers and 'J' in groups:
        joker_count = groups.pop('J')

    counts = list(sorted((v for v in groups.values()), reverse=True)) + [0, 0]
    counts[0] += joker_count # Add jokers to biggest group

    return (counts[0] << 4) | counts[1]

def score_hand(hand, jokers = False):
    card_order = "J23456789TQKA" if jokers else "23456789TJQKA"

    # 5 cards of 4 bit ranks (20 bits)
    total = 0
    for card in hand:
        total <<= 4
        total |= card_order.index(card)
    
    # rank stored in top bits
    total |= hand_type_rank(hand, jokers) << 20
    return total

def total_winnings(hands, jokers = False):
    scored_hands = ((score_hand(hand, jokers), hand, bid) for hand, bid in hands)
    scored_hands = sorted(scored_hands, key=lambda x: x[0], reverse=False)
    return sum( ((i+1) * bid) for i, (_, _, bid) in enumerate(scored_hands) ) 

if __name__ == "__main__":
    hands = list(load_input())
    print(f"part1: {total_winnings(hands)}")
    print(f"part2: {total_winnings(hands, True)}")
