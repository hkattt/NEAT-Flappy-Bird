

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
        pg.init()
        self.background = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Flappy Bird")

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.group()
        self.birds = pg.sprite.group()
        # creates objects
        self.bird = Bird(WIDTH / 2, HEIGHT / 2, self)
        self.run()

    def run(self):
        playing = True
        while playing:
            self.paint()
    
    def paint(self):
        for sprite in self.birds:
            self.background.blit(sprite.rotated_img, sprite.new_rect)

game = Game()
while game.running:
    game.new()