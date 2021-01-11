from shoe import Shoe 
from dealer import Dealer
from player import Player

from card_utils import is_blackjack, is_pair

class Game:
    def __init__(self, hands_to_run):
        self.shoe = Shoe(8, 4)
        self.player = Player()
        self.dealer = Dealer()

        self.hands_to_run = hands_to_run
        self.player_hands = []
        self.player_bank = 0
    
    
    def split_player_hand(self, index):
        return


    def double_player_hand(self, index):
        self.player_hands[index]["cards"].append(self.shoe.draw())
        self.player_bank = self.player_bank - self.player_hands[index]["bet"]

        self.player_hands[index]["bet"] = self.player_hands[index]["bet"] * 2


    def hit_player_hand(self, index):
        self.player_hands[index]["cards"].append(self.shoe.draw())


    def get_player_bet(self):
        player_bet = self.player.get_bet(self.player_bank)
        self.player_bank = self.player_bank - player_bet
        return player_bet


    def player_blackjack(self, index):
        self.player_bank = self.player_bank + self.player_hands[index]["bet"] * 3 / 2


    def player_win(self, index):
        self.player_bank = self.player_bank + self.player_hands[index]["bet"] * 2


    def player_push(self, index):
        self.player_bank = self.player_bank + self.player_hands[index]["bet"]

    
    def should_dealer_play(self):
        # Dealer should not play if all player hands are blackjack or if all player_hands are bust
        for player_hand in self.player_hands:
            if not player_hand["blackjack"] and player_hand["result"] != -1:
                return True

        return False


    def compute_hand(self, index):
        if sum(self.player_hands[index]["cards"]) > 21:
            aces = len([card for card in self.player_hands[index]["cards"] if card == 11])

            if aces > 0:
                self.player_hands[index]["cards"][self.player_hands[index]["cards"].index(11)] = 1
            else:
                print("BUSTING")
                self.player_hands[index]["result"] = -1
                return

        self.player_hands[index]["result"] = sum(self.player_hands[index]["cards"])


    def play_hand(self, index):
        cards = self.player_hands[index]["cards"]
        dealer_upcard = self.dealer.upcard

        if is_blackjack(cards):
            self.player_hands[index]["blackjack"] = True
            return

        if is_pair(cards) and self.player.want_split(cards, dealer_upcard):
            print("SPLIT")
            self.split_player_hand(index)
            self.play_hand(index)
            self.play_hand(index+1)

        
        # Compute the hand now we have offered splits (we can change AA to 12 now and get totals)
        self.compute_hand(index)

        if self.player.want_double(cards, dealer_upcard):
            print("DOUBLE DOWN")
            self.double_player_hand(index)
            self.compute_hand(index)
            return
        

        while self.player_hands[index]["result"] != -1 and self.player.want_hit(self.player_hands[index]["cards"], dealer_upcard):
            print("HIT")
            self.hit_player_hand(index)
            self.compute_hand(index)


    def run(self):
        for i in range(self.hands_to_run):

            print("-------NEW HAND-------")

            player_bet = self.get_player_bet()

            cards = [self.shoe.draw(), self.shoe.draw(), self.shoe.draw(), self.shoe.draw()]

            self.dealer.dealt([cards[1], cards[3]])
            self.player_hands = [
                {"cards": [cards[0], cards[2]], "blackjack": False, "bet": player_bet, "result": 0}
            ]

            self.play_hand(0)

            if self.should_dealer_play():
                self.dealer.play(self.shoe)

            print(f"Dealer: {self.dealer.result}, {self.dealer.cards}")

            for index in range(len(self.player_hands)):

                player_hand = self.player_hands[index]

                print(f'Player: {player_hand["result"]}, {player_hand["cards"]}')

                if player_hand["blackjack"]:
                    self.player_blackjack(index)
                if self.dealer.result < player_hand["result"]:
                    self.player_win(index)
                elif self.dealer.result == player_hand["result"]:
                    self.player_push(index)
                

            print(f"Player bank: {self.player_bank}")
            self.shoe.reset_if_required()


        print(f"Final player bank: {self.player_bank}")
