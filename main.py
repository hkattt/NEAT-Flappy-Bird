

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
        self.clock = pg.time.Clock()

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.birds = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        # creates objects
        self.bird = Bird(WIDTH / 2, HEIGHT / 2, self)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.paint()

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running= False
                
    
    def paint(self):
        background.blit(BG_IMG, (0, 0))
        for sprite in self.birds:
            self.background.blit(sprite.rotated_img, sprite.new_rect)
        pg.display.update()

game = Game()
while game.running:
    game.new()