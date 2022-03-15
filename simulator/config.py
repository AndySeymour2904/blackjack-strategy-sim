DECKS = 6
DECK_PENETRATION = 0.75

IS_INFINITE_SHOE = True

BET = 1

# Will only force the card if it is in the shoe
FORCE_PLAYER_CARD_1 = False # int (card) or False
FORCE_PLAYER_CARD_2 = False # int (card) or False
FORCE_DEALER_UPCARD = False # int (card) or False
FORCE_DEALER_DOWNCARD = False # int (card) or False

DEALER_STAND_THRESHOLD = 17
DEALER_HITS_SOFT_STAND_THRESHOLD = False

def BET_MULTIPLIER_FUNC(true_count):
	# if true_count < 2:
	# 	return 1

	# return 10 * round(true_count)

	return 1
	

CAN_SPLIT_ACES = True
CAN_PLAY_SPLIT_ACES = False

DOUBLE_AFTER_SPLIT = True

BLACKJACK_PAY_AMOUNT = 1.5

MAX_SPLITS = 3

# insurance offered?

# min bet
# max bet