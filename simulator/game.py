from shoe import Shoe 
from dealer import Dealer
from player import Player
from stats import Stats
import logging

from tqdm import tqdm

from card_utils import is_blackjack, is_pair
from config import CAN_PLAY_SPLIT_ACES, CAN_SPLIT_ACES, BLACKJACK_PAY_AMOUNT, MAX_SPLITS

logger = logging.getLogger()

class Game:
    def __init__(self, hands_to_run, should_print_stats):
        self.shoe = Shoe()
        self.player = Player()
        self.dealer = Dealer()

        self.stats = Stats()
        self.should_print_stats = should_print_stats

        self.hands_to_run = hands_to_run
        self.player_hands = []
        self.player_bank = 0

        self.total_player_stake = 0
    
    
    def split_player_hand(self, index):
        cards = self.player_hands[index]["cards"]
        bet = self.player_hands[index]["bet"]

        self.player_hands[index] = {"cards": [cards[0], self.shoe.draw()], "blackjack": False, "bet": bet, "result": 0}
        self.player_hands.insert(index + 1, {"cards": [cards[1], self.shoe.draw()], "blackjack": False, "bet": bet, "result": 0})

        self.player_bank = self.player_bank - bet


    def double_player_hand(self, index):
        self.player_hands[index]["cards"].append(self.shoe.draw())
        self.player_bank = self.player_bank - self.player_hands[index]["bet"]

        self.player_hands[index]["bet"] = self.player_hands[index]["bet"] * 2


    def hit_player_hand(self, index):
        self.player_hands[index]["cards"].append(self.shoe.draw())


    def get_player_bet(self):
        true_count = self.shoe.get_true_count()
        player_bet = self.player.get_bet(true_count)

        logger.debug(f"True count is: {true_count}")
        logger.debug(f"Player bets: {player_bet}")

        self.player_bank = self.player_bank - player_bet

        self.total_player_stake = self.total_player_stake + player_bet

        return player_bet


    def get_player_insurance_bet(self, cards, dealer_upcard):
        player_insurance_bet = self.player.get_insurance_bet(cards, dealer_upcard)

        logger.debug(f"Player insurance bets: {player_insurance_bet}")

        self.player_bank = self.player_bank - player_insurance_bet

        self.total_player_stake = self.total_player_stake + player_insurance_bet

        return player_insurance_bet


    def player_blackjack(self, bet):
        self.player_bank = self.player_bank + bet * (1 + BLACKJACK_PAY_AMOUNT)


    def player_win(self, bet):
        self.player_bank = self.player_bank + bet * 2


    def player_push(self, bet):
        self.player_bank = self.player_bank + bet

    
    def should_dealer_play(self):
        # Dealer should not play if player has blackjack (we still check for dealer blackjack though)
        if self.player_has_blackjack():
            return False
            
        # Dealer should play if a player has an unbust hand
        for player_hand in self.player_hands:
            if player_hand["result"] != -1:
                return True

        return False


    def compute_hand(self, index):
        if sum(self.player_hands[index]["cards"]) > 21:
            aces = len([card for card in self.player_hands[index]["cards"] if card == 11])

            if aces > 0:
                self.player_hands[index]["cards"][self.player_hands[index]["cards"].index(11)] = 1
            else:
                logger.debug("BUST")
                logger.debug(f'Cards: {self.player_hands[index]["cards"]}')
                self.player_hands[index]["result"] = -1
                return

        logger.debug(f'Cards: {self.player_hands[index]["cards"]}')
        self.player_hands[index]["result"] = sum(self.player_hands[index]["cards"])

        logger.debug(f'Total: {self.player_hands[index]["result"]}')

    
    def player_has_blackjack(self):
        return is_blackjack(self.player_hands[0]["cards"]) and len(self.player_hands) == 1


    def play_hand(self, index):
        cards = self.player_hands[index]["cards"]
        dealer_upcard = self.dealer.upcard

        logger.debug(f'Cards: {cards}, Dealer upcard: {dealer_upcard}')

        if self.player_has_blackjack():
            self.player_hands[index]["result"] = 21
            return

        # Offer and compute splits
        if is_pair(cards) and self.player.want_split(cards, dealer_upcard) and (CAN_SPLIT_ACES or self.player_hands[index]["result"] != 22) and len(self.player_hands) < MAX_SPLITS + 1:
            logger.debug("SPLIT")

            hand_is_aces = False
            if self.player_hands[index]["result"] == 22:
                hand_is_aces = True
            
            self.split_player_hand(index)

            if CAN_PLAY_SPLIT_ACES or not hand_is_aces:
                # Play last hand first so any extra splits are inserted and played correctly
                self.play_hand(index+1)
                self.play_hand(index)
                return
            else:
                self.hit_player_hand(index+1)
                self.compute_hand(index+1)
                self.hit_player_hand(index)
                self.compute_hand(index)

        
        # Compute the hand now we have offered splits (we can change AA to 12 now and get totals)
        self.compute_hand(index)

        # Offer and compute double
        if self.player.want_double(cards, dealer_upcard):
            logger.debug("DOUBLE DOWN")
            self.double_player_hand(index)
            self.compute_hand(index)
            return
        

        while self.player_hands[index]["result"] != -1 and self.player.want_hit(self.player_hands[index]["cards"], dealer_upcard):
            logger.debug("HIT")
            self.hit_player_hand(index)
            self.compute_hand(index)


    def run(self):
        for i in tqdm(range(self.hands_to_run), ncols=150, colour='green', leave=False):

            logger.debug("-------NEW HAND-------")

            player_starting_bank = self.player_bank
            player_bet = self.get_player_bet()
            player_insurance_bet = 0

            cards = [self.shoe.draw(), self.shoe.draw(), self.shoe.draw(), self.shoe.draw()]

            self.dealer.dealt([cards[1], cards[3]])
            self.player_hands = [
                {"cards": [cards[0], cards[2]], "blackjack": False, "bet": player_bet, "result": 0}
            ]

            player_starting_cards = self.player_hands[0]["cards"].copy()

            dealer_upcard = self.dealer.upcard

            # Offer insurance (bet can be 0)
            if dealer_upcard == 11:
                player_insurance_bet = self.get_player_insurance_bet(cards, dealer_upcard)

            
            dealer_blackjack = self.dealer.has_blackjack()

            if player_insurance_bet > 0 and dealer_blackjack:
                self.player_win(player_insurance_bet)

            # Player only plays if dealer does not have blackjack
            if not dealer_blackjack:
                self.play_hand(0)
        
            # Dealer doesn't play if player has blackjack or player is bust
            if self.should_dealer_play():
                self.dealer.play(self.shoe)

            logger.debug(f"Dealer: {self.dealer.result}, {self.dealer.cards}")

            for index in range(len(self.player_hands)):

                player_hand = self.player_hands[index]

                logger.debug(f'Player: {player_hand["result"]}, {player_hand["cards"]}')

                if self.player_has_blackjack():
                    logger.debug("BLACKJACK")
                    if self.dealer.has_blackjack():
                        self.player_push(self.player_hands[index]["bet"])
                    else:
                        self.player_blackjack(self.player_hands[index]["bet"])
                else:
                    if self.dealer.result < player_hand["result"]:
                        self.player_win(self.player_hands[index]["bet"])
                    elif self.dealer.result == player_hand["result"]:
                        self.player_push(self.player_hands[index]["bet"])

            if self.should_print_stats:
                self.stats.record_hand(player_starting_cards, dealer_upcard, self.player_bank - player_starting_bank)

            logger.debug(f"Player bank: {self.player_bank}")
            self.shoe.reset_if_required()


        logger.info(f"Final player bank: {self.player_bank}, total stake: {self.total_player_stake}, yield: {100 * self.player_bank / self.total_player_stake}%")

        if self.should_print_stats:
            self.stats.log_payoff_grid()