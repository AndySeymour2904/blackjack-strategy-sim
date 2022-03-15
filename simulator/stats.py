from card_utils import is_pair, is_soft_hand
from tabulate import tabulate
from colorama import Back

tabulate.PRESERVE_WHITESPACE = True

import logging
logger = logging.getLogger()

class Stats:
	def __init__(self):
		self.hard_grid_payoff = [[0] * 10 for j in range(15)]
		self.hard_grid_occurence = [[0] * 10 for j in range(15)]
		self.hard_grid_ev = [[0] * 10 for j in range(15)]

		self.pair_grid_payoff = [[0] * 10 for j in range(10)]
		self.pair_grid_occurence = [[0] * 10 for j in range(10)]
		self.pair_grid_ev = [[0] * 10 for j in range(10)]

		self.soft_grid_payoff = [[0] * 10 for j in range(9)]
		self.soft_grid_occurence = [[0] * 10 for j in range(9)]
		self.soft_grid_ev = [[0] * 10 for j in range(9)]

	def record_hand(self, player_starting_cards, dealer_upcard, outcome):
		if is_pair(player_starting_cards):
			self.pair_grid_occurence[player_starting_cards[0] - 2][dealer_upcard - 2] += 1
			self.pair_grid_payoff[player_starting_cards[0] - 2][dealer_upcard - 2] += outcome
		else:
			player_total = sum(player_starting_cards)

			if is_soft_hand(player_starting_cards):
				self.soft_grid_occurence[player_total - 13][dealer_upcard - 2] += 1
				self.soft_grid_payoff[player_total - 13][dealer_upcard - 2] += outcome
			else:
				self.hard_grid_occurence[player_total - 5][dealer_upcard - 2] += 1
				self.hard_grid_payoff[player_total - 5][dealer_upcard - 2] += outcome

	def log_payoff_grid(self):
		headers = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A"]
		hard_rowIDs = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
		pair_rowIDs = ["2,2", "3,3", "4,4", "5,5", "6,6", "7,7", "8,8", "9,9", "10,10", "A,A"]
		soft_rowIDs = ["A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]

		def compute_cell_and_color(payoff, occurence):
			val = 0 if occurence == 0 else payoff / occurence

			color = ""
			if val > 0:
				color = Back.GREEN
			elif val < 0:
				color = Back.RED

			return f"{color}{val}{Back.RESET}"

		for i in range(len(self.hard_grid_ev)):
			for j in range(len(self.hard_grid_ev[i])):
				self.hard_grid_ev[i][j] = compute_cell_and_color(self.hard_grid_payoff[i][j], self.hard_grid_occurence[i][j])

		for i in range(len(self.pair_grid_ev)):
			for j in range(len(self.pair_grid_ev[i])):
				self.pair_grid_ev[i][j] = compute_cell_and_color(self.pair_grid_payoff[i][j], self.pair_grid_occurence[i][j])

		for i in range(len(self.soft_grid_ev)):
			for j in range(len(self.soft_grid_ev[i])):
				self.soft_grid_ev[i][j] = compute_cell_and_color(self.soft_grid_payoff[i][j], self.soft_grid_occurence[i][j])

		logger.info("\nHARD TOTALS\n" + tabulate(self.hard_grid_ev, headers=headers, showindex=hard_rowIDs, tablefmt="fancy_grid", floatfmt=".5f"))
		logger.info("\nPAIRS\n" + tabulate(self.pair_grid_ev, headers=headers, showindex=pair_rowIDs, tablefmt="fancy_grid", floatfmt=".5f"))
		logger.info("\nSOFT TOTALS\n" + tabulate(self.soft_grid_ev, headers=headers, showindex=soft_rowIDs, tablefmt="fancy_grid", floatfmt=".5f"))