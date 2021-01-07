class Dealer:
    def dealt(self, cards):
        self.cards = cards
        self.aces = len([card for card in self.cards if card == 11])
        self.result = 0

        self.process_hand()


    def process_hand(self):
        if sum(self.cards) > 21:
            self.aces = len([card for card in self.cards if card == 11])

            if self.aces > 0:
                self.cards[self.cards.index(11)] = 1
            else:
                self.result = -1

        self.hand_total = sum(self.cards)


    @property
    def upcard(self):
        return self.cards[0]


    def play(self, shoe):
        while not self.result:

            if self.hand_total < 17:
                self.cards.append(shoe.draw())
            else:
                self.result = self.hand_total
            
            self.process_hand()

        return self.result
