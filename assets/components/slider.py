import pygame
import sys

from assets.utils import *

# Initialize Pygame
pygame.init()


# Slider class
class Slider:
    def __init__(self, x, y, width, min_val, max_val, jump, curr_value=-2):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10
        self.min_val = min_val
        self.max_val = max_val
        self.slider_pos = x
        self.slider_width = 20
        self.slider_height = 20
        self.value = curr_value if curr_value != -2 else min_val
        self.jump = jump
        self.dragging = False

        # Set the initial position of the slider based on the current value
        if curr_value != -1:
            self.slider_pos = max(self.x, min(self.x + (self.width - self.slider_width) * self.value / self.max_val, self.x + self.width - self.slider_width))

    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, MAIN_CLR, (self.slider_pos, self.y - 5, self.slider_width, self.slider_height),
                         border_radius=15)

        # Draw the minimum, maximum and current value
        font = pygame.font.SysFont(None, 24)

        # Draw the minimum value
        min_text = font.render(str(self.min_val), True, WHITE)
        min_rect = min_text.get_rect(center=(self.x - 30, self.y + 5))
        screen.blit(min_text, min_rect)

        # Draw the maximum value
        max_text = font.render(str(self.max_val), True, WHITE)
        max_rect = max_text.get_rect(center=(self.x + self.width + 30, self.y + 5))
        screen.blit(max_text, max_rect)

        # Draw the current value
        value_text = font.render(f"{self.value}", True, WHITE)
        value_rect = value_text.get_rect(center=(self.slider_pos + self.slider_width // 2, self.y + 35))
        screen.blit(value_text, value_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_mouse_on_slider(event.pos):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.update_slider_pos(event.pos)

    def is_mouse_on_slider(self, pos):
        return self.slider_pos <= pos[0] <= self.slider_pos + self.slider_width and self.y <= pos[
            1] <= self.y + self.height

    def update_slider_pos(self, pos):
        self.slider_pos = max(self.x, min(pos[0] - self.slider_width // 2, self.x + self.width - self.slider_width))
        self.value = round(
            (self.slider_pos - self.x) * (self.max_val - self.min_val) / (self.width - self.slider_width) / self.jump) * self.jump
        self.value = max(self.min_val, min(self.value + self.min_val, self.max_val))

