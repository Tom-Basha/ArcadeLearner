import pickle
import pygame
import neat
import os
import time
import main
from game import Game
import constants as c


class Breakout:
    def __init__(self, window):
        self.game = Game(window, main.states, "GAMEPLAY")
        self.ball = self.game.state.ball
        self.player = self.game.state.player
        self.generation = -1

    def test_ai(self, winner_net):
        fps = 0
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(fps)

            self.game.ai_loop(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            if self.game.state_name == "GAMEPLAY":
                self.trained_movement(winner_net)

            pygame.display.update()

            if self.game.state_name == "GAMEOVER":
                break

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

            if self.game.state_name == "GAMEPLAY":
                self.move_player(net)

            pygame.display.update()

            duration = time.time() - start_time

            if self.game.state_name == "GAMEOVER":
                self.calculate_fitness(self.player.score, duration)
                print(genome.key, ")\t Fitness: ", round(genome.fitness, 3),
                      "\t|\t Duration: ", round(duration, 3), "\t|\t Score: ", self.player.score)
                break

        return False

    def move_player(self, net):
        genome = self.genome
        player_x, ball_x, ball_y = self.game.state.get_positions()
        output = net.activate((player_x, abs(self.player.rect.top - ball_y), ball_x))
        decision = output.index(max(output))
        valid = True
        if decision == 0:  # Don't move
            genome.fitness -= 0.01  # we want to discourage this
            self.player.move_player(0)
        else:  # Move left(1) or right(2)
            valid = self.player.move_player(decision)
        if not valid:  # If the movement makes the paddle go off the screen punish the AI
            genome.fitness -= 0.05

    def trained_movement(self, net):
        player_x, ball_x, ball_y = self.game.state.get_positions()
        output = net.activate((player_x, abs(self.player.rect.top - ball_y), ball_x))
        decision = output.index(max(output))
        self.player.move_player(decision)

    def calculate_fitness(self, game_score, duration):
        self.genome.fitness += game_score + duration


def genomes_eval(genomes, config):
    window = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

    for i, (genome_id, genome) in enumerate(genomes):
        genome.fitness = 0
        game = Breakout(window)
        game.train_ai(genome, config)
        game.game.state.reset_game()
        game.ball.last_brick = time.time()
        game.game.update(game.game.clock.tick(0))


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(genomes_eval, 50)
    with open("../../FinalProject 1/PyBreakout/best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("../../FinalProject 1/PyBreakout/best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    window = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
    pygame.display.set_caption("Breakout")
    breakout = Breakout(window)
    breakout.test_ai(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, '../../FinalProject 1/PyBreakout/config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # run_neat(config)
    test_best_network(config)
