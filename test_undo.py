
from game.game import Game

game = Game()

old_queue = game.tile_queue.copy()
hist_move = game.play([0,0], 0)
new_queue = game.tile_queue.copy()
game.undo(hist_move)
undo_queue = game.tile_queue.copy()

print(old_queue)
print(new_queue)
print(undo_queue)
