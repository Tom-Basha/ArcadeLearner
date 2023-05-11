import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pickle
import random
import socket
import time
from random import randrange as rnd
import pygame
import sys

# Game settings
WIDTH = 1280
HEIGHT = 720
fps = 60
# Block settings
COLOR_LEGEND = {
    "1": "blue",
    "2": "green",
    "3": "red",
    "4": "orange",
    "5": "purple",
    "6": "chocolate",
    "7": "grey"
}

GAP_SIZE = 2
TOP_OFFSET = 54

# Final level
FINAL_LEVEL = 1


class BaseState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.window_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, window):
        pass


class BaseObject(pygame.sprite.Sprite):
    def __init__(self):
        super(BaseObject, self).__init__()
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 0

    def update(self):
        pass

    def draw(self, window):
        pass


class Player(BaseObject):
    def __init__(self, groups, obstacles):
        super(Player, self).__init__()
        self.x = 1280 / 2
        self.y = 688
        self.width = 120
        self.height = 27
        self.speed = 7
        self.speed_x = 0
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.rect.center = (self.x, self.y)
        self.color = pygame.Color("white")
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        self.old_rect = self.rect.copy()
        self.groups = groups
        self.obstacles = obstacles
        self.lives = 1
        self.score = 0

    def update(self):
        # Previous frame
        self.old_rect = self.rect.copy()

        self.keystate = pygame.key.get_pressed()

        # Current frame (x position)
        self.rect.x += self.speed_x

        # Preventing player from leaving the screen
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        elif self.rect.left <= 0:
            self.rect.left = 0

        if self.score > 9999999:
            self.score = 9999999


class Block(BaseObject):
    def __init__(self, block_type, pos, groups, obstacles, width, height):
        super(Block, self).__init__()
        self.type = block_type
        self.pos = pos
        self.health = int(self.type)
        self.color = COLOR_LEGEND[self.type]
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect.copy()
        self.groups = groups
        self.obstacles = obstacles

    def update(self):
        self.old_rect = self.rect.copy()
        self.color = COLOR_LEGEND[self.type]
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def damage(self):
        if self.health > 0:
            self.health -= 1
            self.type = str(self.health)

        if self.health == 0:
            self.kill()


def damage_block(block):
    if block.health > 0:
        block.health -= 1
        block.type = str(block.health)

    if block.health == 0:
        block.kill()


def stage_setup(groups, obstacles, level=1):
    # Cycle through all rows and columns in BLOCK_MAP
    block_group = pygame.sprite.Group()

    block_map = [
        "666666666666",
        "444557755444",
        "333333333333",
        "222222222222",
        "111111111111",
        "            ",
        "            ",
        "            ",
        "            "
    ]

    block_width = WIDTH / len(block_map) - 35 - GAP_SIZE
    block_height = HEIGHT / len(block_map[0]) - GAP_SIZE

    for row_index, row in enumerate(block_map):
        for col_index, col in enumerate(row):

            if col != " ":
                # Find the x and y position of each individual block
                x = col_index * (block_width + GAP_SIZE) + GAP_SIZE // 2
                y = TOP_OFFSET + row_index * (block_height + GAP_SIZE) + GAP_SIZE // 2
                block = Block(col, (x, y), groups, obstacles, block_width, block_height)
                block_group.add(block)

    return block_group


class Ball(BaseObject):
    def __init__(self, groups, obstacles, player, surf_rect):
        super(Ball, self).__init__()
        self.surf_rect = surf_rect
        self.color = pygame.Color("lightblue")
        self.radius = 12
        self.ball_rect = int(self.radius * 2 ** 0.5)
        self.rect = pygame.Rect(rnd(self.ball_rect, WIDTH - self.ball_rect), HEIGHT // 2, self.ball_rect,
                                self.ball_rect)
        self.old_rect = self.rect.copy()
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 4
        self.active = False
        self.aim = random.choice(["left", "right"])
        self.groups = groups
        self.obstacles = obstacles
        self.player = player

        # Sticking the ball to the player pad
        self.rect.center = self.player.rect.center
        self.rect.bottom = self.player.rect.top

        # Shooting the ball
        if self.aim == "left":
            self.speed_x = -self.speed
            self.speed_y = -self.speed

        elif self.aim == "right":
            self.speed_x = self.speed
            self.speed_y = -self.speed

        self.active = True

    def update(self):
        # Previous frame
        self.old_rect = self.rect.copy()

        # Current frame (x, y positions)
        if self.active:
            self.rect.x += self.speed_x
            self.collision("horizontal")
            self.collision_window("horizontal")
            self.rect.x = round(self.rect.x)

            self.rect.y += self.speed_y
            self.collision("vertical")
            self.collision_window("vertical")
            self.rect.y = round(self.rect.y)

    def reset_ball(self):
        if self.player.lives > 0:
            self.player.lives -= 1

            if self.player.lives != 0:
                self.active = True

    def draw(self, window):
        pygame.draw.circle(window, (self.color.r, self.color.g, self.color.b), (self.rect.center), self.radius)

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacles, False)

        if self.rect.colliderect(self.player.rect):
            collision_sprites.append(self.player)

        if collision_sprites:
            if direction == "horizontal":
                for sprite in collision_sprites:
                    if getattr(sprite, 'health', None):
                        damage_block(sprite)
                        self.player.score += 1

                    # Collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.rect.x = self.rect.x
                        self.speed_x *= -1

                    # Collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.rect.x = self.rect.x
                        self.speed_x *= -1

            if direction == "vertical":
                for sprite in collision_sprites:
                    if getattr(sprite, 'health', None):
                        damage_block(sprite)
                        self.player.score += 1

                    # Collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.rect.y = self.rect.y
                        self.speed_y *= -1

                    # Collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.rect.y = self.rect.y
                        self.speed_y *= -1

    def collision_window(self, direction):
        if direction == "horizontal":
            if self.rect.left < 0:
                self.rect.left = 0
                self.rect.x = self.rect.x
                self.speed_x *= -1

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.rect.x = self.rect.x
                self.speed_x *= -1

        if direction == "vertical":
            if self.rect.top <= TOP_OFFSET:
                self.rect.top = TOP_OFFSET
                self.rect.y = self.rect.y
                self.speed_y *= -1

            if self.rect.top > HEIGHT:
                self.reset_ball()


class GamePlay(BaseState):
    def __init__(self):
        super(GamePlay, self).__init__()
        self.level = 1
        self.reset = False

        # Used to determine if the player has lost or won
        self.status = ""

        # Used to pause the game
        self.paused = False

        self.main_surface = pygame.Surface((WIDTH, HEIGHT))
        self.main_rect = self.main_surface.get_rect()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collide_sprites = pygame.sprite.Group()
        self.block_group = stage_setup(self.all_sprites, self.collide_sprites)

        # Classes
        self.player = Player(self.all_sprites, self.collide_sprites)
        self.ball = Ball(self.all_sprites, self.collide_sprites, self.player, self.main_rect)

        # Sprites setup
        self.all_sprites.add(self.player, self.block_group)
        self.collide_sprites.add(self.block_group)

        # Text setup
        self.ui_font = pygame.font.Font(None, 40)
        self.score = self.player.score
        self.score_text = self.ui_font.render(f"Score: {self.score}", True, pygame.Color("White"))
        self.score_rect = self.score_text.get_rect(center=(70, 25))

        self.lives = self.player.lives
        self.lives_text = self.ui_font.render(f"Lives: {self.lives}", True, pygame.Color("White"))
        self.lives_rect = self.lives_text.get_rect(center=(1210, 25))

        self.paused_text = self.font.render(f"Paused", True, pygame.Color("White"))
        self.paused_rect = self.paused_text.get_rect(center=self.window_rect.center)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.speed_x = -self.player.speed
                elif event.key == pygame.K_RIGHT:
                    self.player.speed_x = self.player.speed
                else:
                    self.player.speed_x = 0

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True

    def startup(self, persistent):
        self.persist["score"] = 0

        # Reseting the player position
        self.player.rect.center = (self.player.x, self.player.y)

        # Reseting the ball's status/position
        self.ball.active = False

        if self.status == "loser" or self.reset:
            # Reseting the player score
            self.score = 0
            self.player.score = 0

            # Reseting the player's lives
            self.lives = 3
            self.player.lives = 3

            self.level = 1

        # Reseting the level
        if not self.block_group or self.status == "loser":
            self.all_sprites.empty()
            self.collide_sprites.empty()
            self.block_group.empty()
            self.block_group = stage_setup(self.all_sprites, self.collide_sprites, self.level)

            self.all_sprites.add(self.player, self.block_group)
            self.collide_sprites.add(self.block_group)

    def draw(self, window):
        window.fill(pygame.Color("black"))

        window.blit(self.main_surface, self.main_rect)

        self.main_surface.fill(pygame.Color("black"))

        # Drawing the game objects
        self.all_sprites.draw(self.main_surface)
        self.ball.draw(self.main_surface)

        # Drawing the ui text
        window.blit(self.score_text, self.score_rect)
        window.blit(self.lives_text, self.lives_rect)

        if self.paused:
            window.blit(self.paused_text, self.paused_rect)

    def update(self, dt):
        if not self.paused:

            # Updating the lives text
            self.lives = self.player.lives
            self.lives_text = self.ui_font.render(f"Lives: {self.lives}", True, pygame.Color("White"))

            # Updating the score text
            self.score = self.player.score
            self.persist["score"] = self.score
            self.score_text = self.ui_font.render(f"Score: {self.score}", True, pygame.Color("White"))

            # Updating the game objects
            self.all_sprites.update()
            self.ball.update()

            if self.player.lives == 0:
                self.done = True

            if not self.block_group:
                self.status = "winner"
                self.persist["status"] = self.status
                self.persist["level"] = self.level

                self.level += 1

                if self.level <= FINAL_LEVEL:
                    self.done = True

                elif self.level > FINAL_LEVEL:
                    self.done = True


class Game(object):
    def __init__(self, window):
        self.done = False
        self.window = window
        self.clock = pygame.time.Clock()

        self.state_name = "GAMEPLAY"
        self.state = GamePlay()

    def event_loop(self):
        self.state.get_event()

    def flip_state(self):
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state.startup(persistent)

    def update(self, dt):
        self.state.update(dt)

        if self.state.quit:
            self.done = True

        elif self.state.done:
            self.done = True

    def draw(self):
        self.state.draw(self.window)

    def run(self):
        global fps
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        try:
            s.connect(('localhost', 8888))
            instructions = pickle.loads(s.recv(4096))
            # print(f"Requested attributes: {instructions}")
            connected = True
            fps = 0
        except ConnectionRefusedError:
            pass

        while not self.done:
            active_objects = [self.state.player, self.state.ball]

            dt = self.clock.tick(fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()

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
    # initializing pygame and setting the screen resolution
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

    # Game class instance
    game = Game(window)
    game.run()

    # Closing the game
    pygame.quit()
    sys.exit()
