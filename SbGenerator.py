# -*- coding: utf-8 -*-
# Zendes 2.5 WORLD GENERATION 2.8

# Генератор мира для игры Zendes 2.5


# import noise # Шум Перлина (пока не используется в этом генераторе)
import random
import os

PATH = os.path.dirname(os.path.abspath(__file__))+"\\"  # Путь к папке, в которой мы находимся

block_size = 45  # размер блока
block_size_inverted = 1.0 / float(block_size)

generation_size = 20  # GenerationSize
# ogs = int(generation_size*block_size_inverted) #GenerationSize in blocks

# Biom configs
PlainsB = (235, 230, 3, 10, 100, 0)  # world_down, world_up, up_blocks, Trees, chance, biom_id
DesertB = (250, 240, 5, 1000, 60, 1)
MountainsB = (220, 200, 19, 20, 70, 2)
ForestB = (250, 230, 3, 1, 100, 3)
SeaB = (268, 264, 5, 0, 50, 4)

BIOMS0 = [PlainsB, DesertB, MountainsB, ForestB]

# Деревья
STRUCTURES_PATH = PATH + os.path.join("resources", "structures", "")  # Путь к папке со структурами

TreeS = (STRUCTURES_PATH + os.path.join("tree.txt"),
         25)  # путь к файлу со структурой, шанс генерации (колличество повторов в списке структур)
Tree2S = (STRUCTURES_PATH + os.path.join("tree2.txt"), 25)
WheatS = (STRUCTURES_PATH + os.path.join("wheat.txt"), 10)

TREES0 = [TreeS, WheatS, Tree2S]

BIOMS = []
# Генерация списка с биомами с колличеством их копий которое указано в chance в кортеже биома
for BIOM in BIOMS0:
    number_of_copies = BIOM[4]
    for _ in range(number_of_copies):  # Цикл в диапазоне(сколько копий нужно)
        BIOMS.append(BIOM)

TREES = []
for TREE in TREES0:
    number_of_copies = TREE[1]
    for _ in range(number_of_copies):  # Цикл в диапазоне(сколько копий нужно)
        TREES.append(TREE[0])


# Главная функция - генератор мира
def generation(seed, mode, x, y, flatdata=10):
    x = int(x / block_size)
    y = int(y / block_size)
    # seed - interger или float ключ генерации (любое число) может быть отрицательным
    # mode - string режим генерации (в файле сечас только "optim#normal")
    # x, y - int кoординаты блока
    # flatdata - integer больше не используется (высота в режиме плоского мира)


    # основной режим генерации
    if mode == "optim#normal":
        def get_hight(x, y):

            # определение левой и правой точек и их биомов
            left_point = int(x / generation_size) * generation_size
            random.seed(seed)
            random.seed(int(
                (left_point * 100.0) / generation_size / random.randint(10 * generation_size, 30 * generation_size)))
            left_biom = random.choice(BIOMS)

            right_point = (int(x / generation_size) * generation_size) + generation_size
            random.seed(seed)
            random.seed(int(
                (right_point * 100.0) / generation_size / random.randint(10 * generation_size, 30 * generation_size)))
            right_biom = random.choice(BIOMS)
            # Если координаты нулевые то по-умолчанию ставится биом Plains - равнина
            # (биом под персонажем в начале)
            if left_point * block_size_inverted == 0:
                left_biom = ForestB

            if right_point * block_size_inverted == 0:
                right_biom = ForestB

            # определение высот 2-х основных точек, левой и правой
            random.seed(seed * left_point * generation_size)
            left_point_H = random.randint(left_biom[1], left_biom[0])

            random.seed(seed * right_point * generation_size)
            right_point_H = random.randint(right_biom[1], right_biom[0])
            biom = PlainsB

            # если блок совпадает с левой точкой
            if left_point == x:
                point_hight = left_point_H
                biom = left_biom

            # если блок совпадает с правой точкой
            if right_point == x:
                point_hight = right_point_H
                biom = right_biom

            point_hight = None

            if point_hight is None:  # Если высота блока ещё не определена:
                rsn = 0

                # Определения влияния точек на блок
                left_percent = float(x - left_point) / generation_size
                right_percent = float(right_point - x) / generation_size

                # Влияние высоты точек на высоту блока
                lpercented = left_point_H * right_percent
                rpercented = right_point_H * left_percent

                # Определение высоты блока
                point_hight = (left_point_H * right_percent) + (right_point_H * left_percent)

                # Определение биома для блока
                if left_biom[-1] != right_biom[-1]:
                    random.seed(seed + x + y + point_hight)
                    temp = int(right_point_H * right_percent * 100)
                    if random.randint(-temp, temp) >= 0:
                        biom = left_biom
                    else:
                        biom = right_biom
                else:
                    biom = left_biom

            return point_hight, biom

        point_hight, biom = get_hight(x, y)

        # Выбор id блока
        if y > int(point_hight):
            if int(y) == int(point_hight):
                return 6
            if y - 6 <= point_hight:
                return biom[2]

            else:
                # Генерация руд (random может быть заменён на шум Перлина для оптимизации)
                random.seed(seed + x + y + seed - point_hight + biom[0] - biom[1] * x * y * x ** 2)
                rand = random.randint(0, 20000)
                to_id = 1
                # Угольная руда
                if rand < 250:
                    to_id = 4
                # Железная руда
                if rand < 40 and point_hight + 20 < y:
                    to_id = 9
                # Алмазы
                if rand < 5 and point_hight + 100 < y:
                    to_id = 6
                return to_id
        else:
            # уровень моря
            if int(y) >= 251:
                return 11

                # Генерация деревьев (ВСЁ ЗАНОВО!)
        region = int(x / 10) * 10
        reg_hight, reg_biom = get_hight(region + 5, 0)
        reg_hight += 1
        if reg_biom[3] != 1000 and y >= int(reg_hight) - 10:
            # Есть ли в данном квадрате дерево
            random.seed(reg_hight)
            randed = random.randint(0, reg_biom[3])
            if randed == 0:
                TREE = random.choice(TREES)  # Рандомное дерево из кортежа
                tree_file = open(TREE, 'r')
                tree_data = tree_file.readlines()
                # Получение блока из структуры дерева.
                xpos = int(x - region)
                ypos = int(reg_hight - y)
                if xpos >= 0 and ypos >= 0:
                    try:
                        data = tree_data[10 - ypos]
                        data = data.split(".")
                        return int(data[xpos])
                    except IndexError:
                        pass

    return 0

