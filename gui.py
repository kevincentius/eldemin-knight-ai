import kivy
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, StringProperty

from game.game import Game
from ai.tree_search import TreeSearch

game = Game()


# Game Rules
game = Game()
game.board_size = [7, 7]
game.start_pos = [3, 3]
game.num_colors = 6

tree_search = TreeSearch()

game.reset()



class MainView(BoxLayout):
    colors = [
                (0.2, 0.2, 0.2, 1),
                (1, 0, 0, 1),
                (1, 1, 0, 1),
                (0, 1, 0, 1),
                (0, 1, 1, 1),
                (0, 0, 1, 1),
                (1, 0, 1, 1)
                ]
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.img_buttons = []
        self.float_buttons = []
        self.next_buttons = []
        self.build()

    def build(self):
        for i in range(49):
            button = Button(background_normal='')
            self.buttons.append(button)

            img_button = Button(background_normal='')
            self.img_buttons.append(img_button)

            float_button = RelativeLayout()
            float_button.add_widget(button)
            float_button.add_widget(img_button)
            self.float_buttons.append(float_button)

            self.grid_name.add_widget(float_button)

        for i in range(5):
            next_button = Button(background_normal='', size_hint=(None,None), size=(50, 50))
            self.next_buttons.append(next_button)
            self.box_name.add_widget(next_button)

        self.update()

    def update(self):
        for i in range(49):
            color_id = game.board[int(i / 7)][i % 7]
            self.buttons[i].background_color = self.colors[color_id]
            self.img_buttons[i].background_color = (0,0,0,0)
            self.img_buttons[i].background_normal = ''

            if game.player_pos[0] == int(i/7) and game.player_pos[1] == i%7:
                self.img_buttons[i].background_color = (1,1,1,1)
                self.img_buttons[i].background_normal = "knight.png"
        
        for i in range(5):
            self.next_buttons[i].background_color=self.colors[game.tile_queue[i]]
        
        self.label_update.text = str(game.num_moves)

    def make_move(self):
        best_move, best_tile, best_score, legal_moves = tree_search.find_best_move(game, 3)
        if len(legal_moves) > 0:
            game.play(best_move, best_tile)
        
        self.update()
    def make_reset(self):
        game.reset()
        self.update()
    def make_start(self):
        pass
    def make_pause(self):
        pass

    

class GameApp(App):
    def build(self):
        return MainView()

if __name__ == "__main__":
    GameApp().run()