
from game.game import Game
import numpy as np

class CountEvaluator:
	def eval(self, game):
		return np.count_nonzero(game.board==0)
