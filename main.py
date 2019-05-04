
from game.game import Game
from ai.count_evaluator import CountEvaluator
from ai.tree_search import TreeSearch

from random import randint

# Game Rules
game = Game()
game.num_colors = 3

evaluator = CountEvaluator()
tree_search = TreeSearch()

# baseline: 1-deep count evaluator --> 843.3875, 898.015625 moves (3 colors, 9x9 board)
# untrained: 167.39, 123.88, 129.17, 111.58 moves

wa = 0
num_moves = []
for e in range(1000):
	game.reset()

	for n_moves in range(2000):
		best_move, best_tile, best_score, legal_moves = tree_search.find_best_move(game, evaluator, 1)
		#target_pos, tile, score, legal_moves = tree_search.find_best_move(game, agent, 1)

		if len(legal_moves) > 0:
			game.play(best_move, best_tile)

		else:
			num_moves.append(game.num_moves)
			wa = wa * 0.95 + 0.05 * game.num_moves

			# TODO: just bug check, can be removed
			if game.num_moves < 4:
				game.print()
				input()
			break
	
	print('round: {}, wa: {:.2f}, moves: {}'.format(
		e, wa, game.num_moves
	))

print('WA:', wa, 'Average:', sum(num_moves) / len(num_moves), 'moves')

