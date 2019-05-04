
import numpy as np
from random import randint, shuffle

class Game:
	def __init__(self):
		# game rules
		self.board_size = [9, 9]
		self.start_pos = [4, 4]
		self.num_colors = 7
		self.queue_size = 5
		self.active_size = 2
		self.cluster_size = 5
		self.move_matrix = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
		self.connect_matrix = [[-1, 0], [0, -1], [0, 1], [1, 0]]

		self.reset()

	def reset(self):
		self.board = np.zeros(self.board_size, dtype=int)
		self.tile_queue = np.random.randint(self.num_colors, size=self.queue_size) + 1
		self.player_pos = self.start_pos
		self.num_moves = 0
		self.num_cleared = 0

	def save(self):
		return (
			np.copy(self.board),
			self.tile_queue.copy(),
			self.player_pos.copy(),
			self.num_moves,
			self.num_cleared
		)

	def load(self, state):
		self.board, self.tile_queue, self.player_pos, self.num_moves, self.num_cleared = state

	def print(self):
		print(self.board)
		print(self.tile_queue)
		print(self.num_moves, self.num_cleared)

	def get_legal_moves(self):
		legal_moves = []
		for move in self.move_matrix:
			target_pos = [self.player_pos[0] + move[0], self.player_pos[1] + move[1]]
			if self._is_inside(target_pos) and self.board[target_pos[0], target_pos[1]] == 0:
				legal_moves.append(target_pos)
		return legal_moves
	
	def get_legal_tiles(self):
		playable_tiles = list(range(self.active_size))
		shuffle(playable_tiles)
		return playable_tiles

	def play(self, target_pos, tile):
		start_pos = self.player_pos

		# place tile in board
		self.board[target_pos[0]][target_pos[1]] = self.tile_queue[tile]

		# check clear
		check_color = self.tile_queue[tile]
		check_list = [target_pos]
		con_list = []

		while len(check_list) > 0:
			check_pos = check_list.pop()
			con_list.append(check_pos)
			
			for con in self.connect_matrix:
				con_pos = [check_pos[0] + con[0], check_pos[1] + con[1]]
				if self._is_inside(con_pos) and self.board[con_pos[0]][con_pos[1]] == check_color and con_pos not in con_list and con_pos not in check_list:
					check_list.append(con_pos)
		
		if len(con_list) >= self.cluster_size:
			for con_pos in con_list:
				self.board[con_pos[0]][con_pos[1]] = 0

		# update tile queue
		self.tile_queue[tile] = self.tile_queue[self.active_size]
		for i in range(self.active_size, self.queue_size - 1):
			self.tile_queue[i] = self.tile_queue[i+1]
		self.tile_queue[self.queue_size-1] = randint(1, self.num_colors)

		# update player pos
		self.player_pos = target_pos

		# update stats
		self.num_moves += 1

		return (start_pos, target_pos, tile, check_color, con_list)

	def undo(self, move):
		start_pos, target_pos, tile, check_color, con_list = move

		# update stats
		self.num_moves -= 1

		# update player pos
		self.player_pos = start_pos

		# update tile queue
		self.tile_queue[tile] = self.tile_queue[self.active_size]
		for i in reversed(range(self.active_size, self.queue_size - 1)):
			self.tile_queue[i+1] = self.tile_queue[i]
		self.tile_queue[self.active_size] = self.tile_queue[tile]
		self.tile_queue[tile] = check_color

		# undo clear
		if len(con_list) >= self.cluster_size:
			for con_pos in con_list:
				self.board[con_pos[0]][con_pos[1]] = check_color
		
		# remove tile from board
		self.board[target_pos[0]][target_pos[1]] = 0

	def _is_inside(self, pos):
		return pos[0] >= 0 and pos[0] < self.board_size[0] and pos[1] >= 0 and pos[1] < self.board_size[1]
