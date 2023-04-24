import random
import pygame


pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 12
        self.velocity = 0
        self.color = (0, 255, 0)  # green color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self, dt):
        self.velocity += 0.5 * dt
        self.y += int(self.velocity * dt)

    def jump(self):
        self.velocity = -10


class Pillar:
    def __init__(self, x, gap_size, screen_height):
        self.x = x
        self.gap_size = gap_size
        self.screen_height = screen_height
        self.width = 40
        self.color = (150, 150, 150)
        self.top_rect = pygame.Rect(self.x, 0, self.width, random.randint(50, self.screen_height - self.gap_size - 50))
        self.bottom_rect = pygame.Rect(self.x, self.top_rect.bottom + self.gap_size, self.width,
                                       self.screen_height - self.top_rect.height - self.gap_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)

    def update(self, dt, speed):
        self.x -= int(speed * dt)
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def offscreen(self):
        return self.x < -self.width
