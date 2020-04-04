

# importing modules
import pygame as pg
import random
# importing files
from sprites import *
from settings import *

pg.init()
background = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flappy Bird")