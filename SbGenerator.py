# -*- coding: utf-8 -*-
#Zendes 2.5 WORLD GENERATION 2.8

#Генератор мира для игры Zendes 2.5


#import noise # Шум Перлина (пока не используется в этом генераторе)
import random

bs = 45 # размер блока
bsInv = 1.0/float(bs)

gs = 15*bs #GenerationSise
ogs = int(gs*bsInv) #GenerationSise in blocks

#Biom configs
PlainsB = (235*bs, 230*bs, 3, 50, 100) # world_down, world_up, up_blocks, Trees, chance
DesertB = (225*bs, 220*bs, 5, 0, 60)
MountainsB = (210*bs, 200*bs, 18, 90, 70)
ForestB = (250*bs, 230*bs, 3, 4, 100)
SeaB = (268*bs, 264*bs, 5, 0, 50)

BIOMS0 = [PlainsB, DesertB, MountainsB, ForestB, SeaB]
BIOMS = []

# Генерация списка с биомами с колличеством их копий которое указано в chance в кортеже биома
for BIOM in BIOMS0:
	maked = 0
	to_make = BIOM[4]
	while maked < to_make:
		maked += 1
		BIOMS.append(BIOM)



# Главная функция - генератор мира
def generation(seed, mode, x, y, flatdata=10):
	# seed - interger или float ключ генерации (любое число) может быть отрицательным
	# mode - string режим генерации (в файле сечас только "optim#normal")
	# x, y - int кoординаты блока
	# flatdata - interger больше не используется (высота в режиме плоского мира)


	# основной режим генерации
	if mode == "optim#normal":
		lh_DIVggs = 1.0/float(gs)
		point_hight = None
		

		# определение левой и правой точек и их биомов
		left_point = int(x*lh_DIVggs)*gs
		random.seed(seed)
		random.seed(int((left_point*100.0)*bsInv*lh_DIVggs/random.randint(4, 30)))
		left_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		right_point = (int(x*lh_DIVggs)*gs)+gs
		random.seed(seed)
		random.seed(int((right_point*100.0)*bsInv*lh_DIVggs/random.randint(4, 30)))
		right_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		# Если координаты нулевые то по-умолчанию ставится биом Plains - равнина
		# (биом под персонажем в начале)
		if int(left_point*bsInv*bsInv) == 0:
			left_biom = PlainsB

		if int(right_point*bsInv*bsInv) == 0:
			right_biom = PlainsB

		#определение высот 2-х основных точек, левой и правой
		random.seed(seed*left_point*gs)
		left_point_H = int(random.randint(left_biom[1], left_biom[0])*bsInv)*bs
		random.seed(seed*right_point*gs)
		right_point_H = int(random.randint(right_biom[1], right_biom[0])*bsInv)*bs
		biom = PlainsB

		#если блок совподает с левой точкой
		if int(left_point*bsInv)*bs == int(x*bsInv)*bs:
			point_hight = left_point_H
			biom = left_biom

		#если блок совподает с правой точкой
		if int(right_point*bsInv)*bs == int(x*bsInv)*bs:
			point_hight = right_point_H
			biom = right_biom


		if point_hight is None: #Если высота блока ещё не определена:
			rsn = 0

			#Определения влияния точек на блок
			left_percent = float(x-left_point)*lh_DIVggs
			right_percent = float(right_point-x)*lh_DIVggs

			# Влияние высоты точек на высоту блока
			lpercented = left_point_H*right_percent
			rpercented = right_point_H*left_percent

			#Определение высоты блока
			point_hight = lpercented+rpercented

			#Определение биома для блока
			random.seed(seed+x+y+point_hight)
			if random.randint(-(int(rpercented*100)), int(lpercented*100)) >= 0:
				biom = left_biom
			else:
				biom = right_biom

		# Выбор id блока
		if y > point_hight:
			if int(y*bsInv) == int(point_hight*bsInv):
				return 6
			if y - 6*bs <= point_hight:
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
				if rand < 40 and point_hight+(20*bs) < y:
					to_id = 9
				# Алмазы
				if rand < 5 and point_hight+(100*bs) < y:
					to_id = 6
				return to_id
		else:
			# уровень моря
			if int(y*bsInv) >= 251:
				return 11
		return 0
