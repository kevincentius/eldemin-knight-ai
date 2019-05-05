
from game.game import Game

import math

def count_legal_two_steps(game: Game, pos: list):
	count = 0
	for move in game.get_legal_moves():
		hist_move = game.play(move, 0)
		count += len(game.get_legal_moves())
		game.undo(hist_move)
	
	return count

def count_adj(game: Game, pos: list, color: int):
	count_match = 0
	count_mismatch = 0
	count_wall = 0

	for conn in game.connect_matrix:
		adj_pos = [pos[0] + conn[0], pos[1] + conn[1]]
		if game.is_inside(adj_pos):
			if game.board[adj_pos[0], adj_pos[1]] == color:
				count_match += 1
			else:
				count_mismatch += 1
		else:
			count_wall += 1
	return count_match, count_mismatch, count_wall

def count_liberties(game: Game, cluster: list, color: int):
	# find all tiles adjacent to cluster
	adj_tiles = []
	for tile in cluster:
		for conn in game.connect_matrix:
			adj_pos = [tile[0] + conn[0], tile[1] + conn[1]]
			if game.is_inside(adj_pos) and adj_pos not in cluster and adj_pos not in adj_tiles:
				adj_tiles.append(adj_pos)
	
	count_liberty = 0
	count_blocked = 0
	for adj_tile in adj_tiles:
		if game.board[adj_tile[0], adj_tile[1]] == 0:
			count_liberty += 1
		else:
			count_blocked += 1
	
	return count_liberty, count_blocked

def eval_move(game: Game, target_pos: list, tile: int, weights=[0, 0, 0, 0, 0, 0, 0]):
	color = game.tile_queue[tile]
	cluster = game.get_connected_tiles(target_pos, color)
	count_match, count_mismatch, count_wall = count_adj(game, target_pos, color)
	count_liberty, count_blocked = count_liberties(game, cluster, color)
	count_legal_moves_2 = count_legal_two_steps(game, target_pos)
	features = [cluster, count_match, count_mismatch, count_wall, count_liberty, count_blocked, math.log(count_legal_moves_2 + 1)]
	
	return (
		len(cluster)
		+ 0.5 * math.log(count_legal_moves_2 + 1)
	)
