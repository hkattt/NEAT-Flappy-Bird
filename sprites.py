# SPRITE CLASSES

# import modules
import pygame as pg

# sprite images
BIRD_IMGS = [pg.transform.scale2x(pg.image.load("bird1.png")), pg.transform.scale2x(pg.image.load("bird2.png")), pg.transform.scale2x(pg.image.load("bird3.png"))]
PIPE_IMG = pg.transform.scale2x(pg.image.load("pipe.png"))
BASE_IMG = pg.transform.scale2x(pg.image.load("base.png"))
BG_IMG = pg.transform.scale2x(pg.image.load("bg.png"))

class Bird(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        self.groups = game.all_sprites, game.birds # bird groups
        # initiates sprite class
        pg.sprite.Sprite.__init__(self, self.groups)
        # copy of the game
        self.game
        # x, y cooridnates
        self.x = x
        self.y = y
        # tilt of the image
        self.tilt = 0
        self.tick_count = 0
        # keep track of animation
        self.img_count = 0
        self.vel = 0
        self.img = BIRD_IMGS[0]
        self.rect = self.img.get_rect()

    def jump(self):
        """ Makes the bird perfrom a jump """
        self.vel = -10.5
        
        