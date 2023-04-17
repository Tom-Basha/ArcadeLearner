import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pickle
import socket
import time

import pygame
import random
import sys


class GameSnake:
    def __init__(self):
        self.difficulty = 30

        self.frame_size_x = 720
        self.frame_size_y = 480

        # Checks for errors encountered
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)

        # Initialise game window
        pygame.display.set_caption('Snake')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        # Colors (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.snake_pos = [100, 50]
        self.possible_move = [0, 1, 1, 1]   # left, up, right, down
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]
        self.lives = 1
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                         random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True

        self.score = 0
        self.direction = 2
        self.change_to = self.direction

    # Score
    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.frame_size_x / 10, 15)
        else:
            score_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 1.25)
        self.game_window.blit(score_surface, score_rect)
        # pygame.display.flip()

    # Main game loop


def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    try:
        s.connect(('localhost', 8888))
        instructions = pickle.loads(s.recv(4096))
        print(f"Requested attributes: {instructions}")
        connected = True
    except ConnectionRefusedError:
        pass

    snake = GameSnake()
    active_obj = [snake]

    while True:

        # Handling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_to = 0
                if event.key == pygame.K_DOWN:
                    snake.change_to = 1
                if event.key == pygame.K_LEFT:
                    snake.change_to = 3
                if event.key == pygame.K_RIGHT:
                    snake.change_to = 2
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # If two keys pressed simultaneously
        # we don't want snake to move into two directions
        # simultaneously
        if snake.change_to == 0 and snake.direction != 1:
            snake.direction = 0
        if snake.change_to == 1 and snake.direction != 0:
            snake.direction = 1
        if snake.change_to == 3 and snake.direction != 2:
            snake.direction = 3
        if snake.change_to == 2 and snake.direction != 3:
            snake.direction = 2

        # Moving the snake
        if snake.direction == 0:
            snake.snake_pos[1] -= 10
        if snake.direction == 1:
            snake.snake_pos[1] += 10
        if snake.direction == 3:
            snake.snake_pos[0] -= 10
        if snake.direction == 2:
            snake.snake_pos[0] += 10

        # Snake body growing mechanism
        # if snake head is in the same position as the food
        if snake.food_spawn:
            snake.food_pos = [random.randrange(1, (snake.frame_size_x // 10)) * 10,
                              random.randrange(1, (snake.frame_size_y // 10)) * 10]
        snake.food_spawn = False
        snake.snake_body.insert(0, list(snake.snake_pos))
        if snake.snake_pos == snake.food_pos:
            snake.food_spawn = True
            snake.score += 1
        else:
            snake.snake_body.pop()

        # Background
        snake.game_window.fill(snake.black)

        # Draw Snake
        for pos in snake.snake_body:
            pygame.draw.rect(snake.game_window, snake.green, pygame.Rect(
                pos[0], pos[1], 10, 10))

        # Draw Food
        pygame.draw.rect(snake.game_window, snake.white, pygame.Rect(
            snake.food_pos[0], snake.food_pos[1], 10, 10))

        # Game Over conditions
        if snake.snake_pos[0] < 0 or snake.snake_pos[0] > snake.frame_size_x - 10:
            snake.lives -= 1
        if snake.snake_pos[1] < 0 or snake.snake_pos[1] > snake.frame_size_y - 10:
            snake.lives -= 1

        if snake.lives == 0:
            break

        # Touching the snake body
        for block in snake.snake_body[1:]:
            if snake.snake_pos == block:
                break

        # Score Display
        snake.show_score(1, snake.white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Frame Per Second /Refresh Rate
        snake.fps_controller.tick(snake.difficulty)

        if connected:
            data = []
            for attribute in instructions:
                data.append(str(getattr(snake, attribute)))
            data = dict(zip(instructions, data))
            s.sendall(pickle.dumps(data))
            action = s.recv(4096)
            action = pickle.loads(action)
            if action != 0:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=eval(action)))
            time.sleep(0.001)

    s.close()
    return


if __name__ == "__main__":
    run()
