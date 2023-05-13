import os
import pickle
import shutil
import socket
import subprocess
import numpy as np
import neat
import time

from assets.components.button import training_btn
from assets.utils import *

pygame.init()


def set_fitness(genome, score, duration):
    genome.fitness += score + duration / 2


class Trainer:
    def __init__(self, game_name, game_path, inputs, outputs, threshold, generations, population,
                 start_gen, num_hidden):
        self.num_hidden = num_hidden
        self.generations = generations
        if start_gen != -1:
            self.config_path = f"..\\agents\\NEAT\\cps\\{game_name}\\config.txt"
        else:
            self.config_path = "..\\agents\\NEAT\\config.txt"
        self.game_h = None
        self.game_w = None
        self.start_gen = start_gen
        self.population = population
        self.threshold = threshold
        self.game_name = game_name
        self.game_path = game_path
        self.inputs = inputs
        self.outputs = list(outputs)
        self.socket = None
        self.player_frame = [0, 0, 0, 0]
        self.prev_player_frame = [0, 0, 0, 0]
        self.add_essentials()

        self.score = 0
        self.duration = 0

        self.quit_training = False
        self.pause_training = False

        self.buttons = [
            training_btn((365, 635), "Next Genome"),
            training_btn((640, 635), "Pause Training"),
            training_btn((915, 635), "Quit Training")
        ]

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption(f"{game_name} AI Train")
        self.curr_generation = start_gen + 1
        self.last_gemone = None
        self.last_gemone_obj = None

        self.total_genomes = 0
        self.last_five_genomes = []
        self.best_genome = {"Key": -1, "fitness": -1000, "time": -1, "score": -1}
        self.best_genome_obj = None
        self.info_headers = [
            (train_info("#", (265, 130))),
            (train_info("Fitness", (490, 130))),
            (train_info(f"GOAL: {self.threshold}", (490, 157), size=12)),
            (train_info("Duration", (765, 130))),
            (train_info("Score", (990, 130))),
            (train_info("Best Genome", (SCREEN_W // 2, 460)))
        ]

    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        subprocess.Popen(["python", self.game_path], shell=True)

        client_socket, addr = self.socket.accept()
        client_socket.sendall(pickle.dumps(self.inputs))

        self.score = 0
        start_time = time.time()

        game_w = 1280
        game_h = 720

        while True:
            data = client_socket.recv(4096)
            if data:
                data, input_arr = self.organize_data(data)

                self.update_buttons()
                mouse_pos = pygame.mouse.get_pos()
                if self.handle_training_events(mouse_pos, genome):
                    break

                move = self.action(net, input_arr, genome)
                client_socket.sendall(pickle.dumps(move))
                self.frame_penalty(game_w, game_h, genome)

                if genome.fitness >= self.threshold:
                    break
            else:
                break

        self.duration = round(time.time() - start_time, 3)
        if self.duration < 5 and self.score <= 10:
            genome.fitness = -20
        elif self.score <= 5:
            genome.fitness = -5
        elif self.duration < 2:
            genome.fitness = -30

        set_fitness(genome, self.score, self.duration)
        print(
            f"{genome.key}.\t\t Fitness: {round(genome.fitness, 3)}\t|\t Duration: {self.duration}\t|\t Score: {self.score}")

        self.last_gemone = {"key": genome.key, "fitness": round(genome.fitness, 3), "time": self.duration,
                            "score": self.score}
        self.last_gemone_obj = genome

        if len(self.last_five_genomes) >= 5:
            self.last_five_genomes.pop(0)
        self.last_five_genomes.append(self.last_gemone)

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
            genome.fitness -= 0.001
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

        moved = False
        for i in range(len(self.player_frame)):
            if self.player_frame[i] != self.prev_player_frame[i]:
                moved = True

        if not moved:
            genome.fitness -= 0.01

        self.prev_player_frame = self.player_frame.copy()

    def genomes_eval(self, genomes, config):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        # Listen for incoming connections
        self.socket.listen()

        print(f"Requested attributes: {self.inputs}")

        for genome_id, genome in genomes:
            genome.fitness = 0
            if self.last_gemone is None:
                self.update_info(key=genome.key)
            else:
                self.update_info(genome)
            self.train_ai(genome, config)
            while self.pause_training:
                if self.quit_training:
                    break
                mouse_pos = pygame.mouse.get_pos()
                if self.handle_training_events(mouse_pos, genome):
                    break
                if self.last_gemone is None:
                    self.info(key=genome.key)
                else:
                    self.info(genome)
            if self.pause_training and self.quit_training:
                break

        if self.quit_training:
            self.buttons = [
                training_btn((640, 635), "Return")
            ]
            while not self.quit_training:
                mouse_pos = pygame.mouse.get_pos()
                if self.handle_training_events(mouse_pos, self.last_gemone):
                    break
                self.info(self.last_gemone_obj)

        self.socket.close()

    def run_neat(self, config):
        if self.start_gen == -1:
            p = neat.Population(config)
        else:
            checkpoint_file = f"..\\agents\\NEAT\\cps\\{self.game_name}\\train_checkpoint_{str(self.start_gen)}"
            p = neat.checkpoint.Checkpointer.restore_checkpoint(checkpoint_file)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        cps_path = "..\\agents\\NEAT\\cps\\" + self.game_name
        if not os.path.exists(cps_path):
            try:
                os.mkdir(cps_path)
            except OSError as error:
                print("Directory creation failed: ", error)

        cp_prefix = f"{cps_path}\\train_checkpoint_"
        checkpointer = neat.Checkpointer(generation_interval=1, filename_prefix=cp_prefix)

        p.add_reporter(stats)
        p.add_reporter(checkpointer)

        try:
            winner = p.run(self.genomes_eval, self.generations)
            with open(f"{cps_path}\\trained_ai", "wb") as f:
                pickle.dump(winner, f)
        except TypeError:
            winner = self.best_genome_obj
            with open(f"{cps_path}\\unfinished_best_genome", "wb") as f:
                pickle.dump(winner, f)

        # Copy config with train setting
        destination_file = os.path.join(cps_path, 'config.txt')
        os.makedirs(cps_path, exist_ok=True)
        if self.start_gen == -1:
            shutil.copy(self.config_path, destination_file)

    def neat_setup(self):
        if self.start_gen == -1:
            self.update_config()
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             self.config_path)

        if self.start_gen != -1:
            self.total_genomes = self.start_gen * config.pop_size
            self.threshold = config.fitness_threshold
            self.population = config.pop_size
        self.run_neat(config)

        return

    def add_essentials(self):
        essentials = ['rect.x', 'rect.y', 'rect.w', 'rect.h', 'score']

        object_list = list(self.inputs.keys())
        player_key = object_list[0]

        # Add attributes to the key accessed by index
        for index, attribute in enumerate(essentials):
            self.inputs[player_key].insert(index + 1, attribute)

    def test_inputs(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        # Listen for incoming connections
        self.socket.listen()
        subprocess.Popen(["python", self.game_path], shell=True)

        client_socket, addr = self.socket.accept()
        client_socket.sendall(pickle.dumps(self.inputs))

        data = client_socket.recv(4096)
        data, input_arr = self.organize_data(data)

        print(f"\nData example: {data}\nInputs example: {input_arr}\nInput length: {len(input_arr)}")
        self.socket.close()

        return len(input_arr)

    def organize_data(self, data):
        data = pickle.loads(data)
        input_arr = np.array([])
        for s in data:
            value = s[1]
            if '(' in s[1] or '[' in s[1]:
                arr = eval(value)
                if isinstance(arr[0], list) or isinstance(arr[0], np.ndarray):
                    for sub_arr in arr:
                        sub_arr = np.array(sub_arr)
                        input_arr = np.concatenate((input_arr, sub_arr.flatten()))
                else:
                    arr = np.array(arr)
                    input_arr = np.concatenate((input_arr, arr.flatten()))
            elif s[0] == 'score':
                self.score = float(s[1])
            elif s[0] in ['rect.x', 'rect.y', 'rect.w', 'rect.h']:
                self.set_player_frame(s)
            else:
                input_arr = np.append(input_arr, float(s[1]))
        return data, input_arr

    def update_config(self):
        attributes = ['fitness_threshold', 'pop_size', 'num_outputs', 'num_inputs', 'num_hidden']
        values = [self.threshold, self.population, len(self.outputs) + 1, self.test_inputs(), self.num_hidden]

        with open(self.config_path, 'r') as file:
            config_lines = file.readlines()

        updated_lines = []

        for line in config_lines:
            line_strip = line.strip()
            updated_line = line

            for attribute, new_value in zip(attributes, values):
                if line_strip.startswith(attribute):
                    updated_line = f"{attribute} = {new_value}\n"
                    break

            updated_lines.append(updated_line)

        with open(self.config_path, 'w') as file:
            file.writelines(updated_lines)

    def update_info(self, genome=None, key=None):
        self.info(genome, key)

        self.total_genomes += 1
        self.curr_generation = (self.total_genomes - 1) // self.population

    def handle_training_events(self, mouse_pos, genome):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.buttons[0].check_input(mouse_pos):
                    if self.buttons[0].text_input == "Next Genome":
                        return True
                    elif self.buttons[0].text_input == "Resume Training":
                        self.buttons = [
                            training_btn((365, 635), "Next Genome"),
                            training_btn((640, 635), "Pause Training"),
                            training_btn((915, 635), "Quit Training")
                        ]
                        self.info(genome)
                        self.pause_training = False
                if len(self.buttons) >= 2:
                    if self.buttons[1].check_input(mouse_pos):
                        if self.buttons[1].text_input == "Pause Training":
                            self.pause_training = True
                            self.buttons = [
                                training_btn((490, 635), "Resume Training"),
                                training_btn((790, 635), "Quit Training")
                            ]
                            self.info(genome)
                            return True
                        else:
                            self.quit_training = True
                            return True
                if len(self.buttons) == 3:
                    if self.buttons[2].check_input(mouse_pos):
                        self.pause_training = True
                        self.quit_training = True
                        return True

        return False

    def info(self, genome=None, key=None):
        if key is None:
            key = genome.key
        info = [
            train_info(f"GENERATION: {self.curr_generation}", (10, 0), alignment="topleft"),
            train_info(f"MAX GENERATIONS: {self.generations}", (10, 45), alignment="topleft", size=14),
            train_info(f"{self.total_genomes % self.population + 1}/{self.population}", (SCREEN_W // 2, 0),
                       alignment="midtop"),
            train_info(f"GENOME: {key}", (SCREEN_W - 10, 0), alignment="topright"),
        ]

        y_position = 195
        if genome is not None:
            if self.last_gemone["fitness"] > self.best_genome["fitness"]:
                self.best_genome = self.last_gemone
                self.best_genome_obj = self.last_gemone_obj

            for player in self.last_five_genomes:
                info.append(train_info(str(player["key"]), (265, y_position)))
                info.append(train_info(str(player["fitness"]), (490, y_position)))
                info.append(train_info(str(player["time"]), (765, y_position)))
                info.append(train_info(str(player["score"]), (990, y_position)))
                y_position += 50

            if self.total_genomes > 0:
                info.append(train_info(str(self.best_genome["key"]), (265, 530)))
                info.append(train_info(str(self.best_genome["fitness"]), (490, 530)))
                info.append(train_info(str(self.best_genome["time"]), (765, 530)))
                info.append(train_info(str(self.best_genome["score"]), (990, 530)))

        self.screen.fill("black")

        for label, rect in self.info_headers:
            self.screen.blit(label, rect)

        for label, rect in info:
            self.screen.blit(label, rect)

        self.update_buttons()

    def update_buttons(self):
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            button.change_color(mouse_pos)
            button.update(self.screen)

        pygame.display.update()
