import argparse
import logging
from game import Game

logging.basicConfig(
    format='%(levelname)s:%(message)s',
    level=logging.DEBUG
)

def main(hands_to_run, should_print_stats):
    game = Game(hands_to_run, should_print_stats)
    game.run()
    
if __name__ == '__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('--hands', type=int, help='Number of hands to simulate')
    parser.add_argument('--debug', help='Print debug statements', action='store_true')
    parser.add_argument('--stats', help='Print stats statements', action='store_true')
    args=parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    main(args.hands, args.stats)

