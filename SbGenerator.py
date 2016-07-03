# -*- coding: utf-8 -*-
#WORLD GENERATION

# seeds 707
import random
from SbDev import sb_output
from SbDev import divis_get
import math

bs = 45
wdm = 45*bs*0
wum = 30*bs*0

gs = 15*bs #GenerationSise
ogs = int(gs/bs) #GenerationSise in blocks

PlainsB = (65*bs+wdm, 60*bs+wum, 3, 50, 100) # world_down, world_up, up_blocks, Trees, chance
DesertB = (55*bs+wdm, 50*bs+wum, 5, 0, 60)
MountainsB = (40*bs+wdm, 30*bs+wum, 1, 90, 200)
ForestB = (80*bs+wdm, 60*bs+wum, 3, 4, 100)
SeaB = (60*bs+wdm, 60*bs+wum, 6, 0, 500)

BIOMS0 = [PlainsB, DesertB, MountainsB, ForestB]
BIOMS = []
for BIOM in BIOMS0:
	maked = 0
	to_make = BIOM[4]
	while maked < to_make:
		maked += 1
		BIOMS.append(BIOM)



def generation(seed, mode, x, y, flatdata=10):
	if mode == "flat":
		if y/bs - 6 >= flatdata:
			a = random.randint(0,1000)
			z = False
			if a < 35 and a > 20:
				return 4
				z = True
			if not z and a < 20 and a > 10 and y/bs > flatdata+10:
				return 9
				z = True
			if not z:
				return 1
		if y/bs - 2 >= flatdata:
			return 2
		if y/bs - 1 >= flatdata:
			return 3
		if y/bs - 4 < flatdata:
			return 0
	if mode == "empty":
		return 0

	if mode == "interstellar":
		r = seed*x*y
		if divis_get(r, 2):
			return(0)
		else:
			return(1)

	if mode == "normal":

		left_point = int(x/gs)*gs
		random.seed(seed)
		random.seed(int((left_point*100.0)/bs/gs/random.randint(10, 30)))
		left_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		right_point = (int(x/gs)*gs)+gs
		random.seed(seed)
		random.seed(int((right_point*100.0)/bs/gs/random.randint(10, 30)))
		right_biom = BIOMS[random.randint(0, len(BIOMS)-1)]

		#определение высот 2-х основных точек, левой и правой
		random.seed(seed*left_point*gs)
		left_point_H = int(random.randint(left_biom[1], left_biom[0])/bs)*bs
		random.seed(seed*right_point*gs)
		right_point_H = int(random.randint(right_biom[1], right_biom[0])/bs)*bs
		biom = PlainsB
		#если блок совподает с левой точкой
		if int(left_point/bs)*bs == int(x/bs)*bs:
			point_hight = left_point_H
			biom = left_biom
		#если блок совподает с правой точкой
		if int(right_point/bs)*bs == int(x/bs)*bs:
			point_hight = right_point_H
			biom = right_biom
		left_percent = float(float(x-left_point)/gs)
		right_percent = float(float(right_point-x)/gs)
		try:
			point_hight
		except NameError:
			rsn = 0
			point_hight = (left_point_H*right_percent)+(right_point_H*left_percent)

			random.seed(seed+x+y+point_hight)
			if random.randint(-(int(left_point_H*left_percent*100)), int(right_point_H*right_percent*100)) >= 0:
				biom = left_biom
			else:
				biom = right_biom

		if y > point_hight:
			if int(y/bs) == int(point_hight/bs):
				return 6
			if y - 6*bs <= point_hight:
				return biom[2]
			else:
				random.seed(seed+x+y+seed-point_hight+biom[0]-biom[1]*x*y*x**2)
				rand = random.randint(0,20000)
				to_id = 1
				if rand < 250:
					to_id = 4
				if rand < 40 and point_hight+(20*bs) < y:
					to_id = 9
				if rand < 5 and point_hight+(100*bs) < y:
					to_id = 6
				return to_id
		else:
			random.seed(seed+x)
			if biom[3] != 0:
				done_1 = False
				if random.randint(0, biom[3]) == 0:
					if int(y/bs) == int(point_hight/bs):
						return 7
						done_1 = True
					if int(y/bs)+1 == int(point_hight/bs):
						return 7
						done_1 = True
					if int(y/bs)+2 == int(point_hight/bs):
						return 7
						done_1 = True
					if int(y/bs)+3 == int(point_hight/bs):
						return 7
						done_1 = True
					if int(y/bs)+4 == int(point_hight/bs):
						return 7
						done_1 = True
					if int(y/bs)+5 == int(point_hight/bs):
						return 8
					if int(y/bs)+6 == int(point_hight/bs):
						return 8
						done_1 = True

				random.seed(seed+x+bs)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y/bs)+1 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+2 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+3 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+4 == int(point_hight/bs):
						return 8
						done_1 = True
				random.seed(seed+x-bs)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y/bs)+1 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+2 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+3 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+4 == int(point_hight/bs):
						return 8
						done_1 = True
				random.seed(seed+x+bs*2)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y/bs)+2 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+3 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+4 == int(point_hight/bs):
						return 8
						done_1 = True
				random.seed(seed+x-bs*2)
				if not done_1 and random.randint(0, biom[3]) == 0:
					if int(y/bs)+2 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+3 == int(point_hight/bs):
						return 8
						done_1 = True
					if int(y/bs)+4 == int(point_hight/bs):
						return 8
						done_1 = True

				if not done_1:
					return 0
			else:
				return 0
#		x_left_rasn = float(ogs/(x-left_point+0.1))
