
from game.game import Game
from ai.move_eval import count_obstructing, count_adj
import numpy as np

game = Game()

game.board_size = [3, 3]
game.start_pos = [1, 1]
game.reset()

game.board = np.array([
	[2, 1, 0],
	[1, 0, 0],
	[0, 0, 0]
])

assert count_obstructing(game, [1, 1], [1,1], 3) == 1
assert count_obstructing(game, [1, 1], [1,1], 2) == 1
assert count_obstructing(game, [1, 1], [1,1], 1) == 0

assert count_adj(game, [1, 1], 3) == (0, 2, 0)
assert count_adj(game, [1, 1], 1) == (2, 0, 0)

game.board = np.array([
	[0, 1, 0],
	[1, 0, 0],
	[0, 0, 0]
])

assert count_obstructing(game, [1, 1], [1,1], 3) == 0
