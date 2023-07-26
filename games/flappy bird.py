import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pickle
import socket
import time

import pygame
import random
import sys

pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

fps = 150


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect((0, 0), (20, 20))
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.rect.center = (self.x, self.y)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill("green")
        self.velocity = 0
        self.score = 0

    def update(self):
        self.velocity -= 0.4
        self.y -= self.velocity
        self.rect.y -= self.velocity

    def flap(self):
        self.velocity = 7


class Pillar(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.gap_space = 220
        self.top_height = random.randint(50, HEIGHT - self.gap_space - 50)
        self.bottom_height = HEIGHT - self.top_height - self.gap_space

        self.image = pygame.Surface((30, HEIGHT), pygame.SRCALPHA)  # Use an alpha channel for transparency

        self.top_rect = pygame.Rect(0, 0, 30, self.top_height)
        self.bottom_rect = pygame.Rect(0, self.top_height + self.gap_space, 30, self.bottom_height)
        self.gap_top = self.top_rect.bottom
        self.gap_bottom = self.bottom_rect.top
        pygame.draw.rect(self.image, BLACK, self.top_rect)
        pygame.draw.rect(self.image, BLACK, self.bottom_rect)

        self.rect = self.image.get_rect()
        self.x_pos = x
        self.rect.x = x
        self.passed = False

    def update(self):
        self.x_pos -= 3
        self.rect.x -= 3


def draw_text(screen, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def pillar_collision(bird, pillars):
    for pillar in pillars:
        if bird.rect.colliderect(pillar.top_rect.move(pillar.rect.topleft)) or \
                bird.rect.colliderect(pillar.bottom_rect.move(pillar.rect.topleft)):
            return True
    return False


def main():
    global fps
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    try:
        s.connect(('localhost', 8888))
        instructions = pickle.loads(s.recv(4096))
        connected = True
        fps = 150
    except ConnectionRefusedError:
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

    clock = pygame.time.Clock()

    bird = Bird()
    all_sprites = pygame.sprite.Group(bird)
    pillars = pygame.sprite.Group()

    active_objects = [bird, Pillar(-30)]

    pillar_spawn_counter = 0
    total_pillars = 0
    spawn_target = 420 // 3  # Dividing by the pillar speed (3) to get the required number of frames

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Spawn pillars
        pillar_spawn_counter += 1
        if pillar_spawn_counter == spawn_target:
            pillar = Pillar(WIDTH)
            all_sprites.add(pillar)
            pillars.add(pillar)
            pillar_spawn_counter = 0
            if total_pillars == 0:
                active_objects[1] = pillar

        # Update
        all_sprites.update()

        # Check for collisions
        hit_pillar = pillar_collision(bird, pillars)

        # Check if the bird passed a pillar
        for i, pillar in enumerate(pillars):
            if bird.rect.left > pillar.rect.right and not pillar.passed:
                pillar.passed = True
                bird.score += 1
                pillar_list = pillars.sprites()
                active_objects[1] = pillar_list[i + 1]
            if pillar.rect.x < 0 - 30:
                pillars.remove(pillar)
                all_sprites.remove(pillar)

        # Draw
        screen.fill((100, 100, 100))
        all_sprites.draw(screen)
        draw_text(screen, f'Score: {bird.score}', 24, WIDTH // 2, 10)
        pygame.display.flip()

        if not (0 < bird.rect.y < HEIGHT) or hit_pillar:
            bird.image.fill(RED)
            screen.fill((100, 100, 100))
            all_sprites.draw(screen)
            draw_text(screen, f'Score: {bird.score}', 24, WIDTH // 2, 10)
            pygame.display.flip()
            pygame.time.delay(300)
            break


        # print("Gap bottom: ", active_objects[1].gap_bottom, "\tGap top: ", active_objects[1].gap_top, "\tX pos: ", active_objects[1].x_pos, "\tBird x: ", active_objects[0].x)
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
