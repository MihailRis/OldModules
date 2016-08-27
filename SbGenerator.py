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
PlainsB = (235, 230, 3, 10, 100, 0) # world_down, world_up, up_blocks, Trees, chance, biom_id
DesertB = (250, 240, 5, 1000, 60, 1)
MountainsB = (220, 200, 19, 20, 70, 2)
ForestB = (250, 230, 3, 1, 100, 3)
SeaB = (268, 264, 5, 0, 50, 4)

BIOMS0 = [PlainsB, DesertB, MountainsB, ForestB]
BIOMS = []

# Деревья
TreeS = (PATH+"/resourses/structures/tree.txt", 25) # путь к файлу со структурой, шанс генерации (колличество повторов в списке структур)
Tree2S = (PATH+"/resourses/structures/tree2.txt", 25)
WheatS = (PATH+"/resourses/structures/wheat.txt", 10)


TREES0 = [TreeS, WheatS, Tree2S]
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
		def get_hight(x, y):
			point_hight = None
		

			# определение левой и правой точек и их биомов
			left_point = int(x/gs)*gs
			random.seed(seed)
			random.seed(int((left_point*100.0)/gs/random.randint(10*gs, 30*gs)))
			left_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

			right_point = (int(x/gs)*gs)+gs
			random.seed(seed)
			random.seed(int((right_point*100.0)/gs/random.randint(10*gs, 30*gs)))
			right_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

			# Если координаты нулевые то по-умолчанию ставится биом Plains - равнина
			# (биом под персонажем в начале)
			if int(left_point*bsInv) == 0:
				left_biom = ForestB

			if int(right_point*bsInv) == 0:
				right_biom = ForestB

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
				if left_biom[-1] != right_biom[-1]:
					random.seed(seed+x+y+point_hight)
					if random.randint(-(int(left_point_H*left_percent*100)), int(right_point_H*right_percent*100)) >= 0:
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

		# Генерация деревьев (ВСЁ ЗАНОВО!)
		region = int(x/10)*10
		reg_hight, reg_biom = get_hight(region+5, 0)
		reg_hight += 1
		if reg_biom[3] != 1000 and y >= int(reg_hight)-10:
			# Есть ли в данном квадрате дерево
			random.seed(reg_hight)
			randed = random.randint(0, reg_biom[3])

			if randed == 0:
				TREE = TREES[random.randint(0, len(TREES)-1)]
				tree_file = open(TREE[0], 'r')
				tree_data = tree_file.readlines()
				# Получение блока из структуры дерева.
				xpos = int(x-region)
				ypos = int(reg_hight-y)
				if xpos >= 0 and ypos >= 0:
					try:
						data = tree_data[10-int(ypos)]
						data = data.split(".")
						return int(data[int(xpos)])
					except IndexError:
						pass

	return 0
