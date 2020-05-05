from display.engine import Engine
from display.tictactoedefault33scene import TicTacToeDefault33Scene
from renderers.text_renderer import TextRenderer

engine = Engine(TicTacToeDefault33Scene(), TextRenderer())
engine.run_loop()
