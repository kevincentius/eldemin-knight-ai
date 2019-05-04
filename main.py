
from game.game import Game
from ai.count_evaluator import CountEvaluator
from ai.tree_search import TreeSearch

from random import randint

# Game Rules
game = Game()
game.num_colors = 6

evaluator = CountEvaluator()
tree_search = TreeSearch()

wa = 0
num_moves = []
for e in range(1000):
	game.reset()

	for n_moves in range(1000):
		best_move, best_tile, best_score, legal_moves = tree_search.find_best_move(game, evaluator, 4)

		if len(legal_moves) > 0:
			game.play(best_move, best_tile)

		else:
			break
	
	num_moves.append(game.num_moves)
	wa = wa * 0.95 + 0.05 * game.num_moves

	print('round: {}, wa: {:.2f}, moves: {}'.format(
		e, wa, game.num_moves
	))

print('WA:', wa, 'Average:', sum(num_moves) / len(num_moves), 'moves')

