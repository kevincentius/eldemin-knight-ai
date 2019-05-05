
from game.game import Game
from ai.count_evaluator import CountEvaluator
from ai.tree_search import TreeSearch

from random import randint

# Game Rules
game = Game()
game.board_size = [7, 7]
game.start_pos = [3, 3]
game.num_colors = 6

tree_search = TreeSearch()

num_moves = []
e = 0
while True:
	e += 1
	game.reset()

	for n_moves in range(1000):
		best_move, best_tile, best_score, legal_moves = tree_search.find_best_move(game, 4)

		if len(legal_moves) > 0:
			game.play(best_move, best_tile)

		else:
			break

	num_moves.append(game.num_moves)

	print('round: {}, avg: {:.2f}, moves: {}'.format(
		e, sum(num_moves) / len(num_moves), game.num_moves
	))
