

# importing modules
import pygame as pg
import random
# importing files
from sprites import *
from settings import *

pg.init()
background = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")

class Game():
    def __init__(self):
        self.running = True

game = Game()
while game.running:
    pass