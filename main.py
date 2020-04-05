

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
        pg.init()
        self.background = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Flappy Bird")
        self.clock = pg.time.Clock()
        self.score = 0
        self.generation = 0
        self.font = pg.font.SysFont("comicsans", 30)

    def new(self, genomes, config):
        self.generation += 1
        self.reset()
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.birds = pg.sprite.Group()
        self.pipes = pg.sprite.Group()

        # start by creating lists holding the genome itself and the
        # neural network associated with the genome
        self.nets = []
        self.bird_indices = [] # allows us to keep track of what bird coresponds to which genome and neural network
        self.ge = []

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.bird_indices.append(Bird(WIDTH / 2, HEIGHT / 2, self))
            self.ge.append(genome)

        # creates objects
        self.base = Base(400, self)
        self.pipe = Pipe(400, self)
        self.run()

    def run(self):
        self.playing = True
        while self.playing and len(self.bird_indices) > 0:
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
        score = self.font.render("Score: " + str(self.score), 1, WHITE)
        background.blit(score, (WIDTH - 10 - score.get_width(), 10))
        # generation
        generation = self.font.render("Generation: " + str(self.generation), 1, WHITE)
        background.blit(generation, (10, 10))
        pg.display.update()

    def reset(self):
        self.score = 0

game = Game()


def run(config_file):
    """ runs the NEAT algorithm to train a neural network to play flappy bird """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    population = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    # Run for up to 50 generations.
    winner = population.run(game.new, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

