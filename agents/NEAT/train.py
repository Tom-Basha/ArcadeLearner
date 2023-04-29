import os
import pickle
import shutil
import socket
import subprocess
import numpy as np
import pygame
import neat
import time


def set_fitness(genome, score, duration):
    genome.fitness += score + duration


class Trainer:
    def __init__(self, game_name, game_path, inputs, outputs, threshold=100, population=50):
        self.config_path = "..\\agents\\NEAT\\config.txt"
        self.game_h = None
        self.game_w = None
        self.population = population
        self.threshold = threshold
        self.game_name = game_name
        self.game_path = game_path
        self.inputs = inputs
        self.outputs = list(outputs)
        self.socket = None
        self.player_frame = [0, 0, 0, 0]

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

        game_w = 1280
        game_h = 720

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
                    elif s[0] == 'score':
                        score = float(s[1])
                    elif s[0] in ['rect.x', 'rect.y', 'rect.w', 'rect.h']:
                        self.set_player_frame(s)
                    else:
                        input_arr = np.append(input_arr, float(s[1]))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True

                move = self.action(net, input_arr, genome)
                client_socket.sendall(pickle.dumps(move))

                self.frame_penalty(game_w, game_h, genome)
            else:
                duration = time.time() - start_time
                break

        set_fitness(genome, score, duration)
        print(genome.key, ")\t Fitness: ", round(genome.fitness, 3),
              "\t|\t Duration: ", round(duration, 3), "\t|\t Score: ", score)

        return False

    def set_player_frame(self, s):
        name, value = s[0], eval(s[1])
        if name == 'rect.x':
            self.player_frame[0] = value
            return
        elif name == 'rect.y':
            self.player_frame[1] = value
            return
        elif name == 'rect.w':
            self.player_frame[2] = self.player_frame[0] + value
            return
        elif name == 'rect.h':
            self.player_frame[3] = self.player_frame[1] + value
            return

    def action(self, net, values, genome):
        output = net.activate(values)
        decision = output.index(max(output))
        if decision == 0:
            genome.fitness -= 0.01
            return 0
        else:
            decision -= 1
            return self.outputs[decision]

    def frame_penalty(self, w, h, genome):
        if self.player_frame[0] == 0:
            genome.fitness -= 0.01
        if self.player_frame[1] == 0:
            genome.fitness -= 0.01
        if self.player_frame[2] == w:
            genome.fitness -= 0.01
        if self.player_frame[3] == h:
            genome.fitness -= 0.01

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

        cps_path = "..\\agents\\NEAT\\cps\\" + self.game_name
        if not os.path.exists(cps_path):
            try:
                os.mkdir(cps_path)
            except OSError as error:
                print("Directory creation failed: ", error)

        cp_prefix = cps_path + "\\train_checkpoint_"
        checkpointer = neat.Checkpointer(generation_interval=1, filename_prefix=cp_prefix)

        p.add_reporter(stats)
        p.add_reporter(checkpointer)

        winner = p.run(self.genomes_eval, self.population)
        with open(cps_path + "\\trained_ai", "wb") as f:
            pickle.dump(winner, f)

        # Copy config with train setting
        destination_file = os.path.join(cps_path, 'config.txt')
        os.makedirs(cps_path, exist_ok=True)
        shutil.copy(self.config_path, destination_file)

    def neat_setup(self):
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             self.config_path)

        config.fitness_threshold = self.threshold
        config.pop_size = self.population
        config.num_inputs = len(self.inputs)  # Attributes
        config.num_outputs = len(self.outputs)  # Keys

        self.run_neat(config)
        return
