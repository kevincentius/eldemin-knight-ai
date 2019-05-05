
from game.game import Game
from random import shuffle

from ai.move_eval import eval_move

class TreeSearch:

	# returns (targetPos, tile), score
	def find_best_move(self, game: Game, weights, depth: int, scores=[]):
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
					test_queue = game.tile_queue.copy()

					# play move
					scores.append(eval_move(game, move, tile, weights))
					hist_move = game.play(move, tile)

					# check if best move is beaten
					_, _, cur_score, _ = self.find_best_move(game, weights, depth-1)
					if cur_score is not None and (best_score is None or cur_score > best_score):
						best_move = move
						best_tile = tile
						best_score = cur_score
					
					# undo move
					game.undo(hist_move)
					scores.pop()
					
			return best_move, best_tile, best_score, legal_moves

		else:
			# run out of depth, calculate final score
			return None, None, sum(scores), legal_moves
