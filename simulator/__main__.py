import argparse
from shoe import Shoe 
from dealer import Dealer
from player import Player

def main(hands_to_run):
    shoe = Shoe(8, 4)
    player = Player()
    dealer = Dealer()

    for i in range(hands_to_run):

        print("-------NEW HAND-------")

        cards = [shoe.draw(), shoe.draw(), shoe.draw(), shoe.draw()]

        dealer.dealt([cards[1], cards[3]])
        player.dealt([cards[0], cards[2]])

        player.play(shoe, dealer.upcard)

        if player.result > 0 and not player.blackjack:
            dealer.play(shoe)

        print(f"Dealer: {dealer.result}, {dealer.cards}")
        print(f"Player: {player.result}, {player.cards}")

        if dealer.result < player.result:
            player.win()
        elif dealer.result == player.result:
            player.push()
        
        print(f"Player bank: {player.bank}")

        shoe.reset_if_required()

    print(f"Final player bank: {player.bank}")
    

if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--hands', type=int, help='Number of hands to simulate')
    args=parser.parse_args()

    main(args.hands)
