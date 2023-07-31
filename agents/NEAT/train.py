import json
import os
import pickle
import shutil
import socket
import subprocess
import sys

import numpy as np
import neat
import time

from assets.components.button import training_btn, back_btn
from assets.error import error_msg
from assets.utils import *

pygame.init()


class Trainer:
    # Initialize paths, labels, training settings and other variables.
    def __init__(self, game_name, game_path, inputs, outputs, threshold, generations, population,
                 start_gen, num_hidden):
        self.hidden_layers = num_hidden
        self.generations = generations
        self.start_gen = start_gen
        self.population = population
        self.threshold = threshold
        self.game_name = game_name
        self.game_path = game_path
        self.inputs = inputs
        self.outputs = list(outputs)

        if start_gen != -1:
            self.config_path = f"..\\agents\\NEAT\\games\\{game_name}\\config.txt"
        else:
            self.config_path = "..\\agents\\NEAT\\config.txt"
            self.add_essentials()

        self.game_h = None
        self.game_w = None

        self.socket = None
        self.player_frame = [0, 0, 0, 0]
        self.prev_player_frame = [0, 0, 0, 0]

        self.score = 0
        self.duration = 0
        self.penalty = 0

        self.valid_input = True
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

        self.winner_key = None
        self.winner_gen = None
        self.winner_score = None
        self.winner_fitness = None

    # Inputs: Genome (AI player), NEAT config.
    # Description: AI player game loop.
    #              Runs a game, let the genome make moves, calculates fitness.
    def train_ai(self, genome, config):
        # Loads current genome neural network.
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Run the game as a subprocess.
        subprocess.Popen(["python", self.game_path], shell=True)

        # Waits for connection, and sends the game the required attributes.
        client_socket, addr = self.socket.accept()
        client_socket.sendall(pickle.dumps(self.inputs))

        self.score = 0
        self.penalty = 0
        start_time = time.time()

        game_w = 1280
        game_h = 720

        # Main AI player loop.
        while True:
            data = client_socket.recv(4096)

            # Checks if data was sent from the game.
            if data:
                data, input_arr = self.organize_data(data)

                self.update_buttons()
                mouse_pos = pygame.mouse.get_pos()
                if self.handle_training_events(mouse_pos, genome):
                    break

                # Sends data to the neural network, gets an action, sends the action to the game.
                move = self.action(net, input_arr)
                client_socket.sendall(pickle.dumps(move))

                # Check for movement
                self.frame_penalty(game_w, game_h)

                # Calculates current play time and fitness.
                self.duration = round(time.time() - start_time, 3)
                self.update_fitness(genome)

                # Checks if genome got to the required threshold (Win), else continue playing.
                if genome.fitness >= self.threshold:
                    if self.score > 10:
                        self.winner_score = self.score
                        self.winner_gen = self.curr_generation
                        self.winner_key = genome.key
                        self.winner_fitness = round(genome.fitness, 3)
                    else:
                        genome.fitness = 5
                    break
            else:
                # The player lost.
                break

        # Penalties check.
        self.duration = round(time.time() - start_time, 3)
        if self.duration < 5 and self.score <= 10:
            self.penalty += 20
        elif self.score <= 5:
            self.penalty += 5
        elif self.duration < 2:
            self.penalty += 30

        # Calculates final fitness.
        self.update_fitness(genome)

        if self.duration > 300 and self.score < 5:
            genome.fitness = -5
            
        print(
            f"{genome.key}.\t\t Fitness: {round(genome.fitness, 3)}\t|\t Duration: {self.duration}\t|\t Score: {self.score}")

        # Saves data to show in the control screen.
        self.last_gemone = {"key": genome.key, "fitness": round(genome.fitness, 3), "time": self.duration,
                            "score": self.score}
        self.last_gemone_obj = genome

        if len(self.last_five_genomes) >= 5:
            self.last_five_genomes.pop(0)
        self.last_five_genomes.append(self.last_gemone)

        return False

    # Inputs: Genome.
    # Description: Updates the genome fitness.
    def update_fitness(self, genome):
        genome.fitness = self.score + self.duration / 2 - self.penalty

    # Inputs: Player frame data.
    # Description: Updates the player location.
    def set_player_frame(self, info):
        name, value = info[0], eval(info[1])
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

    # Inputs: The player's neural network, data from the game.
    # Outputs: The player's next move.
    # Description: Gets data from the game, send it to the genome's neural network and gets an action to execute.
    def action(self, net, values):
        # Send data to neural network and get the decision.
        output = net.activate(values)    # [0.30 0.57 0.13]
        decision = output.index(max(output))

        # 0 = Doing nothing.
        if decision == 0:
            self.penalty += 0.001       # Add penalty to discourage this kind of behavior.
            return 0
        else:
            decision -= 1
            return self.outputs[decision]       # Translates decision to action and returns the action.

    # Inputs: Game width, game height.
    # Description: Updates the penalty factor if the player touches the game window frame and if the player doesn't move.
    def frame_penalty(self, w, h):
        # Game window penalty.
        if self.player_frame[0] == 0:
            self.penalty += 0.01
        if self.player_frame[1] == 0:
            self.penalty += 0.01
        if self.player_frame[2] == w:
            self.penalty += 0.01
        if self.player_frame[3] == h:
            self.penalty += 0.01

        # Movement penalty.
        moved = False
        for i in range(len(self.player_frame)):
            if self.player_frame[i] != self.prev_player_frame[i]:
                moved = True

        if not moved:
            self.penalty += 0.01

        self.prev_player_frame = self.player_frame.copy()

    # Inputs: Genomes (players), loaded config.
    # Description: Evaluates genomes fitness by letting them play the game one by one.
    def genomes_eval(self, genomes, config):
        # Creates socket and listening to incoming connections.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        self.socket.listen()

        # Each genome plays the game and gets his fitness score.
        for genome_id, genome in genomes:
            genome.fitness = 0
            if self.last_gemone is None:
                self.update_info(key=genome.key)
            else:
                self.update_info(genome)
            self.train_ai(genome, config)               # Train function.

            # Training screen controls.
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

        # Closes the socket when the training is finished.
        self.socket.close()

    # Inputs: Loaded config.
    # Description: Setting up the reporters for stats, final train setting
    def run_neat(self, config):
        # Sets the destinations paths.
        game_files = f"..\\agents\\NEAT\\games\\{self.game_name}"
        cps_path = f"..\\agents\\NEAT\\games\\{self.game_name}\\checkpoints"
        cp_prefix = f"{cps_path}\\train_checkpoint_"

        finished = False
        if self.start_gen == -1:                    # New AI train
            p = neat.Population(config)
            if os.path.exists(cps_path):
                shutil.rmtree(cps_path)
        else:                                       # Start from checkpoint
            checkpoint_file = f"{cp_prefix}{self.start_gen}"
            p = neat.checkpoint.Checkpointer.restore_checkpoint(checkpoint_file)

        # Adds reporters and creates the NEAT population.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()

        if not os.path.exists(cps_path):
            try:
                os.makedirs(cps_path, exist_ok=True)
            except OSError as error:
                print("Directory creation failed: ", error)

        checkpointer = neat.Checkpointer(generation_interval=1, filename_prefix=cp_prefix)      # Sets checkpoint interval and path.
        p.add_reporter(stats)
        p.add_reporter(checkpointer)
        start_time = time.time()

        # Runs the NEAT algorithm and saves the winning genome.
        try:
            winner = p.run(self.genomes_eval, self.generations)
            with open(f"{game_files}\\trained_ai", "wb") as f:
                pickle.dump(winner, f)
            finished = True
        except TypeError:
            winner = self.best_genome_obj
            if not finished:
                with open(f"{game_files}\\unfinished_best_genome", "wb") as f:
                    pickle.dump(winner, f)

        # Calculates total training time.
        end_time = time.time()
        elapsed_time = round(end_time - start_time)
        formatted_time = format_time(elapsed_time)

        # Saves the training data.
        self.save_data(game_files)

        # Copies the configuration file and displays a finish screen if training is completed.
        os.makedirs(game_files, exist_ok=True)
        if self.start_gen == -1:
            destination_file = os.path.join(game_files, 'config.txt')
            shutil.copy(self.config_path, destination_file)
        if finished:
            self.finish_screen(formatted_time)

    # Description: Loads the configuration file and runs NEAT's main function.
    def neat_setup(self):
        # Updates start checkpoint.
        if self.start_gen == -1:
            self.update_config()

        if self.valid_input:
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 self.config_path)

            if self.start_gen != -1:
                self.total_genomes = self.start_gen * self.population
            self.run_neat(config)
        else:
            error_msg(["Invalid attribute type.", "Please select attributes with numeric ", "values only."])

        return

    # Description: Add essentials attributes to the players object for better penalty system.
    def add_essentials(self):
        essentials = ['rect.x', 'rect.y', 'rect.w', 'rect.h', 'score']

        object_list = list(self.inputs.keys())
        player_key = object_list[0]

        # Add attributes to the key accessed by index
        for index, attribute in enumerate(essentials):
            if attribute not in self.inputs[player_key]:
                self.inputs[player_key].insert(index + 1, attribute)

    # Outputs: Length of attributes values array.
    # Description: Calculates the ture length of the attributes values input.
    #              The neural network accepts only numeral values, this function calculates how many numeral values are there.
    def test_inputs(self):
        # Creates socket and listening to incoming connections.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        self.socket.listen()

        # Opens the game as a subprocess.
        subprocess.Popen(["python", self.game_path], shell=True)

        # Socket waits for connection and sends the required attributes.
        client_socket, addr = self.socket.accept()
        client_socket.sendall(pickle.dumps(self.inputs))

        data = client_socket.recv(4096)                 # Gets the data.
        data, input_arr = self.organize_data(data)      # Orginizes the data in array.

        print(f"\nData example: {data}\nInputs example: {input_arr}\nInput length: {len(input_arr)}")
        self.socket.close()             # Closes the socket.

        return len(input_arr)

    # Inputs: Data received from the game as pickle.
    # Outputs: Data and a flattened values array.
    # Description: Flattens the data received from the game into an array and updates some data.
    def organize_data(self, data):
        data = pickle.loads(data)
        input_arr = np.array([])
        for info in data:
            value = info[1]

            # Check for invalid input.
            if '<' in info[1]:
                print(f"PROBLEM: {info[1]}, {type(info[1])}")
                self.valid_input = False

            # Checks for inner arrays/lists to flatten.
            elif '(' in info[1] or '[' in info[1]:
                arr = eval(value)
                if isinstance(arr[0], list) or isinstance(arr[0], np.ndarray):
                    for sub_arr in arr:
                        sub_arr = np.array(sub_arr)
                        input_arr = np.concatenate((input_arr, sub_arr.flatten()))
                else:
                    arr = np.array(arr)
                    input_arr = np.concatenate((input_arr, arr.flatten()))

            # Updates score.
            elif info[0] == 'score':
                self.score = float(info[1])

            # Updates the players frame.
            elif info[0] in ['rect.x', 'rect.y', 'rect.w', 'rect.h']:
                self.set_player_frame(info)
            else:
                if type(eval(info[1])) in (int, float):             # Check for invalid input.
                    input_arr = np.append(input_arr, float(info[1]))
                else:
                    print(f"PROBLEM: {info[1]}, {type(info[1])}")
                    self.valid_input = False

        return data, input_arr

    # Description: Updates the NEAT configuration file by the selected settings of the user.
    def update_config(self):
        # List of attribute names to update in the config file.
        attributes = ['fitness_threshold', 'pop_size', 'num_outputs', 'num_inputs', 'num_hidden']
        inputs_cnt = self.test_inputs()
        if not self.valid_input:
            return False

        # List of corresponding values for the attributes.
        values = [self.threshold, self.population, len(self.outputs) + 1, inputs_cnt, self.hidden_layers]

        with open(self.config_path, 'r') as file:
            config_lines = file.readlines()

        updated_lines = []

        # Iterates through each line in the config file and updates attribute values if found.
        for line in config_lines:
            line_strip = line.strip()
            updated_line = line

            for attribute, new_value in zip(attributes, values):
                if line_strip.startswith(attribute):
                    updated_line = f"{attribute} = {new_value}\n"
                    break

            updated_lines.append(updated_line)

        # Writes the updated lines back to the config file.
        with open(self.config_path, 'w') as file:
            file.writelines(updated_lines)

    # Inputs: Genome and its key.
    # Description: Updates the training control screen info.
    def update_info(self, genome=None, key=None):
        self.info(genome, key)
        self.total_genomes += 1
        self.curr_generation = (self.total_genomes - 1) // self.population

    # Inputs: Mouse position when clicked, genome.
    # Outputs: True if training needs to be stopped, false otherwise.
    # Description: Handles the training control screen events.
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

    # Inputs: Genome and its key.
    # Description: Updates the info in the training control screen.
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

    # Description: Updates button when mouse hover.
    def update_buttons(self):
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            button.change_color(mouse_pos)
            button.update(self.screen)

        pygame.display.update()

    # Inputs: Checkpoints destination folder path.
    # Description: Saves the training data in a JSON file.
    def save_data(self, cps_path):
        # Saved data.
        data = {
            "population": self.population,
            "generations": self.generations,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "threshold": self.threshold
        }

        path = f"{cps_path}\\data.json"     # Destination path.

        # Writes the data to the JSON file.
        with open(path, "w") as json_file:
            json.dump(data, json_file)

    # Inputs: Total training time.
    # Description: Shows training summery with some data.
    def finish_screen(self, timer):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        BACK_BTN = back_btn(color=GREEN)
        headers_x = SCREEN_W // 2 - 300
        resaults_x = SCREEN_W // 2 + 300
        finish_headers = [
            (train_info("Winner Key:", (headers_x, 260), alignment="topleft")),
            (train_info("Winner Generation:", (headers_x, 300), alignment="topleft")),
            (train_info("Winner Score:", (headers_x, 340), alignment="topleft")),
            (train_info("Winner Fitness:", (headers_x, 380), alignment="topleft")),
            (train_info("Training length:", (headers_x, 420), alignment="topleft")),
        ]

        resaults = [
            (train_info(f"{self.winner_key}", (resaults_x, 260), alignment="topright")),
            (train_info(f"{self.winner_gen}", (resaults_x, 300), alignment="topright")),
            (train_info(f"{self.winner_score}", (resaults_x, 340), alignment="topright")),
            (train_info(f"{self.winner_fitness}", (resaults_x, 380), alignment="topright")),
            (train_info(f"{timer}", (resaults_x, 420), alignment="topright")),
        ]

        # Labels
        HEADER_TEXT, HEADER_RECT = header("Success!", color=GREEN)
        SUBHEAD_TEXT, SUBHEAD_RECT = subhead("TRAINING COMPLETED SUCCESSFULLY!", color=WHITE, size=24)

        while True:
            screen.fill("black")

            # Set mouse
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            screen.blit(HEADER_TEXT, HEADER_RECT)
            screen.blit(SUBHEAD_TEXT, SUBHEAD_RECT)

            BACK_BTN.change_color(MENU_MOUSE_POS)
            BACK_BTN.update(screen)

            for label, rect in finish_headers:
                screen.blit(label, rect)

            for label, rect in resaults:
                screen.blit(label, rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button:
                    if BACK_BTN.check_input(MENU_MOUSE_POS):
                        return

            pygame.display.update()


# Inputs: Training time in seconds.
# Outputs: Training time in a 'hours:minutes:seconds' format.
# Description: Formats the training time into a 'hours:minutes:seconds' format.
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours == 0:
        return "{:02d}:{:02d}".format(minutes, seconds)
    else:
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
