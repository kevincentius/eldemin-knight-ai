import kivy
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.core.window import Window

from game.game import Game
from ai.tree_search import TreeSearch

import functools

game = Game()


# Game Rules
game = Game()
game.board_size = [7, 7]
game.start_pos = [3, 3]
game.num_colors = 6

tree_search = TreeSearch()

game.reset()

mv = None



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

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        global mv
        mv = self

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
            img_button.on_press=functools.partial(click_tile, i)
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
            next_button.on_press=swap_tile

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
        best_move, best_tile, best_score, legal_moves = tree_search.find_best_move(game, 4)
        if len(legal_moves) > 0:
            game.play(best_move, best_tile)
        
        self.update()
    def make_reset(self):
        game.reset()
        self.update()
    def make_start(self):
        Clock.schedule_interval(clock_f, 0.25)
    def make_pause(self):
        Clock.unschedule(clock_f)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 32:
            swap_tile()
        return True

def clock_f(dt):
    mv.make_move()

def click_tile(i):
    target_pos = [int(i/7), i%7]

    if target_pos in game.get_legal_moves():
        game.play(target_pos, 0)
        mv.update()

def swap_tile():
    tmp = game.tile_queue[0]
    game.tile_queue[0] = game.tile_queue[1]
    game.tile_queue[1] = tmp
    mv.update()

class GameApp(App):
    def build(self):
        return MainView()

if __name__ == "__main__":
    GameApp().run()