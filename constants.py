import pygame

#  game constants
SCREEN_HEIGHT, SCREEN_WIDTH = 250, 1000
WALL_POS = 180
WALL_WIDTH = 62
MINE_POS = 40
MINE_WIDTH = 58
BARRACKS_POS = 106
BARRACKS_WIDTH = 62
TOWER_HEIGHT = 160
GROUND_HEIGHT = 14
MINE_HEIGHT = 37
BARRACKS_HEIGHT = 50
WALL_HEIGHT = 80
INIT_RESOURCES = 100

# worker constants
WORKER_COST = 50
WORKER_TRAIN = 1
WORKER_SPEED = 0.5
WORKER_PROD = 25
WORKER_REPAIR = 1

#Swordsman constant
SWORD_COST = 75
SWORD_TRAIN = 2
SWORD_SPEED = 0.5
SWORD_RANGE = 3
SWORD_HIT = 0.3
SWORD_REST = 2 

#Archer Constant
ARCHER_COST = 100
ARCHER_TRAIN = 3
ARCHER_SPEED = 0.5
ARCHER_RANGE = 75
ARCHER_HIT = 0.8
ARROW_SPEED = 1.5
ARCHER_REST = 3

# building constants
WALL_HEALTH = 500
TOWER_RANGE = 220
TOWER_HIT = 200
TOWER_REST = 0 #Prima era 3
TOWER_SPEED = 1.75

from player import Player

# players
blue_player = Player()
red_player = Player()

# dispatch vars
workers_disp = []
swords_disp = []
archers_disp = []

# projectiles
projectiles = []

# images
backgorund_img = pygame.image.load('images/background.png')
btower_img = pygame.image.load('images/buildings/blue_tower1.png')
bbarracks_img = pygame.image.load('images/buildings/blue_barracks1.png')
bmine_img = pygame.image.load('images/buildings/blue_mine1.png')
rtower_img = pygame.image.load('images/buildings/red_tower.png')
rbarracks_img = pygame.image.load('images/buildings/red_barracks.png')
rmine_img = pygame.image.load('images/buildings/red_mine.png')
blue_wall_img = pygame.image.load('images/buildings/wall.png')
red_wall_img = pygame.image.load('images/buildings/wall.png')
res_ui_blue_img = pygame.image.load('images/resources_ui_blue.png')
res_ui_red_img = pygame.image.load('images/resources_ui_red.png')
dmd_img = pygame.image.load('images/dmd.png')
