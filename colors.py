class color:
  BLACK = '\033[0;30m'
  RED = '\033[1;31m'
  MAGENTA = '\033[1;35m'
  GREEN = '\033[1;32m'
  LIGHT_BLUE = '\033[1;34m'
  BLUE = '\033[1;34m'
  YELLOW = '\033[1;33m'
  WHITE = '\033[1;37m'
  CYAN = '\033[1;36m'
  GREY = '\033[1;30m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

  def r(string):
    return color.colorize(string, color.RED)

  def g(string):
    return color.colorize(string, color.GREEN)

  def lb(string):
    return color.colorize(string, color.LIGHT_BLUE)

  def b(string):
    return color.colorize(string, color.BLUE)

  def y(string):
    return color.colorize(string, color.YELLOW)

  def w(string):
    return color.colorize(string, color.WHITE)

  def grey(string):
    return color.colorize(string, color.GREY)

  def cyan(string):
    return color.colorize(string, color.CYAN)

  def magenta(string):
    return color.colorize(string, color.MAGENTA)

  def colorize(string, col):
    return col + string + color.ENDC