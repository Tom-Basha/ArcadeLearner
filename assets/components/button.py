import pygame

from assets.paths import *
from assets.utils import *


class Button:
    def __init__(self, pos, text, font, color, hover_color=None, outline=False, bg=paths.BUTTON_BG):
        self.image = pg.image.load(bg) if bg != False else None
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = color
        self.hovering_color = hover_color if hover_color != None else color
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        if outline:
            self.outline = font.render(text, True, BLACK)
            self.outline_pos = (self.text_rect.x + 2, self.text_rect.y + 3)
        else:
            self.outline = None

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        if self.outline is not None:
            screen.blit(self.outline, self.outline_pos)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# presets
def back_btn(text="RETURN"):
    return Button((640, 640), text, get_font(55), MAIN_CLR, SECONDARY_CLR, bg=False)


def manu_btn(text, pos):
    return Button(pos, text, get_font(25), WHITE, "#f0000f", outline=True)


# auto games buttons
def buttons_position(i, buttons_count):
    button_width = 340
    button_height = 143
    x_gap = 30
    y_gap = 10
    max_buttons_per_row = 3

    row = i // max_buttons_per_row
    col = i % max_buttons_per_row

    buttons_on_row = min(buttons_count - row * max_buttons_per_row, max_buttons_per_row)
    total_width = buttons_on_row * button_width + (buttons_on_row - 1) * x_gap
    x_start = (SCREEN_W - total_width) // 2
    y_start = 250

    x_pos = x_start + col * (button_width + x_gap) + button_width // 2
    y_pos = y_start + row * (button_height + y_gap) + button_height // 2

    return x_pos, y_pos


def games_buttons(games_list):
    buttons = []

    for i, (file_name, file_path) in enumerate(games_list):
        text_pos = buttons_position(i, len(games_list))
        button = manu_btn(file_name, text_pos)
        buttons.append(button)

    return buttons


def training_btn(pos, text):
    return Button(pos, text, get_font(28, paths.TRAIN_FONT), BLACK, MAIN_CLR, bg=paths.TRAINING_BTN)
