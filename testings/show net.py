import pickle
import neat

from testings import visualize
from testings import viz

player = f"..\\agents\\NEAT\\games\\Pong\\unfinished_best_genome"
config_path = f"..\\agents\\NEAT\\games\\Pong\\config.txt"
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

with open(player, "rb") as f:
    winner = pickle.load(f)

visualize.draw_net(config, winner, game="Pong")
# viz.draw_net(config, winner)
# visualize.draw_net(config, winner, prune_unused=True)


initial_genome = neat.DefaultGenome(config.genome_config)

# Visualize the graph of the initial genome
visualize.draw_net(config, initial_genome, view=True)
