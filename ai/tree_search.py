
from game.game import Game
from random import shuffle

class TreeSearch:

	# returns (targetPos, tile), score
	def find_best_move(self, game: Game, evaluator, depth: int):
		legal_moves = game.get_legal_moves()
		shuffle(legal_moves)
		if len(legal_moves) == 0:
			return None, None, float("-inf"), legal_moves
		elif depth > 0:
			# try all move and find max score
			best_move = None
			best_tile = None
			best_score = None
			for move in legal_moves:
				playable_tiles = list(range(game.active_size))
				shuffle(playable_tiles)
				for tile in playable_tiles:
					hist_move = game.play(move, tile)

					_, _, cur_score, _ = self.find_best_move(game, evaluator, depth-1)
					if cur_score is not None and (best_score is None or cur_score > best_score):
						best_move = move
						best_tile = tile
						best_score = cur_score
					
					game.undo(hist_move)
			return best_move, best_tile, best_score, legal_moves
		else:
			return None, None, evaluator.eval(game), legal_moves
