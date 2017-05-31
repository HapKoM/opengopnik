from person import Person, Type
from game_loop import GameLoop

game = GameLoop()

while not game.finished():
  game.step()
