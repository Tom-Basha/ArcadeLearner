import os
import pickle
import socket
import sys
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import random

import pygame

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 180)
YELLOW = (255, 255, 0)
FOOD = (190, 136, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 153, 255)
CYAN = (0, 255, 255)
POWER_UP = (215, 100, 0)

# Define the size of Pac-Man
PACMAN_SIZE = 20
PACMAN_SPEED = 20

# Define the starting position of Pac-Man
START_X = 14 * PACMAN_SIZE
START_Y = 26 * PACMAN_SIZE

# Define the size of each block
BLOCK_SIZE = 20

# Define the radius of the food
FOOD_RADIUS = 2

# Define the dimensions of the map
MAP_WIDTH = 28
MAP_HEIGHT = 33

fps = 30
# Initialize Pygame
pygame.init()

# Set the size of the window
window_size = (MAP_WIDTH * BLOCK_SIZE, MAP_HEIGHT * BLOCK_SIZE)
screen = pygame.display.set_mode(window_size, pygame.NOFRAME)


# Define a function to draw a wall block
def draw_wall_block(x, y):
    pygame.draw.rect(screen, BLUE, [x + 2, y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4])


# Define a function to draw an empty block
def draw_empty_block(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 0)


# Define a function to draw a food block
def draw_food_block(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 0)
    pygame.draw.circle(screen, FOOD, [x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2], FOOD_RADIUS, 0)


# Define a function to draw a power up block
def draw_power_up_block(x, y):
    pygame.draw.rect(screen, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 0)
    pygame.draw.circle(screen, POWER_UP, [x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2], FOOD_RADIUS * 3, 0)


# Define a function to draw the entire map
def draw_map(map_matrix):
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            x = col * BLOCK_SIZE
            y = row * BLOCK_SIZE
            if map_matrix[row][col] == -1:
                draw_wall_block(x, y)
            elif map_matrix[row][col] == 0:
                draw_empty_block(x, y)
            elif map_matrix[row][col] == 1:
                draw_food_block(x, y)
            elif map_matrix[row][col] == 2:
                draw_power_up_block(x, y)


class PacMan:
    def __init__(self, x, y, board):
        self.rect = pygame.Rect(x, y, PACMAN_SIZE, PACMAN_SIZE)
        self.score = 0
        self.speed = 20
        self.steps = 0  # Add a steps counter
        self.score_font = pygame.font.Font(None, 36)  # New font object for displaying the score
        self.power_timer = 0
        self.map = board
        self.direction = "up"
        self.next_direction = "up"
        self.position = (x, y)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.rect.center, PACMAN_SIZE // 2, 0)

    def move(self, ghosts):
        # Check if the next_direction is possible
        next_x, next_y = self.rect.x, self.rect.y
        if self.next_direction == "right":
            next_x = (self.rect.x + self.speed) % (len(self.map[0]) * PACMAN_SIZE)
        elif self.next_direction == "left":
            next_x = (self.rect.x - self.speed) % (len(self.map[0]) * PACMAN_SIZE)
        elif self.next_direction == "up":
            next_y = (self.rect.y - self.speed)
        elif self.next_direction == "down":
            next_y = (self.rect.y + self.speed)

        grid_next_x = next_x // PACMAN_SIZE
        grid_next_y = next_y // PACMAN_SIZE

        # Check if the grid position is within the grid bounds and not a wall (-1)
        if (0 <= grid_next_x < len(self.map[0])) and (0 <= grid_next_y < len(self.map)):
            if self.map[grid_next_y][grid_next_x] != -1:
                self.direction = self.next_direction

        # Check if the current direction is possible
        if self.direction == "right":
            next_x = (self.rect.x + self.speed) % (len(self.map[0]) * PACMAN_SIZE)
            next_y = self.rect.y
        elif self.direction == "left":
            next_x = (self.rect.x - self.speed) % (len(self.map[0]) * PACMAN_SIZE)
            next_y = self.rect.y
        elif self.direction == "up":
            next_x = self.rect.x
            next_y = (self.rect.y - self.speed)
        elif self.direction == "down":
            next_x = self.rect.x
            next_y = (self.rect.y + self.speed)

        grid_next_x = next_x // PACMAN_SIZE
        grid_next_y = next_y // PACMAN_SIZE

        # Collect food if the current grid position is a food block (1)
        if self.map[grid_next_y][grid_next_x] == 1:
            self.map[grid_next_y][grid_next_x] = 0
            self.score += 1
        if map_matrix[grid_next_y][grid_next_x] == 2:
            map_matrix[grid_next_y][grid_next_x] = 0
            self.score += 5
            self.power_timer = 5000
            for ghost in ghosts:
                ghost.eat_phase = True

        if self.power_timer > 0:
            self.power_timer -= 30  # frame_time is the time since the last frame in milliseconds
            for ghost in ghosts:
                if ghost.free:
                    ghost.timer = self.power_timer
        else:
            for ghost in ghosts:
                ghost.eat_phase = False

        # Move Pac-Man in the current direction if possible
        if (0 <= grid_next_x < len(self.map[0])) and (0 <= grid_next_y < len(self.map)):
            if self.map[grid_next_y][grid_next_x] != -1:
                self.rect.x = next_x
                self.rect.y = next_y

        # Wrap Pac-Man around the screen if it goes off the edges
        if self.rect.left > (len(self.map[0]) * PACMAN_SIZE):
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = len(self.map[0]) * PACMAN_SIZE

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.next_direction = "left"
            elif event.key == pygame.K_RIGHT:
                self.next_direction = "right"
            elif event.key == pygame.K_UP:
                self.next_direction = "up"
            elif event.key == pygame.K_DOWN:
                self.next_direction = "down"

    def draw_score(self):
        score_text = self.score_font.render("Score: {}".format(self.score), True, WHITE)
        screen.blit(score_text, (
            BLOCK_SIZE * MAP_WIDTH // 2 - score_text.get_width() // 2,
            10))  # Center the score text at the top of the screen


class Ghost:
    def __init__(self, x, y, color, timer):
        self.rect = pygame.Rect(x * PACMAN_SIZE, y * PACMAN_SIZE, PACMAN_SIZE, PACMAN_SIZE)
        self.start_x = x
        self.start_y = y
        self.speed = 20
        self.free = False
        self.position = (x, y)
        self.color = color
        self.timer = timer
        self.last_move = pygame.time.get_ticks()
        self.direction = random.choice(["up", "down", "left", "right"])
        self.eat_phase = False

    def move(self, grid, pacman_x, pacman_y, blinky=None):
        if pygame.time.get_ticks() - self.last_move > self.timer and not self.free:
            self.rect.x, self.rect.y = 14 * PACMAN_SIZE, 13 * PACMAN_SIZE
            self.position = (14, 13)
            time.sleep(0.01)
            self.last_move = pygame.time.get_ticks()
            self.timer = 0
            self.free = True

        if self.free:
            # Check if the next_direction is possible
            next_x, next_y = self.rect.x, self.rect.y
            if self.direction == "right":
                next_x = (self.rect.x + self.speed) % (len(grid[0]) * PACMAN_SIZE)
            elif self.direction == "left":
                next_x = (self.rect.x - self.speed) % (len(grid[0]) * PACMAN_SIZE)
            elif self.direction == "up":
                next_y = (self.rect.y - self.speed)
            elif self.direction == "down":
                next_y = (self.rect.y + self.speed)

            grid_next_x = next_x // PACMAN_SIZE
            grid_next_y = next_y // PACMAN_SIZE

            if grid[grid_next_y][grid_next_x] == -1:
                self.random_move()
            else:
                self.rect.x, self.rect.y = next_x, next_y
                self.position = (next_x // 20, next_y // 20)
                if self.color == RED:
                    self.blinky(pacman_x, pacman_y)
                elif self.color == PINK:
                    self.pinky(pacman_x, pacman_y)
                elif self.color == CYAN:
                    self.inky(pacman_x, pacman_y, blinky.position[0], blinky.position[1])
                elif self.color == GREEN:
                    self.clyde(pacman_x, pacman_y)

    def draw(self):
        color = self.color
        if self.free:
            if self.eat_phase:
                # Blink in blue and white if the ghost can be eaten
                color = WHITE if self.timer % 200 < 100 else BLUE

        pygame.draw.circle(screen, color, self.rect.center, PACMAN_SIZE // 2)

    def blinky(self, pacman_x, pacman_y):
        if self.in_line(pacman_x, pacman_y):
            self.towards(pacman_x, pacman_y)
        else:
            self.random_move()

    def pinky(self, pacman_x, pacman_y):
        pacman_x, pacman_y = pacman_x + 4, pacman_y + 4
        if self.in_map(pacman_x, pacman_y):
            self.towards(pacman_x, pacman_y)
        else:
            self.random_move()

    def inky(self, pacman_x, pacman_y, blinky_x, blinky_y):
        target_x, target_y = pacman_x * 2 - blinky_x, pacman_y * 2 - blinky_y
        if self.in_map(target_x, target_y):
            self.towards(target_x, target_y)
        else:
            self.random_move()

    def clyde(self, pacman_x, pacman_y):
        if self.distance_x(pacman_x) > 8 and self.distance_y(pacman_y) > 8:
            self.random_move()
        else:
            self.away(pacman_x, pacman_y)

    def in_line(self, pacman_x, pacman_y):
        return self.position[0] == pacman_x or self.position[1] == pacman_y

    def towards(self, pacman_x, pacman_y):
        if self.position[0] == pacman_x:
            if self.position[1] < pacman_y:
                self.direction = "down"
            else:
                self.direction = "up"
        else:
            if self.position[0] < pacman_x:
                self.direction = "right"
            else:
                self.direction = "left"

    def random_move(self):
        self.direction = random.choice(["up", "down", "left", "right"])

    def in_map(self, pacman_x, pacman_y):
        return 0 <= pacman_x <= 27 and 2 <= pacman_y <= 32

    def distance_x(self, pacman_x):
        return pacman_x - self.position[0]

    def distance_y(self, pacman_y):
        return pacman_y - self.position[1]

    def away(self, pacman_x, pacman_y):
        if self.distance_x(pacman_x) < self.distance_y(pacman_y):
            if self.position[0] < pacman_x:
                self.direction = "left"
            else:
                self.direction = "right"
        else:
            if self.position[1] < pacman_y:
                self.direction = "up"
            else:
                self.direction = "down"


# Define the matrix representing the map (fill in the matrix here)
map_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1],
    [-1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1],
    [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
    [-1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1],
    [-1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1],
    [-1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1],
    [-1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1],
    [-1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]


def main():
    global fps
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    try:
        s.connect(('localhost', 8888))
        instructions = pickle.loads(s.recv(4096))
        connected = True
        fps = 0
    except ConnectionRefusedError:
        pass

    # Draw the map
    draw_map(map_matrix)

    pacman = PacMan(START_X, START_Y, map_matrix)

    # Create pacman and 4 ghosts
    ghosts = [
        Ghost(12, 16, RED, 3000),
        Ghost(15, 16, PINK, 6000),
        Ghost(13, 16, CYAN, 9000),
        Ghost(14, 16, GREEN, 12000),
    ]

    active_objects = [pacman, ghosts[0], ghosts[1], ghosts[2], ghosts[3]]

    # Update the display
    pygame.display.update()
    clock = pygame.time.Clock()

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            pacman.handle_event(event)

        # Move ghosts
        for ghost in ghosts:
            ghost.move(pacman.map, pacman.rect.x // 20, pacman.rect.y // 20, ghosts[0])

        pacman.move(ghosts)

        for ghost in ghosts:
            if pacman.rect.colliderect(ghost.rect):
                if pacman.power_timer > 0:
                    # Send the ghost to a specific location for 4 seconds
                    ghost.rect.x, ghost.rect.y = ghost.start_x * BLOCK_SIZE, ghost.start_y * BLOCK_SIZE
                    ghost.timer = 4000
                    ghost.last_move = pygame.time.get_ticks()
                    ghost.free = False
                else:
                    running = False

        # Draw Pac-Man
        screen.fill(BLACK)
        draw_map(pacman.map)
        pacman.draw()
        for obj in ghosts + [pacman]:
            obj.draw()
        pacman.draw_score()

        # Update the display
        pygame.display.update()
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

            # print(data)

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
