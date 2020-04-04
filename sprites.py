# SPRITE CLASSES

# import modules
import pygame as pg
# import files
from settings import * 

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
        self.game = game
        # x, y cooridnates
        self.x = x
        self.y = y
        # tilt of the image
        self.tilt = 0
        # keeps track of when the bird last jumped
        self.tick_count = 0
        # keeps track of birds movement
        self.height = self.y
        # keep track of animation
        self.img_count = 0
        self.vel = 0
        self.img = BIRD_IMGS[0]
        self.rect = self.img.get_rect()

    def jump(self):
        """ Makes the bird perfrom a jump """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        # one frame went by
        self.tick_count += 1
        # equation of motion
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2
        # terminal velocity
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement = -2
        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < MAX_ROTATION:
                self.tilt = MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= ROTATION_VEL

    def draw(self):
        self.img_count += 1

        # bird animation
        if self.img_count < ANIMATION_TIME:
            self.img = BIRD_IMGS[0]
        elif self.img_count < ANIMATION_TIME * 2:
            self.img = BIRD_IMGS[1]
        elif self.img_count < ANIMATION_TIME * 3:
            self.img = BIRD_IMGS[2]
        elif self.img_count < ANIMATION_TIME * 4:
            self.img = BIRD_IMGS[1]
        elif self.img_count == ANIMATION_TIME * 4 + 1:
            self.img = BIRD_IMGS[0]
            self.img_count = 0
        
        # the bird should not flap when it is free-falling
        if self.tilt <= -80:
            self.img = BIRD_IMGS[0]
            self.img_count = ANIMATION_TIME * 2

        # rotates the bird
        self.rotated_img = pg.transform.rotate(self.img, self.tilt)
        # rotates it around the centre
        self.new_rect = self.rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        # Creates an image mask for collisions
        self.mask = pg.mask.from_surface(self.img)

    def update(self):
        self.move()
        self.draw()

        