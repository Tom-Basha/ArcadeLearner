import os
import pickle
import socket
import subprocess
import numpy as np
import pygame
import neat
import time


def set_fitness(genome, score, duration):
    genome.fitness += score + duration


class Trainer:
    def __init__(self, game_name, game_path, inputs, outputs, threshold=250, population=10):
        self.population = population
        self.threshold = threshold
        self.game_name = game_name
        self.game_path = game_path
        self.inputs = inputs
        self.outputs = list(outputs)
        self.socket = None

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        subprocess.Popen(["python", self.game_path], shell=True)

        # print("Waiting for a client to connect...")
        client_socket, addr = self.socket.accept()

        # Send the serialized data to the client after the connection is established
        # print("Client connected. Sending data...")
        client_socket.sendall(pickle.dumps(self.inputs))
        # print("Data sent.")

        score = 0
        start_time = time.time()
        while True:
            data = client_socket.recv(4096)
            if data:
                data = pickle.loads(data)
                input_arr = np.array([])
                for s in data:
                    value = s[1]
                    if '(' in s[1]:
                        arr = np.array(eval(value))
                        input_arr = np.concatenate((input_arr, arr.flatten()))

                    else:
                        if s[0] == 'score':
                            score = float(s[1])
                        input_arr = np.append(input_arr, float(s[1]))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True

                move = self.action(net, input_arr)
                client_socket.sendall(pickle.dumps(move))

            else:
                duration = time.time() - start_time
                break

        set_fitness(genome, score, duration)
        print(genome.key, ")\t Fitness: ", round(genome.fitness, 3),
              "\t|\t Duration: ", round(duration, 3), "\t|\t Score: ", score)

        return False

    def action(self, net, values):
        output = net.activate(values)
        decision = output.index(max(output))
        if decision == 0:
            return 0
        else:
            decision -= 1
            return self.outputs[decision]

    def genomes_eval(self, genomes, config):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        # Listen for incoming connections
        self.socket.listen()

        print(f"Requested attributes: {self.inputs}")

        for i, (genome_id, genome) in enumerate(genomes):
            genome.fitness = 0
            self.train_ai(genome, config)

        self.socket.close()

    def run_neat(self, config):
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()

        dir_path = "..\\agents\\NEAT\\cps\\" + self.game_name
        if not os.path.exists(dir_path):
            try:
                os.mkdir(dir_path)
            except OSError as error:
                print("Directory creation failed: ", error)

        cp_prefix = dir_path + "\\train_checkpoint_"
        checkpointer = neat.Checkpointer(generation_interval=1, filename_prefix=cp_prefix)

        p.add_reporter(stats)
        p.add_reporter(checkpointer)

        winner = p.run(self.genomes_eval, self.population)
        with open(dir_path + "\\best.pickle", "wb") as f:
            pickle.dump(winner, f)

    def neat_setup(self):
        config_path = "..\\agents\\NEAT\\config.txt"
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_path)

        config.fitness_threshold = self.threshold
        config.pop_size = self.population
        config.num_inputs = len(self.inputs)  # Attributes
        config.num_outputs = len(self.outputs)  # Keys

        self.run_neat(config)
        return
