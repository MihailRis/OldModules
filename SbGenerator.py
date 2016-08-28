# -*- coding: utf-8 -*-
# Zendes 2.5 WORLD GENERATION 2.8

# Генератор мира для игры Zendes 2.5


# import noise # Шум Перлина (пока не используется в этом генераторе)
import random
import os

# Путь к папке, в которой мы находимся
PATH = os.path.dirname(os.path.abspath(__file__))

# Путь к папке со структурами
STRUCTURES_PATH = os.path.join(PATH, "resources", "structures")

BLOCK_SKY = 0
BLOCK_STONE = 1
BLOCK_SOIL = 2
BLOCK_GRASS = 3
BLOCK_COAL = 4
BLOCK_SAND = 5
BLOCK_DIAMOND = 6
BLOCK_WOOD = 7
BLOCK_FOLIAGE = 8
BLOCK_IRON = 9
BLOCK_WATER = 11
BLOCK_WHEAT = 17
BLOCK_ROCK = 19

BLOCK_SIZE = 45
GENERATION_SIZE = 20
TREE_WIDTH = 10
TREE_HEIGHT = 10
SEA_LEVEL = 251
TOP_LAYER_DEPTH = 6
IRON_DEPTH = 20
DIAMOND_DEPTH = 100
COAL_CHANCE = 1.0 / 80
IRON_CHANCE = 1.0 / 500
DIAMOND_CHANCE = 1.0 / 4000

SEED_BIOM = 0
SEED_HEIGHT = 1
SEED_ORE = 2
SEED_TREE = 3


class Biom:
    def __init__(self, low, high, block, top_block, tree_chance):
        self.low = low
        self.high = high
        self.block = block
        self.top_block = top_block
        self.tree_chance = tree_chance

BIOM_PLAINS = Biom(16, 21, BLOCK_SOIL, BLOCK_GRASS, 1.0 / 10)
BIOM_DESERT = Biom(1, 11, BLOCK_SAND, BLOCK_SAND, 0)
BIOM_MOUNTAINS = Biom(31, 41, BLOCK_ROCK, BLOCK_ROCK, 1.0 / 20)
BIOM_FOREST = Biom(1, 21, BLOCK_SOIL, BLOCK_SOIL, 1)
BIOM_SEA = Biom(-17, -13, BLOCK_SAND, BLOCK_SAND, 0)

BIOM_DISTRIBUTION = (
    10 * [BIOM_PLAINS] +
    6 * [BIOM_DESERT] +
    7 * [BIOM_MOUNTAINS] +
    10 * [BIOM_FOREST]
)


def load_tree(name):
    path = os.path.join(STRUCTURES_PATH, name)
    f = open(path, 'r')
    data = f.readlines()
    return [map(int, row.split(".")) for row in reversed(data)]

TREE_1 = load_tree("tree.txt")
TREE_2 = load_tree("tree2.txt")
TREE_WHEAT = load_tree("wheat.txt")

TREE_DISTRIBUTION = (
    5 * [TREE_1] +
    5 * [TREE_2] +
    2 * [TREE_WHEAT]
)


def get_generation_point_height_and_biom(seed, x):
    # если координаты нулевые то по-умолчанию ставится биом леса
    # (биом под персонажем в начале)
    if x == 0:
        biom = BIOM_FOREST
    else:
        random.seed((SEED_BIOM, seed, x))
        biom = random.choice(BIOM_DISTRIBUTION)

    random.seed((SEED_HEIGHT, seed, x))
    height = random.randint(biom.low, biom.high)

    return height, biom


def get_height_and_biom(seed, x, y):
    # определение левой и правой точек генерации
    left_point = x / GENERATION_SIZE * GENERATION_SIZE
    right_point = left_point + GENERATION_SIZE

    left_height, left_biom = get_generation_point_height_and_biom(seed, left_point)
    right_height, right_biom = get_generation_point_height_and_biom(seed, right_point)

    if x == left_point:
        height = left_height
        biom = left_biom
    elif x == right_point:
        height = right_height
        biom = right_biom
    else:
        # определение влияния точек генерации на блок
        left_weight = float(right_point - x) / GENERATION_SIZE
        right_weight = 1 - left_weight

        if left_biom == right_biom:
            biom = left_biom
        else:
            random.seed((SEED_BIOM, seed, x, y))
            if random.random() < left_weight:
                biom = left_biom
            else:
                biom = right_biom

        height = int(left_height * left_weight + right_height * right_weight + 0.5)

    return height, biom


def generate_ore(seed, x, depth):
    # генерация руд (random может быть заменён на шум Перлина для оптимизации)
    random.seed((SEED_ORE, seed, x, depth))
    rand = random.random()

    if rand < DIAMOND_CHANCE and depth >= DIAMOND_DEPTH:
        return BLOCK_DIAMOND
    if rand < IRON_CHANCE and depth >= IRON_DEPTH:
        return BLOCK_IRON
    if rand < COAL_CHANCE:
        return BLOCK_COAL

    return BLOCK_STONE


def generate_tree(seed, x, y):
    left_point = x / TREE_WIDTH * TREE_WIDTH
    height, biom = get_height_and_biom(seed, left_point + 5, 0)

    row = y - height + 1
    col = x - left_point

    if biom.tree_chance > 0 and 0 <= row < TREE_HEIGHT:
        # есть ли в данном квадрате дерево
        random.seed((SEED_TREE, seed, left_point))
        if random.random() < biom.tree_chance:
            tree = random.choice(TREE_DISTRIBUTION)
            return tree[row][col]


def generate_normal(seed, x, y):
    height, biom = get_height_and_biom(seed, x, y)

    if y < height:
        depth = height - y

        if depth == 1:
            return biom.top_block
        if depth <= TOP_LAYER_DEPTH:
            return biom.block

        return generate_ore(seed, x, depth)

    block = generate_tree(seed, x, y)
    if block is not None:
        return block

    return BLOCK_WATER if y < 0 else BLOCK_SKY


# елавная функция - генератор мира
def generation(seed, mode, x, y):
    x = int(x) / BLOCK_SIZE
    y = SEA_LEVEL - int(y) / BLOCK_SIZE
    # seed - any ключ генерации
    # mode - string режим генерации (в файле сечас только "optim#normal")
    # x, y - int координаты блока

    # основной режим генерации
    if mode == "optim#normal":
        return generate_normal(seed, x, y)

    return BLOCK_SKY
