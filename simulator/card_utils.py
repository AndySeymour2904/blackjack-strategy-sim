def is_blackjack(cards):
    return len(cards) == 2 and sum(cards) == 21


def is_pair(cards):
    return len(cards) == 2 and cards[0] == cards[1]


def is_soft_hand(cards):
    return len([card for card in cards if card == 11]) > 0

def get_count_for_card(card):
    # Hi-Lo strategy for counting cards
    if card < 7:
        return 1
    elif card > 9:
        return -1
    else:
        return 0
