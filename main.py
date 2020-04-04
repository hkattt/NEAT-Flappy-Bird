

# importing modules
import pygame as pg
import random
import os
import neat
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
        self.score = 0
        self.score_font = pg.font.SysFont("comicsans", 30)

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.birds = pg.sprite.Group()
        self.pipes = pg.sprite.Group()
        
        self.nets = []
        self.ge = []
        self.BIRDS = []

        # creates objects
        self.bird = Bird(WIDTH / 2, HEIGHT / 2, self)
        self.base = Base(400, self)
        self.pipe = Pipe(400, self)
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
        # background image
        background.blit(BG_IMG, (0, 0))
        # pipes
        for pipe in self.pipes:
            background.blit(pipe.pipe_top, (pipe.x, pipe.top))
            background.blit(pipe.pipe_bottom, (pipe.x, pipe.bottom))
        # base
        background.blit(self.base.img, (self.base.x1, self.base.y))
        background.blit(self.base.img, (self.base.x2, self.base.y))
        # bird
        for sprite in self.birds:
            self.background.blit(sprite.rotated_img, sprite.new_rect)
         # score
        text = self.score_font.render("Score: " + str(self.score), 1, WHITE)
        background.blit(text, (WIDTH - 10 - text.get_width(), 10))
        pg.display.update()

game = Game()
while game.running:
    game.new()
pg.quit()
quit()

