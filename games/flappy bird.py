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


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.rect.center = (self.x, self.y)
        self.velocity = 0
        self.score = 0

    def update(self):
        self.velocity -= 0.5
        self.y -= self.velocity
        self.rect.y -= self.velocity

    def flap(self):
        self.velocity = +10


class Pillar(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.gap_space = 200
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
        self.x_pos = -3
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    try:
        s.connect(('localhost', 8888))
        instructions = pickle.loads(s.recv(4096))
        # print(f"Requested attributes: {instructions}")
        connected = True
    except ConnectionRefusedError:
        pass

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy")
    clock = pygame.time.Clock()

    bird = Bird()
    all_sprites = pygame.sprite.Group(bird)
    pillars = pygame.sprite.Group()

    active_objects = [bird, Pillar(-30), Pillar(-30), Pillar(-30)]

    pillar_spawn_counter = 0
    total_pillars = 0
    spawn_target = 350 // 3  # Dividing by the pillar speed (3) to get the required number of frames

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Spawn pillars
        pillar_spawn_counter += 1
        if pillar_spawn_counter == spawn_target:
            total_pillars += 1
            pillar = Pillar(WIDTH)
            all_sprites.add(pillar)
            active_objects[total_pillars % 3 + 1] = pillar
            pillars.add(pillar)
            pillar_spawn_counter = 0

        # Update
        all_sprites.update()

        # Check for collisions
        hit_pillar = pillar_collision(bird, pillars)

        # Check if the bird passed a pillar
        for pillar in pillars:
            if bird.rect.left > pillar.rect.right and not pillar.passed:
                pillar.passed = True
                bird.score += 1
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

        clock.tick(0)

        if connected:
            data = []
            for class_name, attributes in instructions.items():
                obj = next((o for o in active_objects if o.__class__.__name__ == class_name), None)
                if obj is not None:
                    for attr in attributes:
                        if hasattr(obj, attr):
                            data.append((attr, str(getattr(obj, attr))))

            print(data)

            s.sendall(pickle.dumps(data))
            action = s.recv(4096)
            action = pickle.loads(action)
            if action != 0:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=eval(action)))
            time.sleep(0.001)

    s.close()
    return


if __name__ == "__main__":
    main()
