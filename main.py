import pyglet
from pyglet import shapes
import string
import random

window = pyglet.window.Window(width=1280, height=720)

class Game:
    def __init__(self, correct_word):
        self.correct_word = correct_word
        self.word = ['_' for _ in self.correct_word]
        self.word_label = pyglet.text.Label()

        self.wrong_attemps = list()
        self.wrong_attemps_label = pyglet.text.Label()

        self.hang = pyglet.graphics.Batch()
        self.hangman = pyglet.graphics.Batch()

        self.__update_label()

    def __update_label(self):
        self.word_label = pyglet.text.Label(
            ''.join(self.word),
            font_name = 'Fira Code',
            font_size = 36,
            x = window.width // 2,
            y = window.height // 2,
            anchor_x = 'center',
            anchor_y = 'center'
        )

        self.wrong_attemps_label = pyglet.text.Label(
            ''.join(self.wrong_attemps),
            font_name = 'Fira Code',
            font_size = 36,
            x = window.width // 2,
            y = window.height // 2 - 220,
            anchor_x = 'center',
            anchor_y = 'center'
        )

    def key_pressed(self, letter):
        if letter in self.word or letter in self.wrong_attemps:
            return

        match = False
        for i in range(len(self.correct_word)):
            if self.correct_word[i] == letter:
                self.word[i] = letter
                match = True

        if not match:
            self.wrong_attemps.append(letter)

        self.__update_label()

    def draw_hang(self):
        x = window.width // 2 - 300
        y = window.height // 2 - 120

        line_1 = shapes.Line(x, y, x, y + 300, width=5, color=(255, 255, 255), batch=self.hang)
        line_2 = shapes.Line(x, y + 300, x + 100, y + 300, width=5, color=(255, 255, 255), batch=self.hang)
        line_3 = shapes.Line(x + 100, y + 300, x + 100, y + 270, width=5, color=(255, 255, 255), batch=self.hang)

        self.hang.draw()

    def draw_hangman(self):
        x = window.width // 2 - 200
        y = window.height // 2 + 120

        wrong_count = len(self.wrong_attemps)

        if wrong_count > 0:
            head = shapes.Circle(x, y, 30, color=(255, 255, 255), batch=self.hangman)

        if wrong_count > 1:
            body = shapes.Line(x, y, x, y - 120, width=5, color=(255, 255, 255), batch=self.hangman)

        if wrong_count > 2:
            arm_1 = shapes.Line(x, y - 50, x - 40, y - 100, width=5, color=(255, 255, 255), batch=self.hangman)

        if wrong_count > 3:
            arm_2 = shapes.Line(x, y - 50, x + 40, y - 100, width=5, color=(255, 255, 255), batch=self.hangman)

        if wrong_count > 4:
            leg_1 = shapes.Line(x, y - 120, x - 40, y - 200, width=5, color=(255, 255, 255), batch=self.hangman)

        if wrong_count > 5:
            leg_2 = shapes.Line(x, y - 120, x + 40, y - 200, width=5, color=(255, 255, 255), batch=self.hangman)

        self.hangman.draw()

    def run(self):
        self.draw_hang()
        self.draw_hangman()
        self.word_label.draw()
        self.wrong_attemps_label.draw()

        if not '_' in self.word:
            window.clear()
            pyglet.text.Label(
                    'You Win',
                    font_name='Fira Code',
                    font_size=56,
                    x = window.width // 2,
                    y = window.height // 2,
                    anchor_x = 'center',
                    anchor_y = 'center'
                    ).draw()

        if len(self.wrong_attemps) >= 6:
            window.clear()
            pyglet.text.Label(
                    'Game Over',
                    font_name='Fira Code',
                    font_size=56,
                    x = window.width // 2,
                    y = window.height // 2,
                    anchor_x = 'center',
                    anchor_y = 'center'
                    ).draw()
        pass

selected_word = ""
with open('words.txt') as f:
    words = list()
    for word in f.readlines():
        words.append(word[:-1])

    selected_word = random.choice(words)

game = Game(selected_word)

@window.event
def on_draw():
    window.clear()
    game.run()

@window.event
def on_key_press(symbol, _):
    if chr(symbol) in string.ascii_letters:
        game.key_pressed(chr(symbol).lower())

if __name__ == '__main__':
    pyglet.app.run()
