# -*- coding: UTF-8 -*-

from enum import Enum
from colors import color as cl
import random
import artefacts
import weapons
import defence

class Type(Enum):
  POTSAN   = 0
  OTMOROZOK = 1
  GOPNIK    = 2
  VOR       = 3
  MANIAC    = 4
  BEZPREDEL = 5
  DOHLAK    = 6
  NEFOR     = 7
  MENT      = 8
  NARK      = 9

  def __str__(self):
    if self == Type.POTSAN:
      return "Подтсан"
    elif self == Type.OTMOROZOK:
      return "Отморозок"
    elif self == Type.GOPNIK:
      return "Гопник"
    elif self == Type.VOR:
      return "Вор"
    elif self == Type.MANIAC:
      return "Маньячок"
    elif self == Type.BEZPREDEL:
      return "Беспредельщик"
    elif self == Type.DOHLAK:
      return "Дохляк"
    elif self == Type.NEFOR:
      return "Нефор"
    elif self == Type.MENT:
      return "Мент"
    elif self == Type.NARK:
      return "Нарк"
    else:
      raise TypeError("Unknown type")

class Person:
  
  def __init__(self, person_type, name):
    self.name           = ""
    self.person_type    = None
    self.strength       = 0
    self.agility        = 0
    self.vitality       = 0
    self.luck           = 0
    self.level          = 0
    self.shield         = 0
    self.current_health = 0
    self.artefacts      = []
    self.weapons        = []
    self.shields        = []
    self.skill          = 0
    self.beer           = float(0.0)
    self.pot            = 0
    self.money          = 0
    self.stuff          = 0
    # Есть мобила?
    self.mobile         = False
    # Есть солнечные очки
    self.sun_glass      = False
    # Есть татуировка
    self.tattoo         = False
    # Есть зубная защита
    self.jaw_shield     = False
    # Сломана нога?
    self.broken_leg     = False
    # Сломана челюсть?
    self.broken_jaw     = False
    self.person_type = person_type
    self.name        = name
    # Понтовость среди гопоты
    self.pont = 0
    if person_type == Type.POTSAN:
      self.strength       = 3
      self.agility        = 3
      self.vitality       = 3
      self.luck           = 3
    elif person_type == Type.OTMOROZOK:
      self.strength       = 5
      self.agility        = 2
      self.vitality       = 4
      self.luck           = 1
    elif person_type == Type.GOPNIK:
      self.strength       = 4
      self.agility        = 3
      self.vitality       = 3
      self.luck           = 2
    elif person_type == Type.VOR:
      self.strength       = 3
      self.agility        = 3
      self.vitality       = 2
      self.luck           = 4
    elif person_type == Type.MANIAC:
      self.strength       = 4
      self.agility        = 5
      self.vitality       = 4
      self.luck           = 5
    elif person_type == Type.BEZPREDEL:
      self.strength       = 5
      self.agility        = 5
      self.vitality       = 4
      self.luck           = 4
    elif person_type == Type.DOHLAK:
      self.strength       = 1
      self.agility        = 2
      self.vitality       = 2
      self.luck           = 1
    elif person_type == Type.NEFOR:
      self.strength       = 2 #3
      self.agility        = 2 #1
      self.vitality       = 1 #2
      self.luck           = 4 #3
    elif person_type == Type.MENT:
      self.strength       = 4
      self.agility        = 5
      self.vitality       = 4
      self.luck           = 5
    elif person_type == Type.NARK:
      self.strength       = 2
      self.agility        = 1
      self.vitality       = 4
      self.luck           = 1
    self.current_health = self.getMaxHealth()

  def levelStr(self):
    names = [
      "Опущенный",
      "Полное ЧМО",
      "ЧМО",
      "Частично не ЧМО",
      "Чё-то не понятное",
      "Чё-то отдалённо похожее на не ЧМО"
      "Вроде не ЧМО",
      "Не ЧМО",
      "Совсем не ЧМО",
      "Похожий на Чувака",
      "Чувак",
      "Нормальный Чувак",
      "Да нормальный такой Чувак",
      "Довольно понтовый чувак",
      "Понтовый Чувак",
      "Вполне понтовый Чувак",
      "Очень понтовый чувак",
      "Чувак отдалённо похожий на Пацана",
      "Похожий на Пацана",
      "Сильно похожий на Пацана",
      "Вроде Пацан",
      "Пацан",
      "Пацан покруче",
      "Понтоватый Пацан",
      "Понтовый Пацан",
      "Очень понтовый Пацан",
      "Крутой Пацан",
      "Очень крутой Пацан",
      "Пацан метящий в реальные",
      "Довольно реальный Пацан",
      "Реальный Пацан",
      "Пацан немного более реальный",
      "Очень реальный Пацан",
      "Офигенно реальный Пацан",
      "Да типа ваще реальный Пацан",
      "Смотри не лопни от реальности, реальный Пацан",
      "Крутой Реальный Пацан",
      "Очень крутой Реальный Пацан",
      "Самый Крутой Реальный Пацан",
      "Пацан, который завалил Проректора СУНЦа",
      "Пацан, который всех опрокинул",
    ]
    if self.level < len(names):
      return names[self.level]
    else:
      return "Не в этой жизни"

  def getMinStrike(self):
    bestWeaponStrike = 0
    for w in self.weapons:
      if w.strike_mod > bestWeaponStrike:
        bestWeaponStrike = w.strike_mod
    return self.eff_strength() // 2 + bestWeaponStrike

  def getMaxStrike(self):
    bestWeaponStrike = 0
    for w in self.weapons:
      if w.strike_mod > bestWeaponStrike:
        bestWeaponStrike = w.strike_mod
    return self.eff_strength() + bestWeaponStrike

  def getMaxHealth(self):
    return 10 + self.eff_vitality()*5 + self.eff_strength()

  def nextLevelSkill(self):
    if self.level < 0:
      self.level = 0
    return 10*(self.level + 1)

  def levelUp(self, silent=False):
    s = self.strength + self.agility + self.vitality + self.luck
    v = random.randint(0, s - 1)
    descr = ""
    if v < self.strength:
      self.strength += 1
      descr = "Сила +1 "
    elif v < self.strength + self.agility:
      self.agility += 1
      descr = "Ловкость +1 "
    elif v < self.strength + self.agility + self.vitality:
      self.vitality += 1
      descr = "Живучесть +1 "
    else:
      self.luck += 1
      descr = "Удача +1 "
    v = random.randint(0, s - 1)
    if v < self.strength:
      self.strength += 1
      descr += "Сила +1"
    elif v < self.strength + self.agility:
      self.agility += 1
      descr += "Ловкость +1"
    elif v < self.strength + self.agility + self.vitality:
      self.vitality += 1
      descr += "Живучесть +1"
    else:
      self.luck += 1
      descr += "Удача +1"
    self.skill -= self.nextLevelSkill()
    old_level_str = self.levelStr()
    self.level += 1
    new_level_str = self.levelStr()
    if not silent:
      print(cl.b("Был ты " + old_level_str + " а стал " + new_level_str))
      print(cl.b("Понтовость увеличивается: " + descr))
    self.current_health = self.getMaxHealth()

  def levelDown(self, silent=False):
    if self.level == 0:
      return
    s = self.strength + self.agility + self.vitality + self.luck
    v = random.randint(0, s - 1)
    descr = ""
    if v < self.strength:
      self.strength -= 1
      descr = "Сила -1 "
    elif v < self.strength + self.agility:
      self.agility += 1
      descr = "Ловкость -1 "
    elif v < self.strength + self.agility + self.vitality:
      self.vitality += 1
      descr = "Живучесть -1 "
    else:
      self.luck += 1
      descr = "Удача -1 "
    v = random.randint(0, s - 1)
    if v < self.strength:
      self.strength += 1
      descr += "Сила -1"
    elif v < self.strength + self.agility:
      self.agility += 1
      descr += "Ловкость -1"
    elif v < self.strength + self.agility + self.vitality:
      self.vitality += 1
      descr += "Живучесть -1"
    else:
      self.luck += 1
      descr += "Удача -1"
    if self.strength < 0:
      self.strength = 0
    if self.agility < 0:
      self.agility = 0
    if self.vitality < 0:
      self.vitality = 0
    if self.luck < 0:
      self.luck = 0
    self.skill = 0
    self.level -= 1
    self.current_health = self.getMaxHealth()
    if not silent:
      print(cl.r(descr))

  def increaseExp(self, exp):
    if self.level < 0:
      self.level = 0
    self.skill += exp
    while self.skill >= self.nextLevelSkill():
      self.levelUp()
    if self.skill <= 0:
      self.skill = 0


  def getStrikesAccuracy(self):
    acc = 20 + self.eff_agility()*5
    if acc < 20:
      acc = 20
    strikes = []
    while acc > 0:
      if acc > 90:
        strikes.append(90)
      else:
        strikes.append(acc)
      acc -= 90
    return strikes

  def isDead(self):
    return (self.current_health <= 0)

  def eff_shield(self):
    '''Броня с учётом действия всех артефактов'''
    val = self.shield
    for s in self.shields:
      val += a.shield_mod
    return val

  def eff_strength(self):
    '''Сила с учётом действия всех артефактов'''
    val = self.strength
    for a in self.artefacts:
      val += a.strength_mod
    return val

  def eff_strength_s(self):
    val = self.eff_strength()
    if val == self.strength:
      return cl.w(str(val))
    else:
      return cl.b("{0}".format(val))

  def eff_agility(self):
    '''Ловкость с учётом действия всех артефактов'''
    val = self.agility
    for a in self.artefacts:
      val += a.agility_mod
    return val

  def eff_agility_s(self):
    val = self.eff_agility()
    if val == self.agility:
      return cl.w(str(val))
    else:
      return cl.b("{0}".format(val))

  def eff_vitality(self):
    '''Живучесть с учётом действия всех артефактов'''
    val = self.vitality
    for a in self.artefacts:
      val += a.vitality_mod
    return val

  def eff_vitality_s(self):
    val = self.eff_vitality()
    if val == self.vitality:
      return cl.w(str(val))
    else:
      return cl.b("{0}".format(val))

  def eff_luck(self):
    '''Удача с учётом действия всех артефактов'''
    val = self.luck
    for a in self.artefacts:
      val += a.luck_mod
    return val

  def eff_luck_s(self):
    val = self.eff_luck()
    if val == self.luck:
      return cl.w(str(val))
    else:
      return cl.b("{0}".format(val))

  def enemyStr(self):
    result = cl.g("Это {0} {1} уровня - {2}\n".format(str(self.person_type), str(self.level), self.levelStr()))
    result += cl.w("Сл:") + self.eff_strength_s() + cl.w(" Лв:") + self.eff_agility_s() + cl.w(" Жв:") + self.eff_vitality_s() + cl.w(" Уд:") + self.eff_luck_s() + "\n"
    weaponstr = "Урон {0}-{1}".format(self.getMinStrike(), self.getMaxStrike())
    if (len(self.weapons) > 0):
      weaponstr += "    "
      for w in self.weapons:
        weaponstr += str(w)
        weaponstr += " "
      weaponstr = cl.lb(weaponstr)
    else:
      weaponstr = cl.w(weaponstr)
    weaponstr += "\n"
    result += weaponstr
    healthstr = "Здоровье {0}/{1}".format(self.current_health, self.getMaxHealth())
    if self.broken_leg:
      healthstr += cl.r(" Сломана нога")
    if self.broken_jaw:
      healthstr += cl.r(" Сломана челюсть")
    healthstr += "\n"
    if self.current_health > (self.getMaxHealth() * 2 / 3):
      result += cl.g(healthstr)
    elif self.current_health > (self.getMaxHealth() * 1 / 3):
      result += cl.y(healthstr)
    else:
      result += cl.r(healthstr)
    strikes = self.getStrikesAccuracy()
    accstr = ""
    if len(strikes) == 1:
      accstr = "Точность {0}%\n".format(strikes[0])
    elif len(strikes) == 2:
      accstr = "Точность 90%,   Второй удар {0}%\n".format(strikes[1])
    else:
      accstr = "Точность 90% - {1} ударов, Точность {2} удара {3}%\n".format(len(strikes) - 1, len(strikes), strikes[len(strikes) - 1])
    result += cl.w(accstr)
    if (self.eff_shield() > 0):
      shieldstr = "Броня {0}".format(self.eff_shield())
      shieldstr += "    "
      for s in self.shields:
        shieldstr += str(s)
        shieldstr += " "
      shieldstr += "\n"
      result += cl.w(shieldstr)
    return result

  def __str__(self):
    result = cl.g("Ты {0} {1} уровня - {2}\n".format(str(self.person_type), str(self.level), self.levelStr()))
    result += cl.g("А зовут тебя: ")
    result += self.name
    result += "\n"
    result += cl.y("Сейчас у тебя {0} опыта, а для прокачки надо {1}\n".format(self.skill, self.nextLevelSkill()))
    result += cl.w("Сл:") + self.eff_strength_s() + cl.w(" Лв:") + self.eff_agility_s() + cl.w(" Жв:") + self.eff_vitality_s() + cl.w(" Уд:") + self.eff_luck_s() + "\n"
    simple_artefacts_str = cl.w("Феньки:")
    simple_artefacts_count = 0
    power_artefacts_str = cl.w("Мощные феньки:")
    power_artefacts_count = 0
    for a in self.artefacts:
      if a.is_powerful:
        power_artefacts_count += 1
        power_artefacts_str += cl.b(" {0}".format(str(a)))
      else:
        simple_artefacts_count += 1
        simple_artefacts_str += cl.b(" {0}".format(str(a)))
    if simple_artefacts_count > 0:
      result += simple_artefacts_str
      result += "\n"
    if power_artefacts_count > 0:
      result += power_artefacts_str
      result += "\n"
    if self.mobile:
      result += cl.lb("У тебя есть мобильник\n")
    if self.sun_glass:
      result += cl.lb("У тебя есть тёмные очки\n")
    if self.tattoo:
      result += cl.lb("На тебе зоновская наколка\n")
    weaponstr = "Урон {0}-{1}".format(self.getMinStrike(), self.getMaxStrike())
    if (len(self.weapons) > 0):
      weaponstr += "    "
      for w in self.weapons:
        weaponstr += str(w)
        weaponstr += " "
      weaponstr = cl.lb(weaponstr)
    else:
      weaponstr = cl.w(weaponstr)
    weaponstr += "\n"
    result += weaponstr
    healthstr = "Здоровье {0}/{1}".format(self.current_health, self.getMaxHealth())
    if self.jaw_shield:
      healthstr += cl.b(" Зубная защита")
    if self.broken_leg:
      healthstr += cl.r(" Сломана нога")
    if self.broken_jaw:
      healthstr += cl.r(" Сломана челюсть")
    healthstr += "\n"
    if self.current_health > (self.getMaxHealth() * 2 / 3):
      result += cl.g(healthstr)
    elif self.current_health > (self.getMaxHealth() * 1 / 3):
      result += cl.y(healthstr)
    else:
      result += cl.r(healthstr)
    strikes = self.getStrikesAccuracy()
    accstr = ""
    if len(strikes) == 1:
      accstr = "Точность {0}%\n".format(strikes[0])
    elif len(strikes) == 2:
      accstr = "Точность 90%,   Второй удар {0}%\n".format(strikes[1])
    else:
      accstr = "Точность 90% - {1} ударов, Точность {2} удара {3}%\n".format(len(strikes) - 1, len(strikes), strikes[len(strikes) - 1])
    result += cl.w(accstr)
    if (len(self.shields) > 0):
      shieldstr = "Броня {0}".format(self.shield)
      shieldstr += "    "
      for s in self.shields:
        shieldstr += str(s)
        shieldstr += " "
      shieldstr += "\n"
      result += cl.w(shieldstr)
    if (self.pot > 0):
      result += cl.w("Косяки {0}\n".format(self.pot))
    if self.beer > 0:
      result += cl.w("Пиво {0}л.\n".format(round(self.beer, 1)))
    else:
      result += cl.r("Пива нет\n")
    if self.money > 0:
      result += cl.w("Бабки {0}".format(self.money))
    else:
      result += cl.r("Бабок нет")
    if self.stuff > 0:
      result += cl.w("\nХлам {0}".format(self.stuff))
    return result

  def step(self):
    '''Действия, выполняемые на каждом шаге'''
    health_recovery = 0
    break_healing_prob = 0
    for a in self.artefacts:
      if a.is_powerful:
        health_recovery += a.health_recovery
        break_healing_prob += a.break_healing_prob
    self.current_health += health_recovery
    if self.current_health > self.getMaxHealth():
      self.current_health = self.getMaxHealth()
    if random.randint(0, 100) < break_healing_prob:
      if self.broken_jaw:
        self.broken_jaw = False
        # Надо что-то написать о залечении челюсти
    if random.randint(0, 100) < break_healing_prob:
      if self.broken_leg:
        self.broken_leg = False
        # Надо что-то написать о залечении челюсти