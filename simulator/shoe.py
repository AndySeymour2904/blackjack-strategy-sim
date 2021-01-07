import random

class Shoe:
    def __init__(self, num_decks, min_decks):
        self.num_decks = num_decks
        self.min_decks = min_decks
        self.create_and_shuffle_shoe()

    def create_and_shuffle_shoe(self):
        print("-------NEW SHOE-------")
        self.shoe = (list(range(2, 12)) + [10, 10, 10]) * 4 * self.num_decks
        random.shuffle(self.shoe)


    def draw(self):
        return self.shoe.pop()


    def reset_if_required(self):
        if len(self.shoe) < self.min_decks * 52:
            self.create_and_shuffle_shoe()