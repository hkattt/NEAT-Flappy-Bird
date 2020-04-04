# SPRITE CLASSES

# import modules
import pygame as pg
import random
# import files
from settings import * 

# sprite images
BIRD_IMGS = [pg.image.load("bird1.png"), pg.image.load("bird2.png"), pg.image.load("bird3.png")]
PIPE_IMG = pg.image.load("pipe.png")
BASE_IMG = pg.image.load("base.png")
BG_IMG = pg.image.load("bg.png")

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

    def update(self):
        #self.move()
        self.animation()

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
        if displacement >= 10:
            displacement = 10

        if displacement < 0:
            displacement = -2
        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < MAX_ROTATION:
                self.tilt = MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= ROTATION_VEL

    def animation(self):
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

class Pipe(pg.sprite.Sprite):
    def __init__(self, x, game):
        self.groups = game.all_sprites, game.pipes # pipe groups
        # initiates sprite class
        pg.sprite.Sprite.__init__(self, self.groups)
        # copy of the game
        self.game = game
        # x coordinate
        self.x = x
        self.height = 0
        self.gap = 100
        # keep track of each pipes position
        self.top = 0
        self.bottom = 0
        # top pipe (the image needs to be flipped horiontally)
        self.pipe_top = pg.transform.flip(PIPE_IMG, False, True)
        # bottom pipe
        self.pipe_bottom = PIPE_IMG
        self.passed = False
        self.set_height()

    def update(self):
        self.move()
        # checks for a collision
        if self.collisions():
            pass
        # removes the pipe if it is off the display
        if self.x + PIPE_IMG.get_width() < 0:
            self.game.all_sprites.remove(self)
            self.game.pipes.remove(self)
        # if the bird passed the pipe a new pipe is created
        if not self.passed and self.x < self.game.bird.x:
            self.game.score += 1
            self.game.pipe = Pipe(400, self.game)
            self.passed = True

    def set_height(self):
        self.height = random.randrange(50, 260)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= PIPE_VEL

    def collisions(self):
        # pipe masks
        top_mask = pg.mask.from_surface(self.pipe_top)
        bottom_mask = pg.mask.from_surface(self.pipe_bottom)

        # offset between the masks
        top_offset = (self.x - round(self.game.bird.x), self.top - round(self.game.bird.y))
        bottom_offset = (self.x - round(self.game.bird.x), self.bottom - round(self.game.bird.y))

        # calculates the point of collision
        point_of_collision_t = self.game.bird.mask.overlap(top_mask, top_offset)
        point_of_collision_b = self.game.bird.mask.overlap(bottom_mask, bottom_offset)

        # checks if there was a collision between either mask
        if point_of_collision_t or point_of_collision_b:
            return True
        return False

class Base(pg.sprite.Sprite):
    def __init__(self, y, game):
        self.groups = game.all_sprites # sprite groups
        # initiates sprite class
        pg.sprite.Sprite.__init__(self, self.groups)
        # copy of the game
        self.game = game
        self.width = BASE_IMG.get_width()
        # x, y coordinates
        self.x1 = 0
        self.x2 = self.width
        self.y = y
        self.img = BASE_IMG

    def update(self):
        self.move()
        if self.collisions():
            self.game.playing = False
            self.game.running = False

    def move(self):
        self.x1 -= BASE_VEL
        self.x2 -= BASE_VEL

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def collisions(self):
        if self.game.bird.y + self.game.bird.img.get_height() > self.y:
            return True

    