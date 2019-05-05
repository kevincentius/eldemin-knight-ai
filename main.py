
from game.game import Game
from ai.count_evaluator import CountEvaluator
from ai.tree_search import TreeSearch

from random import randint

# Game Rules
game = Game()
game.board_size = [7, 7]
game.start_pos = [3, 3]
game.num_colors = 5

tree_search = TreeSearch()

# Search Rules
weights = [1, 0, 0, 0, 0, 0, 0] # [1, 0, 0, 0, 0.2, 0, 0.5]
num_sims = 50

test_change = 0.2
change_rate = 0.002
max_change = 0.05

def simulate(weights):
	num_moves = []
	for e in range(num_sims):
		game.reset()

		for n_moves in range(1000):
			game.print()
			input()

			best_move, best_tile, best_score, legal_moves = tree_search.find_best_move(game, weights, 4)

			if len(legal_moves) > 0:
				game.play(best_move, best_tile)

			else:
				break
	
		game.print()
		input()
		
		num_moves.append(game.num_moves)

		# print('round: {}, avg: {:.2f}, moves: {}'.format(
		# 	e, sum(num_moves) / len(num_moves), game.num_moves
		# ))
	
	return sum(num_moves) / len(num_moves)

while True:
	feat_deltas = [0]

	# see performance of current weights
	base_score = simulate(weights)
	print('base score', base_score, 'weights', weights)

	# try small changes in each feature
	for i in range(1, len(weights)):
		test_weight = weights.copy()
		test_weight[i] += test_change
		inc_score = simulate(test_weight)

		test_weight[i] -= 2*test_change
		dec_score = simulate(test_weight)

		# calculate feature update based on 'learning_rate' * 'gradient'
		feat_delta = change_rate * (inc_score - dec_score)
		if feat_delta < -max_change:
			feat_delta = -max_change
		elif feat_delta > max_change:
			feat_delta = max_change

		feat_deltas.append(feat_delta)

	# update weights
	print('deltas', feat_deltas)
	for i in range(1, len(weights)):
		weights[i] += feat_deltas[i]
