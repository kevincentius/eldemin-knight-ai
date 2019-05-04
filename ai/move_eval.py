
from game.game import Game

def eval_move(game: Game, target_pos: list, tile: int):
	return len(game.get_connected_tiles(target_pos, game.tile_queue[tile]))
