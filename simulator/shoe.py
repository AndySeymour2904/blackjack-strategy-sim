import random
import logging

from config import DECKS, DECK_PENETRATION, IS_INFINITE_DECK

from card_utils import get_count_for_card

logger = logging.getLogger()

class Shoe:
    def __init__(self):
        self.num_decks = DECKS
        self.min_decks = DECKS * DECK_PENETRATION
        self.create_and_shuffle_shoe()

    def create_and_shuffle_shoe(self):
        logger.debug("-------NEW SHOE-------")
        self.shoe = (list(range(2, 12)) + [10, 10, 10]) * 4 * self.num_decks
        self.count = 0
        random.shuffle(self.shoe)


    def draw(self):
        if IS_INFINITE_DECK:
            card = random.choice(self.shoe)
        else:
            card = self.shoe.pop()

        self.count = self.count + get_count_for_card(card)

        logger.debug(f"Shoe draws: {card}")
        return card


    def get_true_count(self):
        return self.count / (len(self.shoe) / 52)


    def reset_if_required(self):
        if len(self.shoe) < self.min_decks * 52:
            self.create_and_shuffle_shoe()