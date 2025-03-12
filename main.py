import random
import hashlib
import time
import json
import os

# Пути к файлам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REM_DIR = f"{BASE_DIR}/Data/REMEMBER.json"
STR_DIR = f"{BASE_DIR}/Data/STRINGS.json"
NAMES_DIR = f"{BASE_DIR}/Data/NAMES.json"

# Функция получения строк
def text_path(path=''):
    # Получение случайной строки по пути
    try:
        p = path.split('.')
        dir = STR
        for i in p:
            dir = dir[i]
        return random.choice(dir)
    except:
        return path

# Загрузка надуманных данных
try:
    with open(REM_DIR, 'r', encoding='utf-8') as file:
        REM = json.load(file)
except Exception as e:
    print(f"[{e}] {text_path('system.remember_error')}")
    REM = []

# Загрузка строк
try:
    with open(STR_DIR, 'r', encoding='utf-8') as file:
        STR = json.load(file)
except Exception as e:
    print(f"[{e}] {text_path('system.text_error')}")
    AMMO = -1

# Загрузка списка имён
try:
    with open(NAMES_DIR, 'r', encoding='utf-8') as file:
        NAMES = json.load(file)
except Exception as e:
    print(f"[{e}] {text_path('system.names_error')}")
    NAMES = ["John"]

# Константы
CODE = [4, 9, 2, 8]
LR = 1
HR = 6
AMMO = HR
KILL = random.randint(LR, HR)
HAND = True
N2 = random.choice(NAMES)
MOVES = 0
WAIT_TIME = 2.5
VER = "1.0r"
'''
Параметры противника
-----------------------------------
AG - Агрессия (Aggressive)
FE - Страх (Fear)
'''
TRAITS = {
    "AG": random.random(),
    "FE": random.random()
}

# Функции
def save():
    # Обновление списка памяти
    with open(REM_DIR, 'w', encoding='utf-8') as file:
        json.dump(REM, file, ensure_ascii=False, indent=4)

def hash_code(code):
    # Функция хеша
    return hashlib.sha256(code.encode()).hexdigest()

# Вступительное сообщение
print(f"{text_path('welcome')}{VER}\n")

# Случайная подсказка
print(text_path('hint'))

# Внезапное вспоминание
if N2 in REM and N2 != "???":
    print(text_path('remember'))
REM.append(N2)

# Игровой цикл
while AMMO > 0:
    # Обновление количества летальных пуль
    if MOVES % 5 == 0 and MOVES != 0:
        HR -= 1
        AMMO = HR
        KILL = random.randint(LR, HR)
        print(text_path("game.harding"))
    
    # Если в руке
    if HAND:
        print(f"{text_path('game.selector.self.main')} {N2} (he)?\n")
        com = input("> ").split()
        if not com:
            com = ['']
        
        # Спин
        if com[0] == '':
            AMMO = HR
            KILL = random.randint(LR, HR)
            print(text_path('game.choice.spin'))
            MOVES += 1
        
        # Если выбрали себя
        elif com[0].lower() == "me":
            print(text_path('game.choice.self.action'))
            time.sleep(WAIT_TIME)
            # Если патрон оказался летальным
            if AMMO == KILL:
                print(text_path('game.choice.self.die'))
                AMMO = -1
            
            # Если патрон холостой
            else:
                print(text_path('game.choice.self.survive'))
                AMMO -= 1
                MOVES += 1
        
        # Если выбрали противника
        elif com[0].lower() == "he":
            print(text_path('game.choice.enemy.action'))
            time.sleep(WAIT_TIME)
            # Если патрон оказался летальным
            if AMMO == KILL:
                print(text_path('game.choice.enemy.die'))
                code = random.choice(CODE)
                if random.random() > 0.5:
                    print(f"{text_path('game.selector.ending.story')} ''cc: {code} at index {CODE.index(code)}''.")
                AMMO = -1
            
            # Если патрон холостой
            else:
                print(text_path('game.choice.enemy.survive'))
                AMMO -= 1
                HAND = False
                MOVES += 1
        
        # Был введён чит-код на x-ray
        elif hash_code(com[0].lower()) == "1790419d6d0b0488e5d23463f02ae52f563d37edba379b275fc026c591336cb9":
            print(f"{text_path('game.selector.cheat.xray.0')} {KILL} {text_path('game.selector.cheat.xray.1')} {AMMO}\n")
        
        # Был введён чит-код на изменение имени
        elif len(com) == 2 and hash_code(com[0].lower()) == "82a3537ff0dbce7eec35d69edc3a189ee6f17d82f353a553f9aa96cb0be3ce89":
            # Проверка на валидность
            if com[1]:
                N2 = com[1]
            else:
                print(text_path('game.selector.cheat.name.error'))
                continue
            REM.append("custom")
            print(f"{text_path('game.selector.cheat.name.ok')} {N2}.\n")
        
        # Чит-код на пьянку
        elif hash_code(com[0].lower()) == "1d8176d17935a44c5d8cd0687a0e81f3c38415e4b6e4cecbeead791d3e1dc37d":
            print(text_path('game.selector.cheat.who'))
            AMMO = -1
        
        # Если напечатано не то
        else:
            continue
    
    # Ход противника
    else:
        print(text_path('game.enemy.thinking'))
        time.sleep(WAIT_TIME)
        action1 = random.random()
        action2 = random.random()
        
        factor = (AMMO - AMMO * TRAITS["FE"] - 4 * TRAITS["AG"]) / 6
        
        if action1 > TRAITS["FE"] / 2:
            # Если выбрал игрока
            if action2 >= factor:
                # Если патрон убийственный 
                if AMMO == KILL:
                    print(text_path('game.enemy.player.kill'))
                    if "custom" in REM:
                        print(text_path('game.enemy.cheating'))
                    AMMO = -1
                
                # Если патрон холостой
                else:
                    print(text_path('game.enemy.player.survive'))
                    AMMO -= 1
                    HAND = True
                    MOVES += 1
            
            # Он выбрал себя
            else:
                # Если патрон убийственный
                if AMMO == KILL:
                    print(text_path('game.enemy.self.kill'))
                    AMMO = -1
                
                # Если патрон холостой
                else:
                    print(text_path('game.enemy.self.survive'))
                    AMMO -= 1
                    MOVES += 1
        
        # Выбрал прокрутить револьвер
        else:
            print(text_path('game.enemy.spin'))
            MOVES += 1

save()
