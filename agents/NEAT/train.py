import pickle
import pygame
import neat
import os
import time



def train_ai(self, genome, config):
    stuck = False
    run = True
    start_time = time.time()

    net = neat.nn.FeedForwardNetwork.create(genome, config)
    self.genome = genome

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True

        stuck = self.ball.last_break()
        if stuck == True:
            genome.fitness -= 20

        dt = self.game.clock.tick(self.game.fps)
        self.game.event_loop()
        self.game.update(dt)
        self.game.draw()

        pygame.display.update()

        self.move_player(net)

        pygame.display.update()

        duration = time.time() - start_time

        if self.game.state_name == "GAMEOVER":
            self.calculate_fitness(self.player.score, duration)
            print(genome.key, ")\t Fitness: ", round(genome.fitness, 3),
                  "\t|\t Duration: ", round(duration, 3), "\t|\t Score: ", self.player.score)
            break

    return False


def genomes_eval(selected_game, genomes, config):
    window = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        game = selected_game
        game.train_ai(genome, config)
        game.game.state.reset_game()
        game.game.update(game.game.clock.tick(0))


def run_neat(config, selected_game):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(genomes_eval(selected_game), p)
    with open("cps/best.pickle", "wb") as f:
        pickle.dump(winner, f)


def neat_setup(selected_game, inputs, outputs, threshold=250, population=50):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         "config.txt")

    config.fitness_threshold = threshold
    config.pop_size = population
    config.num_inputs = inputs  # Attributes
    config.num_outputs = outputs  # Keys

    run_neat(config, selected_game)
    return
