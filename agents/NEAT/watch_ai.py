import os
import pickle
import subprocess
import socket

import neat
import numpy as np
import pygame


class AI_Player:
    def __init__(self, game_name, game_path, inputs, outputs):
        self.config_path = "..\\agents\\NEAT\\games\\" + game_name + "\\config.txt"
        self.player = "..\\agents\\NEAT\\games\\" + game_name + "\\trained_ai"
        self.player_unfinished = "..\\agents\\NEAT\\games\\" + game_name + "\\unfinished_best_genome"
        self.game_name = game_name
        self.game_path = game_path
        self.inputs = inputs
        self.outputs = list(outputs)
        self.socket = None

    def neat_setup(self):
        playable = False
        player = None
        if os.path.exists(self.player) or os.path.exists(self.player_unfinished):
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
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

            self.play(winner_net)
        else:
            return False
        return True

    def play(self, winner_net):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 8888))
        self.socket.listen()

        print(f"Requested attributes: {self.inputs}")
        subprocess.Popen(["python", self.game_path], shell=True)
        client_socket, addr = self.socket.accept()
        client_socket.sendall(pickle.dumps(self.inputs))

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
                    elif s[0] in ['rect.x', 'rect.y', 'rect.w', 'rect.h', 'score']:
                        pass
                    else:
                        input_arr = np.append(input_arr, float(s[1]))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True

                move = self.action(winner_net, input_arr)
                client_socket.sendall(pickle.dumps(move))

            else:
                self.socket.close()
                break

    def action(self, net, values):
        output = net.activate(values)
        decision = output.index(max(output))
        if decision == 0:
            return 0
        else:
            decision -= 1
            return self.outputs[decision]
