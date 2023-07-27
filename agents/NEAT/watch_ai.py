import json
import os
import pickle
import socket
import subprocess

import neat
import numpy as np

from assets.utils import *

pygame.init()


class AI_Player:
    def __init__(self, game_name, game_path):
        self.winner_net = None
        self.score = None
        self.saved_folder =  f"..\\agents\\NEAT\\games\\{game_name}"
        self.config_path = f"{self.saved_folder}\\config.txt"
        self.player = f"{self.saved_folder}\\trained_ai"
        self.player_unfinished = f"{self.saved_folder}\\unfinished_best_genome"
        self.player_data = f"{self.saved_folder}\\data.json"

        if os.path.exists(self.player_data):
            with open(self.player_data, 'r') as f:
                data = json.load(f)

                self.inputs = data["inputs"]
                self.outputs = list(data["outputs"])

                self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
                pygame.display.set_caption(f"{game_name} AI Evaluation")

        self.game_name = game_name
        self.game_path = game_path

        self.socket = None

    # Description: Loads the configuration file and checks if trained AI exists.
    def neat_setup(self):
        playable = False
        player = None

        # Checks if a trained AI exists.
        if os.path.exists(self.player):
            playable = True
            if os.path.exists(self.player):
                player = self.player
            else:
                player = self.player_unfinished
        if playable:
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 self.config_path)

            with open(player, "rb") as f:
                winner = pickle.load(f)
            self.winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

        else:
            return False
        return True

    # Description: AI Player plays the game.
    def play(self):
        # Creates socket and listening to incoming connections.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        self.socket.listen()
        print(f"Requested attributes: {self.inputs}")

        # Opens the game as a subprocess.
        subprocess.Popen(["python", self.game_path], shell=True)

        # Socket waits for connection and sends the required attributes.
        client_socket, addr = self.socket.accept()
        client_socket.sendall(pickle.dumps(self.inputs))

        while True:
            data = client_socket.recv(4096)
            if data:
                # Flattens the data.
                data = pickle.loads(data)
                input_arr = np.array([])
                for s in data:
                    value = s[1]

                    # Checks for inner arrays/lists to flatten.
                    if '(' in s[1] or '[' in s[1]:
                        arr = eval(value)
                        if isinstance(arr[0], list) or isinstance(arr[0], np.ndarray):
                            for sub_arr in arr:
                                sub_arr = np.array(sub_arr)
                                input_arr = np.concatenate((input_arr, sub_arr.flatten()))
                        else:
                            arr = np.array(arr)
                            input_arr = np.concatenate((input_arr, arr.flatten()))
                    elif s[0] in ['rect.x', 'rect.y', 'rect.w', 'rect.h']:
                        pass
                    elif s[0] == 'score':
                        self.score = eval(value)
                    else:
                        input_arr = np.append(input_arr, float(s[1]))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True

                # Decides what is the next move by the neural network decision and send it to the game.
                move = self.action(self.winner_net, input_arr)
                client_socket.sendall(pickle.dumps(move))

            else:
                break

        # Closes the socket.
        self.socket.close()

    # Inputs: Genome neural network, data from the game.
    # Outputs: The player's next move.
    # Description: Gets data from the game, send it to the genome's neural network and gets an action to execute.

    def action(self, net, values):
        # Send data to neural network and get the decision.
        output = net.activate(values)
        decision = output.index(max(output))

        # 0 = Doing nothing.
        if decision == 0:
            return 0
        else:
            decision -= 1
            return self.outputs[decision]

