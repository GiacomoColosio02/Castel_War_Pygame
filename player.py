from constants import *

class Player:
    def __init__(self):
        self.units = [0, 0, 0]  # the first one is the worker, 
                                # the second on is the swordsman
                                # and the third one is the archer
        self.resources = INIT_RESOURCES
        self.wall = WALL_HEALTH