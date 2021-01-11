import argparse
from game import Game

def main(hands_to_run):
    game = Game(hands_to_run)
    game.run()
    

if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--hands', type=int, help='Number of hands to simulate')
    args=parser.parse_args()

    main(args.hands)
