from card_utils import is_soft_hand

I_HARD_HAND_OFFSET = 4
J_HARD_HAND_OFFSET = 2

I_SOFT_HAND_OFFSET = 13
J_SOFT_HAND_OFFSET = 2

I_SPLIT_HAND_OFFSET = 2
J_SPLIT_HAND_OFFSET = 2

BASIC_STRATEGY_GRID_HARD_HANDS = [
    # Dealer upcard
    #"2", "3", "4", "5", "6", "7", "8", "9", "10", "11"
    ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 4 T
    ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 5 O
    ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 6 T
    ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 7 A
    ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 8 L
    ["H", "D", "D", "D", "D", "H", "H", "H", "H" , "H" ], # 9
    ["D", "D", "D", "D", "D", "D", "D", "D", "H" , "H" ], # 10
    ["D", "D", "D", "D", "D", "D", "D", "D", "D" , "D" ], # 11
    ["H", "H", "S", "S", "S", "H", "H", "H", "H" , "H" ], # 12
    ["S", "S", "S", "S", "S", "H", "H", "H", "H" , "H" ], # 13
    ["S", "S", "S", "S", "S", "H", "H", "H", "H" , "H" ], # 14
    ["S", "S", "S", "S", "S", "H", "H", "H", "H" , "H" ], # 15
    ["S", "S", "S", "S", "S", "H", "H", "H", "H" , "H" ], # 16
    ["S", "S", "S", "S", "S", "S", "S", "S", "S" , "S" ], # 17
    ["S", "S", "S", "S", "S", "S", "S", "S", "S" , "S" ], # 18
    ["S", "S", "S", "S", "S", "S", "S", "S", "S" , "S" ], # 19
    ["S", "S", "S", "S", "S", "S", "S", "S", "S" , "S" ], # 20
    ["S", "S", "S", "S", "S", "S", "S", "S", "S" , "S" ], # 21
]

BASIC_STRATEGY_GRID_SOFT_HANDS = [
    # Dealer upcard
    #"2" , "3" , "4" , "5" , "6" , "7", "8", "9", "10", "11"
    ["H" , "H" , "H" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 12 # AA
    ["H" , "H" , "H" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 13 T
    ["H" , "H" , "H" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 14 O
    ["H" , "H" , "D" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 15 T
    ["H" , "H" , "D" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 16 A
    ["H" , "D" , "D" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 17 L
    ["Ds", "Ds", "Ds", "Ds", "Ds", "S", "S", "H", "H" , "H" ], # 18
    ["S" , "S" , "S" , "S" , "Ds", "S", "S", "S", "S" , "S" ], # 19
    ["S" , "S" , "S" , "S" , "S" , "S", "S", "S", "S" , "S" ], # 20
    ["S" , "S" , "S" , "S" , "S" , "S", "S", "S", "S" , "S" ], # 21
]

BASIC_STRATEGY_GRID_SPLIT_HANDS = [
    # Dealer upcard
    #"2"  , "3"  , "4" , "5"   , "6"   , "7", "8", "9", "10", "11"
    ["Y/N", "Y/N", "Y" , "Y"   , "Y"   , "Y", "N", "N", "N" , "N" ], # 2 P
    ["Y/N", "Y/N", "Y" , "Y"   , "Y"   , "Y", "N", "N", "N" , "N" ], # 3 A
    ["N"  , "N"  , "N" , "Y/N" , "Y/N" , "N", "N", "N", "N" , "N" ], # 4 I
    ["N"  , "N"  , "N" , "N"   , "N"   , "N", "N", "N", "N" , "N" ], # 5 R
    ["Y/N", "Y"  , "Y" , "Y"   , "Y"   , "N", "N", "N", "N" , "N" ], # 6 
    ["Y"  , "Y"  , "Y" , "Y"   , "Y"   , "Y", "N", "N", "N" , "N" ], # 7
    ["Y"  , "Y"  , "Y" , "Y"   , "Y"   , "Y", "Y", "Y", "Y" , "Y" ], # 8
    ["Y"  , "Y"  , "Y" , "Y"   , "Y"   , "N", "Y", "Y", "N" , "N" ], # 9
    ["N"  , "N"  , "N" , "N"   , "N"   , "N", "N", "N", "N" , "N" ], # 10
    ["Y"  , "Y"  , "Y" , "Y"   , "Y"   , "Y", "Y", "Y", "Y" , "Y" ], # 11
]



class Player:
    def get_bet(self, bank):
        return 1


    def want_split(self, cards, dealer_upcard):
        return False


    def want_double(self, cards, dealer_upcard):
        hand_total = sum(cards)

        if is_soft_hand(cards):
            action = BASIC_STRATEGY_GRID_SOFT_HANDS[hand_total - I_SOFT_HAND_OFFSET][dealer_upcard - J_SOFT_HAND_OFFSET]
        else:
            action = BASIC_STRATEGY_GRID_HARD_HANDS[hand_total - I_HARD_HAND_OFFSET][dealer_upcard - J_HARD_HAND_OFFSET]

        if action == 'D' or action == 'Ds':
            return True
        else:
            return False


    def want_hit(self, cards, dealer_upcard):
        hand_total = sum(cards)

        print(f"hand_total: {hand_total}, dealer_upcard: {dealer_upcard}")

        if is_soft_hand(cards):
            action = BASIC_STRATEGY_GRID_SOFT_HANDS[hand_total - I_SOFT_HAND_OFFSET][dealer_upcard - J_SOFT_HAND_OFFSET]
        else:
            action = BASIC_STRATEGY_GRID_HARD_HANDS[hand_total - I_HARD_HAND_OFFSET][dealer_upcard - J_HARD_HAND_OFFSET]

        print(f"Action: {action}")
        if action == "D" or action == "H":
            return True
        elif action == "Ds" or action == "S":
            return False

