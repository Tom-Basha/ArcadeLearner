import pickle
import socket
import time

import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 200, 200
GRID_SIZE = 15
BLOCK_SIZE = 20  # Size of each block (20x20 pixels)

# Adjust screen dimensions to fit blocks
WIDTH = GRID_SIZE * BLOCK_SIZE
HEIGHT = GRID_SIZE * BLOCK_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 120, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

fps = 20


class Snake:
    def __init__(self):
        self.size = 20
        self.positions = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2 + self.size),
                          (WIDTH // 2, HEIGHT // 2 + 2 * self.size)]
        self.direction = (0, -self.size)
        self.next_direction = self.direction
        self.rect = pygame.Rect(self.positions[0][0], self.positions[0][1], self.size, self.size)
        self.score = 0

        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for x, y in self.positions:
            self.grid[y // self.size][x // self.size] = 1
        self.grid[self.positions[0][1] // self.size][self.positions[0][0] // self.size] = 2

    def move(self):
        self.direction = self.next_direction
        new_pos = (self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1])
        old_tail = self.positions.pop()
        self.positions.insert(0, new_pos)

        self.grid[old_tail[1] // self.size][old_tail[0] // self.size] = 0

        if (0 <= new_pos[0] < WIDTH and 0 <= new_pos[1] < HEIGHT):
            self.grid[new_pos[1] // self.size][new_pos[0] // self.size] = 2

        self.grid[self.positions[1][1] // self.size][self.positions[1][0] // self.size] = 1
        self.rect.topleft = new_pos

    def grow(self):
        self.positions.append(self.positions[-1])
        self.score += 1

        self.grid[self.positions[-1][1] // self.size][self.positions[-1][0] // self.size] = 1

    def draw(self, screen):
        for i, pos in enumerate(self.positions):
            if i == 0:
                color = GREEN
            else:
                color = DARK_GREEN
            pygame.draw.rect(screen, color, (pos[0] + 1, pos[1] + 1, self.size - 2, self.size - 2))


class Food:
    def __init__(self, snake):
        self.size = snake.size
        self.position = self.spawn(snake)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size)

        snake.grid[self.position[1] // self.size][self.position[0] // self.size] = 3

    def spawn(self, snake):
        while True:
            x = random.randrange(0, WIDTH, self.size)
            y = random.randrange(0, HEIGHT, self.size)
            if snake.grid[y // self.size][x // self.size] == 0:
                return x, y

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

    def respawn(self, snake):
        snake.grid[self.position[1] // self.size][self.position[0] // self.size] = 0
        self.position = self.spawn(snake)
        self.rect.topleft = self.position

        snake.grid[self.position[1] // self.size][self.position[0] // self.size] = 3


def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", 1, WHITE)
    screen.blit(text, (10, 10))


def main():
    global fps
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    try:
        s.connect(('localhost', 8888))
        instructions = pickle.loads(s.recv(4096))
        # print(f"Requested attributes: {instructions}")
        connected = True
        fps = 60
    except ConnectionRefusedError:
        pass

    snake = Snake()
    food = Food(snake)

    active_objects = [snake, food]

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, snake.size):
                    snake.next_direction = (0, -snake.size)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -snake.size):
                    snake.next_direction = (0, snake.size)
                elif event.key == pygame.K_LEFT and snake.direction != (snake.size, 0):
                    snake.next_direction = (-snake.size, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-snake.size, 0):
                    snake.next_direction = (snake.size, 0)

        snake.move()

        # Check for collision with wall or self
        if (snake.positions[0][0] < 0 or snake.positions[0][0] >= WIDTH or
                snake.positions[0][1] < 0 or snake.positions[0][1] >= HEIGHT or
                snake.positions[0] in snake.positions[1:]):
            pygame.quit()
            sys.exit()

        # Check for collision with food
        if snake.positions[0] == food.position:
            snake.grow()
            food.respawn(snake)

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        pygame.display.flip()

        clock.tick(fps)

        if connected:
            data = []
            for class_name, attributes in instructions.items():
                for obj in active_objects:
                    if obj.__class__.__name__ == class_name and obj is not None:
                        for attr in attributes:
                            temp_obj = obj
                            temp_attr = attr
                            if "." in attr:
                                parts = attr.split(".")
                                temp_obj = getattr(obj, str(parts[0]))
                                temp_attr = parts[1]
                            if hasattr(temp_obj, temp_attr):
                                data.append((attr, str(getattr(temp_obj, temp_attr))))

            s.sendall(pickle.dumps(data))
            action = s.recv(4096)
            if action:
                action = pickle.loads(action)

                if action != 0:
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=eval(action)))
            else:
                break
            time.sleep(0.001)

    s.close()


if __name__ == "__main__":
    main()

# Closing the game
pygame.quit()
sys.exit()
