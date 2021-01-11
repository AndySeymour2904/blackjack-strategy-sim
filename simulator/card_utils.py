def is_blackjack(cards):
    return len(cards) == 2 and sum(cards) == 21


def is_pair(cards):
    return len(cards) == 2 and cards[0] == cards[1]


def is_soft_hand(cards):
    return len([card for card in cards if card == 11]) > 0