import sys
from assets.components.button import *
from assets.utils import *
from assets.paths import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Settings")
font = pygame.font.Font(None, 24)


# Slider class
class Slider:

    def __init__(self, x, y, width, min_val, max_val, jump, curr_value=-1, pop_size=50, fitness_threshold=250,
                 hidden_layers=4):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10
        self.min_val = min_val
        self.max_val = max_val
        self.top_margin = 200
        self.bottom_margin = 150
        self.list_height = 0
        self.list_window = SCREEN_H - self.top_margin - self.bottom_margin
        self.pop_size = pop_size  # initial value for population
        self.fitness_threshold = fitness_threshold  # initial value for threshold
        self.hidden_layers = hidden_layers  # initial value for threshold
        self.slider_pos = x
        self.slider_width = 20
        self.slider_height = 20
        self.value = curr_value if curr_value != -1 else min_val
        self.jump = jump
        self.dragging = False

        #  Scrollbar settings
        self.scrollbar_width = 20
        self.scrollbar_x = SCREEN_W
        self.scrollbar_y = 0
        self.scrollbar_height = 0
        if self.list_height > self.list_window:
            self.scrollbar_height = self.list_window * self.list_window / self.list_height
            self.scrollbar_x = SCREEN_W - self.scrollbar_width - 10
        self.min_offset = -self.list_height + SCREEN_H - self.top_margin - self.bottom_margin
        self.max_offset = 0
        self.scroll_offset = 0
        self.scrollbar_position = 0
        self.scroll_speed = 30

        # Set the initial position of the slider based on the current value
        if curr_value != -1:
            self.slider_pos = max(self.x, min(self.x + (self.width - self.slider_width) * self.value / self.max_val,
                                              self.x + self.width - self.slider_width))

    def update(self, scroll_offset):
        ratio = (scroll_offset - self.max_offset) / (self.min_offset - self.max_offset)
        self.scrollbar_position = ratio * (
                SCREEN_H - self.scrollbar_height - self.top_margin - self.bottom_margin) + self.top_margin

    def draw(self, screen):
        # Draw the slider bar
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, GREEN, (self.slider_pos, self.y - 5, self.slider_width, self.slider_height),
                         border_radius=15)
        pygame.draw.rect(screen, MAIN_CLR,
                         (self.scrollbar_x, self.top_margin, self.scrollbar_width, self.list_window), border_radius=10)

        # Draw the marks
        mark_step = max(self.jump, (self.max_val - self.min_val) // 10)
        offset = 10
        intervals = (self.max_val - self.min_val) // self.jump
        show_every_other = intervals > 10

        for i in range(intervals + 1):
            if show_every_other and i % 2 != 0:
                continue
            value = self.min_val + i * self.jump
            mark_text = font.render(str(value), True, WHITE)
            mark_rect = mark_text.get_rect(
                center=(self.x + offset + i * (self.width - 2 * offset) // intervals, self.y - 20))
            screen.blit(mark_text, mark_rect)

        # Draw the value text
        value_text = font.render(f"Value: {self.value}", True, WHITE)
        text_rect = value_text.get_rect(center=(self.x + self.width // 2, self.y + 50))
        screen.blit(value_text, text_rect)

        # Draw values on screen
        pop_text = font.render("Choose the population size: ", True, (255, 255, 255))
        thresh_text = font.render("Choose the fitness threshold: ", True, (255, 255, 255))
        hid_text = font.render("Choose the hidden layers: ", True, (255, 255, 255))
        screen.blit(pop_text, (50, 200))
        screen.blit(thresh_text, (50, 350))
        screen.blit(hid_text, (50, 500))

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
            (self.slider_pos - self.x) * (self.max_val - self.min_val) / (
                    self.width - self.slider_width) / self.jump) * self.jump
        self.value = max(self.min_val, min(self.value + self.min_val, self.max_val))
        if self == slider:
            self.pop_size = self.value
        if self == slider1:
            self.fitness_threshold = self.value
        if self == slider2:
            self.hidden_layers = self.value

    def handle_scrollbar(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * self.scroll_speed
            self.scroll_offset = min(max(self.scroll_offset, self.min_offset), self.max_offset)


# Create a slider
slider = Slider(430, 200, 400, 10, 30, 100, 5, 50)
slider1 = Slider(430, 350, 400, 10, 100, 1000, 50, 250)
slider2 = Slider(430, 500, 400, 10, 1, 5, 1, 4)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        slider.handle_event(event)
        slider1.handle_event(event)
        slider2.handle_event(event)

    MENU_MOUSE_POS = pg.mouse.get_pos()

    BACK_BTN = back_btn()
    BACK_BTN.change_color(MENU_MOUSE_POS)

    BG = pygame.image.load(BACKGROUND_IMAGE)
    screen.blit(BG, (0, 0))


    BACK_BTN.update(screen)
    HEADER, HEADER_RECT = header("SETTINGS")
    SUBHEAD, SUBHEAD_RECT = subhead("SELECT THE RELEVANT VALUES FOR THE AI LEARNING PROCESS", 16)
    screen.blit(HEADER, HEADER_RECT)
    screen.blit(SUBHEAD, SUBHEAD_RECT)

    slider.draw(screen)
    slider1.draw(screen)
    slider2.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
