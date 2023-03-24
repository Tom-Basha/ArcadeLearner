import pygame as pg
from assets.utils import *
from assets.paths import *


class Button:
    def __init__(self, pos, text, font, color, hover_color, bg=paths.BUTTON_BG,
                 command=None):
        self.image = pg.image.load(paths.BUTTON_BG) if bg != False else None
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = color, hover_color
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.command = command

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
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

    def do_command(self):
        if self.command:
            self.command()


# presets
def quit_btn():
    return Button((640, 640), "QUIT", get_font(55), MAIN_CLR, SECONDARY_CLR, bg=False)


def back_btn():
    return Button((640, 640), "RETURN", get_font(55), MAIN_CLR, SECONDARY_CLR, bg=False)


def manu_btn(text, pos):
    return Button(pos, text, get_font(30), WHITE, SECONDARY_CLR)
