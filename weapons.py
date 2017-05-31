class Weapon:
  def __init__(self):
    self.strike_mod = 0
    self.price = 0
  def __str__(self):
    return ""

class ClubWeapon(Weapon):
  '''Дубинка'''
  def __init__(self):
    self.strike_mod = 4
  def __str__(self):
    return "Дубинка(Урон+4)"

class CleaverWeapon(Weapon):
  '''Тесак'''
  def __init__(self):
    self.strike_mod = 9
  def __str__(self):
    return "Тесак(Урон+9)"