# -*- coding: utf-8 -*-
#Zendes 2.5 WORLD GENERATION 2.8

#Генератор мира для игры Zendes 2.5


#import noise # Шум Перлина (пока не используется в этом генераторе)
import random
import sys

PATH = sys.path[0][:-4]

bs = 45 # размер блока
bsInv = 1.0/float(bs)

gs = 20 #GenerationSise
#ogs = int(gs*bsInv) #GenerationSise in blocks

#Biom configs
PlainsB = (235, 230, 3, 50, 100, 0) # world_down, world_up, up_blocks, Trees, chance, biom_id
DesertB = (225, 220, 5, 0, 60, 1)
MountainsB = (220, 200, 19, 90, 70, 2)
ForestB = (250, 230, 3, 4, 100, 3)
SeaB = (268, 264, 5, 0, 50, 4)

BIOMS0 = [PlainsB, DesertB, MountainsB, ForestB, SeaB]
BIOMS = []

# Деревья
TreeS = (PATH+"/resourses/structures/tree.txt", 55) # путь к файлу со структурой, шанс генерации (колличество повторов в списке структур)


TREES0 = [TreeS]
TREES = []

# Генерация списка с биомами с колличеством их копий которое указано в chance в кортеже биома
for BIOM in BIOMS0:
	maked = 0
	to_make = BIOM[4]
	while maked < to_make:
		maked += 1
		BIOMS.append(BIOM)

for TREE in TREES0:
	maked = 0
	to_make = TREE[1]
	while maked < to_make:
		maked += 1
		TREES.append(TREE[:-1])



# Главная функция - генератор мира
def generation(seed, mode, x, y, flatdata=10):
	x = int(x/bs)
	y = int(y/bs)
	# seed - interger или float ключ генерации (любое число) может быть отрицательным
	# mode - string режим генерации (в файле сечас только "optim#normal")
	# x, y - int кoординаты блока
	# flatdata - interger больше не используется (высота в режиме плоского мира)


	# основной режим генерации
	if mode == "optim#normal":
		point_hight = None
		

		# определение левой и правой точек и их биомов
		left_point = int(x/gs)*gs
		random.seed(seed)
		random.seed(int((left_point*100.0)/gs/random.randint(20, 100)))
		left_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		right_point = (int(x/gs)*gs)+gs
		random.seed(seed)
		random.seed(int((right_point*100.0)/gs/random.randint(20, 100)))
		right_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		# Если координаты нулевые то по-умолчанию ставится биом Plains - равнина
		# (биом под персонажем в начале)
		if int(left_point*bsInv) == 0:
			left_biom = PlainsB

		if int(right_point*bsInv) == 0:
			right_biom = PlainsB

		#определение высот 2-х основных точек, левой и правой
		random.seed(seed*left_point*gs)
		left_point_H = int(random.randint(left_biom[1], left_biom[0]))
		random.seed(seed*right_point*gs)
		right_point_H = int(random.randint(right_biom[1], right_biom[0]))
		biom = PlainsB

		#если блок совподает с левой точкой
		if int(left_point) == int(x):
			point_hight = left_point_H
			biom = left_biom

		#если блок совподает с правой точкой
		if int(right_point) == int(x):
			point_hight = right_point_H
			biom = right_biom


		if point_hight is None: #Если высота блока ещё не определена:
			rsn = 0

			#Определения влияния точек на блок
			left_percent = float(float(x-left_point)/gs)
			right_percent = float(float(right_point-x)/gs)

			# Влияние высоты точек на высоту блока
			lpercented = left_point_H*right_percent
			rpercented = right_point_H*left_percent

			#Определение высоты блока
			point_hight = (left_point_H*right_percent)+(right_point_H*left_percent)

			#Определение биома для блока
			random.seed(seed+x+y+point_hight)
			if random.randint(-(int(left_point_H*left_percent*100)), int(right_point_H*right_percent*100)) >= 0:
				biom = left_biom
			else:
				biom = right_biom

		# Выбор id блока
		if y > int(point_hight):
			if int(y) == int(point_hight):
				return 6
			if y - 6 <= point_hight:
				return biom[2]
			else:
				#Генерация руд (random может быть заменён на шум Перлина для оптимизации)
				random.seed(seed+x+y+seed-point_hight+biom[0]-biom[1]*x*y*x**2)
				rand = random.randint(0,20000)
				to_id = 1
				# Угольная руда
				if rand < 250:
					to_id = 4
				# Железная руда
				if rand < 40 and point_hight+20 < y:
					to_id = 9
				# Алмазы
				if rand < 5 and point_hight+100 < y:
					to_id = 6
				return to_id
		else:
			# уровень моря
			if int(y) >= 251:
				return 11

		# Генерация деревьев
		region = int(x/10)+int(y/10)

		return 0
