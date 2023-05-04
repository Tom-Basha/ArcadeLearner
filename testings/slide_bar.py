import pygame
import sys

# Initialize Pygame
pygame.init()


# Slider class
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, jump, curr_value=-1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.slider_pos = x
        self.slider_width = 20
        self.slider_height = 20
        self.value = curr_value if curr_value != -1 else min_val
        self.jump = jump
        self.dragging = False

        # Set the initial position of the slider based on the current value
        if curr_value != -1:
            self.slider_pos = max(self.x, min(self.x + (self.width - self.slider_width) * self.value / self.max_val, self.x + self.width - self.slider_width))

    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (50, 50, 50), (self.slider_pos, self.y - 5, self.slider_width, self.slider_height),
                         border_radius=15)

        # Draw the marks
        font = pygame.font.SysFont(None, 24)
        mark_step = max(self.jump, (self.max_val - self.min_val) // 10)
        offset = 10
        intervals = (self.max_val - self.min_val) // self.jump
        show_every_other = intervals > 10

        for i in range(intervals + 1):
            if show_every_other and i % 2 != 0:
                continue
            value = self.min_val + i * self.jump
            mark_text = font.render(str(value), True, (0, 0, 0))
            mark_rect = mark_text.get_rect(
                center=(self.x + offset + i * (self.width - 2 * offset) // intervals, self.y - 20))
            screen.blit(mark_text, mark_rect)

        # Draw the value text
        value_text = font.render(f"Value: {self.value}", True, (0, 0, 0))
        text_rect = value_text.get_rect(center=(self.x + self.width // 2, self.y + 50))
        screen.blit(value_text, text_rect)

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


# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slider Example")

# Create a slider
slider = Slider(200, 100, 400, 10, 30, 100, 5, 50)
slider1 = Slider(200, 300, 400, 10, 100, 1000, 50, 250)
slider2 = Slider(200, 500, 400, 10, 1, 5, 1, 4)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        slider.handle_event(event)
        slider1.handle_event(event)
        slider2.handle_event(event)

    screen.fill((255, 255, 255))
    slider.draw(screen)
    slider1.draw(screen)
    slider2.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
