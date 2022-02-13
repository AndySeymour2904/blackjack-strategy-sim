from card_utils import is_soft_hand

from config import DEALER_STAND_THRESHOLD, DEALER_HITS_SOFT_STAND_THRESHOLD

class Dealer:
    def dealt(self, cards):
        self.cards = cards
        self.aces = len([card for card in self.cards if card == 11])
        self.result = 0
        self.hand_total = 0

        self.process_hand()

    def has_blackjack(self):
        return sum(self.cards) == 21 and len(self.cards) == 2

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

            # Dealer hits soft 17 or below
            if self.hand_total < DEALER_STAND_THRESHOLD or (DEALER_HITS_SOFT_STAND_THRESHOLD and self.hand_total == DEALER_STAND_THRESHOLD and is_soft_hand(self.cards)):
                self.cards.append(shoe.draw())
            else:
                self.result = self.hand_total
            
            self.process_hand()

        return self.result
