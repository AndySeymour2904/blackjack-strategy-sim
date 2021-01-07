I_HARD_HAND_OFFSET = 4
J_HARD_HAND_OFFSET = 2

I_SOFT_HAND_OFFSET = 12
J_SOFT_HAND_OFFSET = 2

class Player:
    def __init__(self):
        self.bank = 0
        self.bet = 0

        self.basic_strategy_grid_hard_hands = [
            #"2", "3", "4", "5", "6", "7", "8", "9", "10", "11"
            ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 4
            ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 5
            ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 6
            ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 7
            ["H", "H", "H", "H", "H", "H", "H", "H", "H" , "H" ], # 8
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

        self.basic_strategy_grid_soft_hands = [
            #"2" , "3" , "4" , "5" , "6" , "7", "8", "9", "10", "11"
            ["H" , "H" , "H" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 12 # AA
            ["H" , "H" , "H" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 13
            ["H" , "H" , "H" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 14
            ["H" , "H" , "D" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 15
            ["H" , "H" , "D" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 16
            ["H" , "D" , "D" , "D" , "D" , "H", "H", "H", "H" , "H" ], # 17
            ["Ds", "Ds", "Ds", "Ds", "Ds", "S", "S", "H", "H" , "H" ], # 18
            ["S" , "S" , "S" , "S" , "Ds", "S", "S", "S", "S" , "S" ], # 19
            ["S" , "S" , "S" , "S" , "S" , "S", "S", "S", "S" , "S" ], # 20
            ["S" , "S" , "S" , "S" , "S" , "S", "S", "S", "S" , "S" ], # 21
        ]


    def dealt(self, cards):
        self.cards = cards
        self.aces = len([card for card in self.cards if card == 11])
        self.result = 0
        self.has_doubled = False

        self.process_hand()

        self.blackjack = self.hand_total == 21


    def wager(self, bet):
        self.bet = bet
        self.bank = self.bank - self.bet


    def double_down(self):
        self.bank = self.bank - self.bet
        self.bet = self.bet * 2
        self.has_doubled = True


    def win(self):

        if self.blackjack:
            self.bank = self.bank + 3 * self.bet / 2
        else:
            self.bank = self.bank + 2 * self.bet

        self.bet = 0


    def push(self):
        self.bank = self.bank + self.bet
        self.bet = 0


    def is_soft_hand(self):
        return self.aces > 0


    def process_hand(self):
        if sum(self.cards) > 21:
            self.aces = len([card for card in self.cards if card == 11])

            if self.aces > 0:
                self.cards[self.cards.index(11)] = 1
            else:
                self.result = -1

        self.hand_total = sum(self.cards)

        if self.has_doubled:
            self.result = self.hand_total


    def play(self, shoe, dealer_upcard):
    
        self.wager(1)

        while not self.result:

            if self.is_soft_hand():
                action = self.basic_strategy_grid_soft_hands[self.hand_total - I_SOFT_HAND_OFFSET][dealer_upcard - J_SOFT_HAND_OFFSET]
            else:
                action = self.basic_strategy_grid_hard_hands[self.hand_total - I_HARD_HAND_OFFSET][dealer_upcard - J_HARD_HAND_OFFSET]

            
            print(f"Total: {self.hand_total}, Cards: {self.cards}, Dealer upcard: {dealer_upcard}, Action: {action}")

            if action == "D":
                if len(self.cards) == 2:
                    self.double_down()
                    self.cards.append(shoe.draw())
                    self.process_hand()
                else:
                    action = "H"
                    print("Unable to D, doing H")
            elif action == "Ds":
                if len(self.cards) == 2:
                    self.double_down()
                    self.cards.append(shoe.draw())
                    self.process_hand()
                else:
                    action = "S"
                    print("Unable to D, doing S")


            if action == "H":
                self.cards.append(shoe.draw())
            elif action == "S":
                self.result = self.hand_total

            self.process_hand()


        return self.result
