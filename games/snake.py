import pickle
import socket
import time

import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 120, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

fps = 20


class Food:
    def __init__(self, snake):
        self.size = snake.size
        self.position = self.spawn(snake)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size)

    def spawn(self, snake):
        while True:
            food_pos = (
                random.randrange(0, WIDTH - self.size, self.size), random.randrange(0, HEIGHT - self.size, self.size))
            if food_pos not in snake.positions:
                return food_pos

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.position[0] + self.size // 2, self.position[1] + self.size // 2),
                           self.size // 2)

    def respawn(self, snake):
        self.position = self.spawn(snake)
        self.rect.topleft = self.position


# Snake object
class Snake:
    def __init__(self):
        self.size = 20
        self.positions = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2, HEIGHT // 2 + self.size),
                          (WIDTH // 2, HEIGHT // 2 + 2 * self.size)]
        self.direction = (0, -self.size)
        self.next_direction = self.direction
        self.rect = pygame.Rect(self.positions[0][0], self.positions[0][1], self.size, self.size)
        self.score = 0
        self.options = [0, 0, 0, 0]  # left, up, right, down

    def update_options(self):
        left_pos = (self.positions[0][0] - self.size, self.positions[0][1])
        up_pos = (self.positions[0][0], self.positions[0][1] - self.size)
        right_pos = (self.positions[0][0] + self.size, self.positions[0][1])
        down_pos = (self.positions[0][0], self.positions[0][1] + self.size)

        self.options = [
            1 if left_pos not in self.positions and 0 <= left_pos[0] < WIDTH else -1,
            1 if up_pos not in self.positions and 0 <= up_pos[1] < HEIGHT else -1,
            1 if right_pos not in self.positions and 0 <= right_pos[0] < WIDTH else -1,
            1 if down_pos not in self.positions and 0 <= down_pos[1] < HEIGHT else -1,
        ]

        if self.direction == (0, -self.size):  # going up
            self.options[3] = 0
        elif self.direction == (0, self.size):  # going down
            self.options[1] = 0
        elif self.direction == (-self.size, 0):  # going left
            self.options[2] = 0
        elif self.direction == (self.size, 0):  # going right
            self.options[0] = 0

    def move(self):
        self.direction = self.next_direction
        new_pos = (self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1])
        self.positions.insert(0, new_pos)
        self.positions.pop()
        self.rect.topleft = new_pos

    def grow(self):
        self.positions.append(self.positions[-1])
        self.score += 1

    def draw(self, screen):
        for i, pos in enumerate(self.positions):
            if i == 0:
                color = GREEN
            else:
                color = DARK_GREEN
            pygame.draw.rect(screen, color, (pos[0] + 1, pos[1] + 1, self.size - 2, self.size - 2))

    def check_collision(self, pos):
        if pos in self.positions[1:]:
            return True
        return False


def spawn_food(snake):
    while True:
        food_pos = (
            random.randrange(0, WIDTH - snake.size, snake.size), random.randrange(0, HEIGHT - snake.size, snake.size))
        if food_pos not in snake.positions:
            return food_pos


def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", 1, WHITE)
    screen.blit(text, (10, 10))


def main():
    global fps
    print("!@$!")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    print("!@$!")

    try:
        s.connect(('localhost', 8888))

        instructions = pickle.loads(s.recv(4096))
        connected = True
        fps = 0
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
        snake.update_options()

        if (snake.rect.left < 0 or snake.rect.right > WIDTH or
                snake.rect.top < 0 or snake.rect.bottom > HEIGHT or
                snake.check_collision(snake.rect.topleft)):
            pygame.quit()
            sys.exit()

        if snake.rect.colliderect(food.rect):
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
