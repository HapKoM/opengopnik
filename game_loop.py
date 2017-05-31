# -*- coding: UTF-8 -*-

from person import Person, Type
from colors import color as cl
import random
import artefacts

def prob(p):
  return random.randint(0, 100) < p

class GameLoop:
  STATE_NOT_STARTED = 0
  STATE_WAIT_CMD    = 1
  STATE_BATTLE_START= 2
  STATE_BATTLE      = 3
  STATE_FINISHED    = 4
  STATE_GYM         = 5
  STATE_CLUB        = 6
  STATE_HOSPITAL    = 7

  def __init__(self):
    self.state = GameLoop.STATE_NOT_STARTED
    self.person = None
    self.enemy = None
    self.rep_discovered = False
    self.girl_discovered = False
    self.kl_discovered = False
    self.bmar_discovered = False
    self.trn_discovered = False
    self.pr_discovered = False
    self.evil_enemies = False
    self.church_visited_ctr = 0
    # Минимальная ставка в клубе
    self.minimal_club_bet = 5
    self.cmds = {
      "w": self.walk,
      "s": self.showYourelf,
      "sv": self.showEnemy,
      "e": self.exitGame,
      "i": self.info_commands,
      "name": self.rename,
      "k": self.kickEnemy,
      "run": self.run,
      "mar": self.goToMarket,
      "bmar": self.goToBmarket,
      "pr": self.goToPriton,
      "trn": self.goToGym,
      "kl": self.goToClub,
      "rep": self.goToHospital,
      "girl": self.goToGirlfriend,
      "h": self.drinkBeer,
      "mh": self.drinkMuchBeer,
    }
    self.battle_cmds = {
      "s": self.showYourelf,
      "sv": self.showEnemy,
      "e": self.exitGame,
      "k": self.kickEnemy,
      "run": self.run,
      "h": self.drinkBeer,
    }
    self.gym_commands = {
      "w": self.walk,
      "1": self.trainStrength,
      "2": self.trainVitality,
      "3": self.trainSkill,
      "4": self.buyJawShield,
      "5": self.trainShield,
    }
    self.club_commands = {
      "w": self.walk,
      "p": self.play,
      "1": self.party,
      "2": self.spyForCheaters,
    }
    self.hospital_commands = {
      "w": self.walk,
      "h": self.heal,
      "r": self.repair,
    }

  def startNewGame(self):
    random.seed()
    default_name = cl.w("Раз") + cl.y("дол") + cl.r("бай")
    self.person = Person(Type.POTSAN, default_name)
    input(cl.w("Год 2xxx от Р.Х."))
    print(cl.w("Последний день ты пришел в универ"))
    print(cl.w("Ты по-страшному косил и забивал"))
    print(cl.w("Ты ещё мог сдать все задания, которые ты взял у друзей"))
    input(cl.w("Но тут..."))
    input(cl.y("Ректор: Ах ты урод, чёртов забивала. Вали из универа!"))
    input(cl.g("Ты: А типа чё?"))
    input(cl.y("Ректор: Ты отчислен мудак!!! Как ты был лохом так и останешься."))
    input(cl.r("Это слышали все и ты из пацана превратился в опущенного.") + "\n")
    print(cl.w("Ты не можешь стерпеть такой наезд, однако ректор офигительно крутой."))
    input(cl.w("Ты решил доказать свою крутизну всему миру (в твоем понимании - Городу)."))
    person_selected = False
    first_time = True
    while not person_selected:
      if first_time:
        print(cl.w("Выбери кем ты будешь:"))
      else:
        print(cl.w("А теперь выбирай:"))
      print(cl.w("0-Пацан"))
      print(cl.w("1-Отморозок"))
      print(cl.w("2-Гопник"))
      print(cl.w("3-Вор"))
      if first_time:
        print(cl.w("4-Чё за батва?"))
      val = input(cl.w(""))
      if first_time and val == "4":
        print(cl.lb("Пацан - это нормальный тип. (Бонус - Гёлфренд, Клуб)"))
        print(cl.lb("Отморозок - тупой корявый мудак. (Бонус - Самолечение царапин)"))
        print(cl.lb("Гопник - гоп он и ест гоп. (Бонус - Притон)"))
        print(cl.lb("Вор - везучий ублюдок. (Бонус - Воровство, Барыги)"))
        first_time = False
      else:
        if val == "1":
          self.person = Person(Type.OTMOROZOK, default_name)
        elif val == "2":
          self.person = Person(Type.GOPNIK, default_name)
          self.pr_discovered = True
        elif val == "3":
          self.person = Person(Type.VOR, default_name)
          self.bmar_discovered = True
        else: # По-умолчанию - пацан
          self.person = Person(Type.POTSAN, default_name)
          self.girl_discovered = True
          self.kl_discovered = True
        person_selected = True
    name = input(cl.g("А зовут тебя:"))
    if name != "":
      self.person.name = name
    print(cl.lb("Ты стоишь у дверей университета."))
    print(cl.lb("Отсюда ты начинаешь свой нелёгкий путь гопника."))
    print(cl.w("Доказать свою крутизну ты можешь, отпинывая разных мудаков."))
    print(cl.w("Тебе придётся поработать над собой, чтобы стать крутым."))
    print(cl.w("Введи ") + cl.y("i") + cl.w(" чтобы посмотреть команды, введи ") +
          cl.y("help") + cl.w(" чтобы узнать чё за ботва"))

  def generateEnemy(self):
    types = [Type.POTSAN, Type.OTMOROZOK, Type.GOPNIK, Type.VOR, Type.DOHLAK, Type.NEFOR, Type.MENT, Type.NARK]
    t = random.choice(types)
    minLevel = self.person.level - 5
    if minLevel < 0:
      minLevel = 0
    maxlevel = minLevel + 10
    level = random.randint(minLevel, maxlevel)
    enemy = Person(t, "enemy")
    for i in range(0, level):
      enemy.levelUp(silent=True)
    enemy.money = random.randint(0, level)
    enemy.stuff = random.randint(0, level)
    if prob(level):
      enemy.artefacts.append(random.choice([artefacts.GodSaveRing(), artefacts.GodHelpRing(), artefacts.MegaRing(), artefacts.GodForgiveRing()]))
    return enemy

  def meetGod(self):
    def meetGodImpl(person):
      '''Реализация случайного благославления'''
      choice = random.choice([0, 1, 2, 3, 4, 5, 6])
      god_say = ""
      if choice == 0:
        god_say += cl.b("Да увеличится, офигенно, твоя понтовость среди гопоты!\n")
        god_say += cl.b("Получи 100!")
        person.pont += 100
      elif choice == 1:
        god_say += cl.b("Да увеличится твоя понтовость!")
        person.increaseExp(self.person.nextLevelSkill() - person.skill)
      elif choice == 2:
        god_say += cl.b("Да увеличится твоя сила!")
        person.strength += 1
        person.current_health = person.getMaxHealth()
      elif choice == 3:
        god_say += cl.b("Да возрастут твои силы жизненные!")
        person.vitality += 1
        person.current_health = person.getMaxHealth()
      elif choice == 4:
        god_say += cl.b("Да уменьшится твоя корявость!")
        person.agility += 1
      elif choice == 5:
        god_say += cl.b("Накладываю на тебя защиту!")
        person.shield += 1
      elif choice == 6:
        god_say += cl.b("Дарю тебе феньку!")
        variants = [artefacts.GodSaveRing(), artefacts.GodHelpRing(), artefacts.MegaRing(), artefacts.GodForgiveRing()]
        artefact = random.choice(variants)
        if artefact.description != "":
          god_say += "\n" + cl.b(artefact.description)
        person.artefacts.append(artefact)
      input(god_say)

    input(cl.w("Бродя по окрестностям с самыми грязными намерениями..."))
    input(cl.w("Ты наткнулся на храм Божий."))
    if self.church_visited_ctr == 0:
      input(cl.w("Раз такая батва..."))
      input(cl.w("Надо типа помолиться Господу Богу..."))
      input(cl.w("Как делают новые руссские."))
      input(cl.g("\"Господи, Братан, прости грешника\". - Начал было ты..."))
      input(cl.b("Громовой голос: \"Да пошёл ты нахрен!\""))
      input(cl.g(" - Эээ.. типа.. а чё?.."))
      input(cl.b(" - \"а чё?\" блин! ") + self.person.name + cl.b("-" + str(self.person.person_type) + " чёртов!"))
      input(cl.g("Ну.."))
      input(cl.b("Ладна насылаю на тебя, типа, \"моё благославление\""))
      meetGodImpl(self.person)
      print(cl.b("А теперь вали отсюда и никогда здесь не появляйся!"))
      print("")
      print(cl.w("Ты идёшь дальше"))
      print(cl.w("Ничё не происходит"))
    elif self.church_visited_ctr == 1:
      input(cl.w("В прошлый раз Бог сказал чтобы ты не осквернял своей рожей святой храм"))
      input(cl.w("Но надо бы типа помолиться о прощении"))
      input(cl.g("\"Господи, Братан, прости грешника опять\"."))
      input(cl.b("Бог: \"Да блин, упорный чудак!\""))
      input(cl.b("Ладно насылаю на тебя, типа, \"моё благославление\" снова"))
      meetGodImpl(self.person)
    else:
      input(cl.b("Бог: \"А ты опять.\""))
      input(cl.b("Ну ладно насылаю на тебя \"благославление\""))
      meetGodImpl(self.person)
      print(cl.b("А теперь проваливай!"))
    self.church_visited_ctr += 1

  def walk(self):
    if self.state != GameLoop.STATE_WAIT_CMD:
      self.state = GameLoop.STATE_WAIT_CMD
      return
    self.person.step()
    if prob(1):
      self.meetGod()
      return
    if not self.rep_discovered:
      if prob(5):
        print(cl.lb("Ты спросил у прохожего где тут больница."))
        self.rep_discovered = True
    if not self.trn_discovered:
      if prob(5):
        print(cl.lb("На стене реклама: \"Жизнь тяжела. Если не хочешь сдохнуть качайся!\"."))
        self.trn_discovered = True
    r = random.uniform(0, 100)
    if r < 5:
      if not self.evil_enemies:
        print(cl.y("Ты зашёл на тропинку где бродит искитимская гопота."))
        self.evil_enemies = True
      else:
        print(cl.y("Ты вышел с тропинки."))
        self.evil_enemies = True
      return
    if r < 60:
      print(cl.w("Ничё не происходит."))
      return
    if r < 70:
      print(cl.w("Совсем ничё не происходит."))
      return
    newenemy = self.generateEnemy()
    aggressive_types = [Type.POTSAN, Type.OTMOROZOK, Type.GOPNIK, Type.VOR]
    aggressive = random.choice([True, False]) and (newenemy.person_type in aggressive_types)
    if newenemy.person_type in [Type.POTSAN, Type.OTMOROZOK, Type.GOPNIK, Type.VOR, Type.DOHLAK, Type.NEFOR, Type.NARK]:
      aggressive_str = ""
      if aggressive:
        aggressive_str = ", ищущий кого отпинать"
      print(cl.y("Идёт {0} {1} уровня{2}. Хочешь наехать?").format(str(newenemy.person_type), str(newenemy.level), aggressive_str))
      reply = input()
      if reply == "y":
        variants = [0, 1]
        v = random.choice(variants)
        if v == 0:
          print(cl.w("Слышь Вась.."))
          print(cl.r("А чё ваще?"))
        else:
          print(cl.r("Пацан ты из какого района?"))
          print(cl.w("А ты по пинкам суди!"))
        self.enemy = newenemy
        self.state = GameLoop.STATE_BATTLE_START
        return
      elif aggressive:
        found_threshold = 50
        val = random.uniform(0, 100)
        if val > found_threshold:
          print(cl.r("Он тебя заметил."))
          print(cl.r("Эй мудак?!"))
          self.enemy = newenemy
          self.state = GameLoop.STATE_BATTLE_START
        else:
          print(cl.g("Ты смылся."))
    elif newenemy.person_type == Type.MENT:
      print(cl.y("Идёт ментяра {0} уровня гроза гопов.".format(str(newenemy.level))))
      if self.person.sun_glass:
        print(cl.g("Ты напялил тёмные очки и мент не узнал твою рожу, которая висит на почётном стенде \"Разыскиваются за гопничество\""))
        return
      found_threshold = 50
      val = random.uniform(0, 100)
      if val > found_threshold:
        print(cl.r("Запалил!"))
        print(cl.r("Блин! это же ") + self.person.name + cl.r(" - известный {0}".format(str(self.person.person_type))))
        self.enemy = newenemy
        self.state = GameLoop.STATE_BATTLE_START
      else:
        print(cl.g("Ты затаился, прикинулся не гопом... Мент вроде не заметил"))
    elif newenemy.person_type == Type.MANIAC:
      print(cl.y("Идёт Маньячок {0}, ищущий кого отпинать.".format(str(newenemy.level))))
      found_threshold = 50
      val = random.uniform(0, 100)
      if val > found_threshold:
        print(cl.r("Он тебя заметил."))
        print(cl.r("Я МАНЬЯК!!!"))
        print(cl.w("Рад познакомиться - " + str(self.person.person_type)))
        self.enemy = newenemy
        self.state = GameLoop.STATE_BATTLE_START
      else:
        print(cl.g("Ты смылся."))

  def showYourelf(self):
    print(str(self.person))

  def showEnemy(self):
    if self.enemy:
      print(self.enemy.enemyStr())

  def exitGame(self):
    print(cl.y("Блин не быть тебе нормальным пацаном"))
    print(cl.lb("А результат:"))
    self.showYourelf()
    input()
    self.state = GameLoop.STATE_FINISHED

  def info_commands(self):
    print(cl.w("Напиши: ") + cl.y("w") + cl.w(" чтобы шататься по окрестностям - искать на свою жопу приключения"))
    print(cl.w("Напиши: ") + cl.y("mar") + cl.w(" чтобы идти на рынок"))
    if self.bmar_discovered:
      print(cl.w("Напиши: ") + cl.y("bmar") + cl.w(" чтобы идти к барыгам"))
    if self.rep_discovered:
      print(cl.w("Напиши: ") + cl.y("rep") + cl.w(" чтобы идти к ветеринару"))
    if self.girl_discovered:
      print(cl.w("Напиши: ") + cl.y("girl") + cl.w(" чтобы идти к своей девчонке"))
    if self.kl_discovered:
      print(cl.w("Напиши: ") + cl.y("kl") + cl.w(" чтобы идти в клуб"))
    if self.pr_discovered:
      print(cl.w("Напиши: ") + cl.y("pr") + cl.w(" чтобы идти в местный притон гопоты"))
    if self.trn_discovered:
      print(cl.w("Напиши: ") + cl.y("trn") + cl.w(" чтобы идти в качалку"))
    print(cl.w("Напиши: ") + cl.y("s") + cl.w(" чтобы посмотреть в лужу на свою уродскую рожу"))
    print(cl.w("Напиши: ") + cl.y("sv") + cl.w(" чтобы присмотреться к пинаемому мудаку"))
    print(cl.w("Напиши: ") + cl.y("k") + cl.w(" чтобы гасить мудака который тебе попался на дороге"))
    print(cl.w("Напиши: ") + cl.y("run") + cl.w(" чтобы смыться от мудака который тебе попался на дороге"))
    print(cl.w("Напиши: ") + cl.y("v") + cl.w(" чтобы позвать подкрепление"))
    print(cl.w("Напиши: ") + cl.y("kos") + cl.w(" чтобы схватить косяк"))
    print(cl.w("Напиши: ") + cl.y("h") + cl.w(" чтобы выпить пиво (если не охото к ветеринару)"))
    print(cl.w("Напиши: ") + cl.y("mh") + cl.w(" чтобы набухаться до чёртиков"))
    print(cl.w("Напиши: ") + cl.y("name") + cl.w(" чтобы сменить погоняло"))
    print(cl.w("Напиши: ") + cl.y("e") + cl.w(" если захочешь выйти"))

  def rename(self):
    print(cl.g("Звали тебя: " + self.person.name))
    name = input(cl.g("А теперь будут: ") + cl.w(""))
    if name != "":
      self.person.name = cl.w(name)

  def startBattle(self):
    # TODO необходимо учитывать бонус ловкости персонажа и врага
    self.state = GameLoop.STATE_BATTLE

  def kickEnemy(self):
    if self.state != GameLoop.STATE_BATTLE:
      print(cl.y("Чё машешь копытами? Ищи мудака которого будешь пинать!"))
    else:
      my_strikes = self.person.getStrikesAccuracy()
      first_strike = True
      for p in my_strikes:
        if not first_strike:
          print(cl.g("Из-за большой ловкости ты можешь пнуть ещё раз"))
        first_strike = False
        if prob(p):
          strike = random.randint(self.person.getMinStrike(), self.person.getMaxStrike())
          doubleStrike = prob(50)
          if doubleStrike:
            strike = self.person.getMaxStrike() * 2
            print(cl.g("Точный удар!!!"))
          strike -= self.enemy.eff_shield()
          if strike < 0:
            strike = 0
          new_enemy_health = self.enemy.current_health - strike
          self.enemy.current_health = new_enemy_health
          print(cl.g("Ты пнул врага на {0}з. У него осталось {1}".format(strike, new_enemy_health)))
          if self.enemy.isDead():
            print(cl.g("Враг сдох."))
            self.finishBattle()
            return
        else:
          print(cl.r("Ты промазал"))
      enemy_strikes = self.enemy.getStrikesAccuracy()
      first_strike = True
      for p in enemy_strikes:
        if not first_strike:
          print(cl.r("Из-за большой ловкости враг может пнуть ещё раз"))
        first_strike = False
        if prob(p):
          strike = random.randint(self.enemy.getMinStrike(), self.enemy.getMaxStrike())
          doubleStrike = prob(50)
          if doubleStrike:
            strike = self.enemy.getMaxStrike() * 2
            variants = [0, 1, 2]
            v = random.choice(variants)
            if v == 0:
              print(cl.r("Враг:Сдохни урод!!!"))
            elif v == 1:
              print(cl.r("Враг:Получи гнида!!"))
            else:
              print(cl.r("Тебе не хило врезали!"))
          strike -= self.person.eff_shield()
          if strike < 0:
            strike = 0
          new_person_health = self.person.current_health - strike
          self.person.current_health = new_person_health
          print(cl.r("Он пнул тебя на {0}з. У тебя осталось {1}".format(strike, new_person_health)))
          if self.person.isDead():
            print(cl.r("Ты сдох."))
            self.exitGame()
            return
        else:
          print(cl.g("Враг промазал"))

  def finishBattle(self):
    #TODO надо вычислить и добавить очки опыта персонажу
    exp = self.enemy.eff_strength() + self.enemy.eff_agility() + self.enemy.eff_vitality() + self.enemy.eff_luck()
    print(cl.y("За отпин врага ты получаешь {0} качков опыта".format(exp)))
    skillToLevel = self.person.nextLevelSkill() - self.person.skill
    #self.person.increaseExp()
    if exp < skillToLevel:
      self.person.increaseExp(exp)
      print(cl.y("Ты запинал слишком слабого мудака для увеличения понтовости"))
      print(cl.y("Сейчас у тебя {0} качков опыта, А для прокачки надо {1}".format(self.person.skill, self.person.nextLevelSkill())))
    else:
      self.person.increaseExp(exp)
      print(cl.y("Сейчас у тебя {0} качков опыта. До следующей прокачки надо {1}".format(self.person.skill, self.person.nextLevelSkill())))
    print(cl.b("Пиво победителю!"))
    self.person.beer += 2.0
    #TODO надо обобрать побеждённого врага
    self.person.money += self.enemy.money
    self.person.stuff += self.enemy.stuff
    if self.enemy.artefacts:
      print(cl.b("Оба на! Колечко! Вот свезло так свезло!"))
      print(cl.b(self.enemy.artefacts[0].description))
      self.person.artefacts.extend(self.enemy.artefacts)
    self.enemy = None
    self.state = GameLoop.STATE_WAIT_CMD

  def run(self):
    if self.state != GameLoop.STATE_BATTLE:
      print(cl.y("Забегал мудак."))
      self.walk()
    else:
      if self.person.broken_leg:
        print(cl.r("Ты не можешь убежать на сломаной ноге"))
      else:
        if self.person.level == 0:
          print(cl.r("Враг: Засранец!"))
        else:
          print(cl.r("Враг: Трусливый засранец!"))
          self.person.levelDown()
        self.state = GameLoop.STATE_WAIT_CMD

  def goToMarket(self):
    pass #TODO пока не реализовано

  def goToBmarket(self):
    if not self.bmar_discovered:
      print(cl.y("Туда любого дебила с улицы не пропустят - сначала докажи, что ты не засранец - отпинай побольше ублюдков"))
    else:
      pass #TODO пока не реализовано

  def goToPriton(self):
    if not self.pr_discovered:
      print(cl.r("Тебя мудака такого туда не пустят - поднимай понтовость"))
    else:
      pass #TODO пока не реализовано

  def goToGym(self):
    if not self.trn_discovered:
      print(cl.y("Ты пока не знаешь где в этом районе качалка"))
    else:
      print(cl.w("Ты пришёл в качалку напиши ") + cl.y("w") + cl.w(" чтобы уйти"))
      price_1 = "20"
      price_2 = "20"
      price_3 = "10"
      price_4 = "30"
      price_5 = "20"
      if self.person.money < 10:
        price_3 = cl.r("10")
      if self.person.money < 20:
        price_1 = cl.r("20")
        price_2 = cl.r("20")
        price_5 = cl.r("20")
      if self.person.money < 30:
        price_4 = cl.r("30")
      print(cl.w(" 1 - ") + price_1 + cl.w(" качаться гантелями и штангой(Сила +1)"))
      print(cl.w(" 2 - ") + price_2 + cl.w(" качаться на тренажёрах(Выносливость +1)"))
      print(cl.w(" 3 - ") + price_3 + cl.w(" прокачать 10 качков опыта"))
      print(cl.w(" 4 - ") + price_4 + cl.w(" купить зубную защиту боксёров(-75% что сломают челюсть)"))
      print(cl.w(" 5 - ") + price_5 + cl.w(" прокачать пресс(Броня +1)"))
      self.state = GameLoop.STATE_GYM

  def trainStrength(self):
    if self.person.money < 20:
      print(cl.r("Не хватает"))
    else:
      self.person.money -= 20
      self.person.strength += 1
      print(cl.g("Ты прокачиваешь силу"))
      print(cl.b("Сила +1"))

  def trainVitality(self):
    if self.person.money < 20:
      print(cl.r("Не хватает"))
    else:
      self.person.money -= 20
      self.person.vitality += 1
      print(cl.g("Ты прокачиваешь выносливость"))
      print(cl.b("Выносливость +1"))

  def trainSkill(self):
    if self.person.money < 10:
      print(cl.r("Не хватает"))
    else:
      self.person.money -= 10
      self.person.increaseExp(10)
      print(cl.g("Ты тренируешься"))
      print(cl.b(" +10 качков опыта"))

  def buyJawShield(self):
    if self.person.money < 30:
      print(cl.r("Не хватает"))
    else:
      if self.person.jaw_shield:
        print(cl.y("У тебя есть эта штучка"))
      else:
        self.person.money -= 30
        self.person.jaw_shield = True
        print(cl.g("Ты купил защиту"))

  def trainShield(self):
    if self.person.money < 20:
      print(cl.r("Не хватает"))
    else:
      self.person.money -= 20
      self.person.shield += 1
      print(cl.g("Ты прокачиваешь пресс"))
      print(cl.b("Броня +1"))

  def goToClub(self):
    if not self.kl_discovered:
      print(cl.y("Ты пока не знаешь где в этом районе клуб"))
    else:
      print(cl.w("Ты пришёл в клуб напиши ") + cl.y("w") + cl.w(" чтобы уйти"))
      print(cl.w(" Здесь можно сыграть в карты (") + cl.y("p") + cl.w(" Минимальная ставка- 5р.)"))
      price_1 = "15"
      price_2 = "22"
      if self.person.money < 15:
        price_1 = cl.r("15")
      if self.person.money < 22:
        price_2 = cl.r("22")
      print(cl.w(" 1 - ") + price_1 + cl.w(" потусоваться на дискотеке(Ловкость +1)"))
      print(cl.w(" 2 - ") + price_2 + cl.w(" разузнать приемы мухлёжников(Удача +1)"))
      self.state = GameLoop.STATE_CLUB
      self.minimal_club_bet = 5

  def play(self):
    if self.person.money < self.minimal_club_bet:
      print(cl.r("Не хватает"))
      return
    print(cl.w("Ты поставил {0} рублей".format(self.minimal_club_bet)))
    p = self.person.luck
    if p > 90:
      p = 90
    win = prob(p)
    if win:
      print(cl.w("Ты выиграл {0} рублей".format(self.minimal_club_bet)))
      print(cl.y("Ты получаешь 4 качков опыта"))
      self.person.money += self.minimal_club_bet
      self.person.increaseExp(4)
      self.minimal_club_bet += 2
      print(cl.y("Ставки изменились. Теперь ставка - {0}".format(self.minimal_club_bet)))
    else:
      print(cl.w("Ты проиграл {0} рублей".format(self.minimal_club_bet)))
      self.person.money -= self.minimal_club_bet
      if self.person.money < 0:
        self.person.money = 0
      self.minimal_club_bet = 5

  def party(self):
    if self.person.money < 15:
      print(cl.r("Не хватает"))
    else:
      self.person.money -= 15
      self.person.agility += 1
      print(cl.g("Ты прокачиваешь ловкость"))
      print(cl.b("Ловкость +1"))

  def spyForCheaters(self):
    if self.person.money < 22:
      print(cl.r("Не хватает"))
    else:
      self.person.money -= 22
      self.person.luck += 1
      print(cl.g("Ты прокачиваешь удачу"))
      print(cl.b("Удача +1"))

  def goToHospital(self):
    if not self.rep_discovered:
      print(cl.y("Сначала найди где находится эта больница"))
    else:
      print(cl.w("Ты пришёл на ремонт, к ветеринару напиши ") + cl.y("w") + cl.w(" чтобы уйти"))
      if self.person.current_health >= self.person.getMaxHealth():
        print("Док: вали отсюда ты здоров")
        return
      else:
        print("Док: не волнуйся всё зарастёт как на собаке")
      price_1 = "3"
      price_2 = "7"
      if self.person.money < 3:
        price_1 = cl.r("3")
      if self.person.money < 7:
        price_2 = cl.r("7")
      print(cl.g("h") + cl.w(" - за ") + price_1 + cl.w(" рубля тебя залатают"))
      print(cl.g("r") + cl.w(" - за ") + price_2 + cl.w(" рублей починят переломы"))
      self.state = GameLoop.STATE_HOSPITAL

  def heal(self):
    if self.person.money < 3:
      print(cl.r("Блин халявщик, медицина не бесплатная"))
      return
    phrases = [
      cl.y("Эй, Док а зачем тебе паяльник?\n") + "Док: Молчи животное!",
      "Щас гайки подтянем и будешь как новый"
    ]

  def repair(self):
    if self.person.money < 7:
      return
    print("Ого! Да тебя не иначе как грузовик откатал!")
    print(cl.g("Твои переломы залечены."))
    self.person.broken_jaw = False
    self.person.broken_leg = False
    self.person.money -= 7

  def goToGirlfriend(self):
    if not self.girl_discovered:
      print(cl.r("У тебя пока нет девчонки"))
    else:
      if self.person.money < 12:
        print(cl.y("Ну не пойдёшь же как придурок без ничего"))
      else:
        print(cl.g("Ты пришёл к своей подруге."))
        print(cl.y("Ты купил ей чё-то, потратив 12 рублей."))
        print(cl.g("Ты расслабился, отдохнул и снова можешь творить свои гоповские дела."))
        self.person.money -= 12
        self.person.current_health = self.person.getMaxHealth()

  def drinkBeer(self):
    if self.person.current_health >= self.person.getMaxHealth():
      print(cl.y("Блин только тупить не надо - и так здоровья до фига."))
      return
    if self.person.broken_jaw:
      print(cl.r("Ты не можешь пить из-за сломаной челюсти."))
      return
    if self.person.beer > 0:
      add_health = self.person.getMaxHealth() - self.person.current_health
      if add_health > 5:
        add_health = 5
      self.person.current_health += add_health
      self.person.beer -= 0.5
      if self.person.beer < 0:
        self.person.beer = 0
      print(cl.g("Пиво прибавляет {0}з. Здоровья:{1}/{2}. Осталось {3}л. пива".format(
        add_health, self.person.current_health, self.person.getMaxHealth(), round(self.person.beer, 1))))
    else:
      print(cl.r("Пива нету"))

  def drinkMuchBeer(self):
    if self.person.current_health >= self.person.getMaxHealth():
      print(cl.y("Блин только тупить не надо - и так здоровья до фига."))
      return
    pass

  def greetings(self):
    lines = [
      "┌─── ┌───┐ ┌───┐ ╷   ╷ ╷   ╷ ╷   ╷",
      "│    │   │ │   │ │   │ │   │ │  ╱ ",
      "│    │   │ │   │ │   │ │   │ │ ╱  ",
      "│    │   │ │   │ ├───┤ │  ╱│ │╱   ",
      "│    │   │ │   │ │   │ │ ╱ │ │╲   ",
      "│    │   │ │   │ │   │ │╱  │ │ ╲  ",
      "│    │   │ │   │ │   │ │   │ │  ╲ ",
      "╵    └───┘ ╵   ╵ ╵   ╵ ╵   ╵ ╵   ╵",
      "                      Версия 2.00 ",
    ]
    print(cl.grey(lines[0]))
    print(cl.b(lines[1]))
    print(cl.g(lines[2]))
    print(cl.cyan(lines[3]))
    print(cl.r(lines[4]))
    print(cl.magenta(lines[5]))
    print(cl.y(lines[6]))
    print(cl.w(lines[7]))
    print(cl.g(lines[8]))

  def finished(self):
    return self.state == GameLoop.STATE_FINISHED

  def step(self):
    if self.state == GameLoop.STATE_NOT_STARTED:
      self.greetings()
      print("\n")
      print(cl.y("    Нажми какую-нибудь кнопку"))
      input(cl.w(""))
      self.startNewGame()
      self.state = GameLoop.STATE_WAIT_CMD
    elif self.state == GameLoop.STATE_WAIT_CMD:
      cmd = input(cl.w("\\"))
      if cmd in self.cmds.keys():
        self.cmds[cmd]()
    elif self.state == GameLoop.STATE_BATTLE_START:
      self.startBattle()
    elif self.state == GameLoop.STATE_BATTLE:
      cmd = input(cl.w("Битва\\"))
      if cmd in self.battle_cmds.keys():
        self.battle_cmds[cmd]()
    elif self.state == GameLoop.STATE_GYM:
      cmd = input(cl.w("Качалка\\"))
      if cmd in self.gym_commands.keys():
        self.gym_commands[cmd]()
    elif self.state == GameLoop.STATE_CLUB:
      cmd = input(cl.w("Клуб\\"))
      if cmd in self.club_commands.keys():
        self.club_commands[cmd]()
    elif self.state == GameLoop.STATE_HOSPITAL:
      cmd = input(cl.w("Ветеринар\\"))
      if cmd in hospital_commands.keys():
        hospital_commands[cmd]()
    else:
      pass