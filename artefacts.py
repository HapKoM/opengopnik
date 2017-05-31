
class Artefact:
  def __init__(self):
    self.init_impl()

  def init_impl(self):
    self.strength_mod = 0
    self.agility_mod = 0
    self.vitality_mod = 0
    self.luck_mod = 0
    # Восстановление жизни за 1 ход
    self.health_recovery = 0
    # Вероятность зарастания перелома за ход
    self.break_healing_prob = 0
    # Мщная фенька?
    self.is_powerful = False
    self.description = "Артефакт"
    self.name = "Артефакт"

  def __str__(self):
    return self.name

class GodSaveRing(Artefact):
  def init_impl(self):
    self.strength_mod = 0
    self.agility_mod = 0
    self.vitality_mod = 0
    self.luck_mod = 1
    self.health_recovery = 0
    self.break_healing_prob = 0
    self.is_powerful = False
    self.description = ""
    self.name = "Кольцо \"Гс\"(Удача +1)"

class GodHelpRing(Artefact):
  def init_impl(self):
    self.strength_mod = 1
    self.agility_mod = 1
    self.vitality_mod = 1
    self.luck_mod = 1
    self.health_recovery = 0
    self.break_healing_prob = 0
    self.is_powerful = True
    self.description = "Кольцо \"Помоги Господи\""
    self.name = "Кольцо \"Пг\"(Всё +1)"

class MegaRing(Artefact):
  def init_impl(self):
    self.strength_mod = 4
    self.agility_mod = 4
    self.vitality_mod = 4
    self.luck_mod = 4
    self.health_recovery = 0
    self.break_healing_prob = 0
    self.is_powerful = True
    self.description = "\"Мега Кольцо\"! со своего, можно сказать, пальца"
    self.name = "Мега Кольцо(Всё +4)"

class GodForgiveRing(Artefact):
  def init_impl(self):
    self.strength_mod = 0
    self.agility_mod = 0
    self.vitality_mod = 0
    self.luck_mod = 0
    self.health_recovery = 3
    self.break_healing_prob = 5
    self.is_powerful = True
    self.description = "Ваще полезное кольцо \"Господи помилуй\"\nВосст. жизни - 3, 5% самозарост переломов"
    self.name = "Кольцо \"Гп\"(Самолечение)"