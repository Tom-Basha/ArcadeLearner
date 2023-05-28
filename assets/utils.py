import pygame
from assets import paths

pygame.font.init()

# Colors Presets
MAIN_CLR = "#b68f40"
ERROR_CLR = "#ff0000"
ERROR2_CLR = "#aa0000"
SECONDARY_CLR = "#f6fcd4"
WHITE = (255, 255, 255, 0)
BLACK = (0, 0, 0, 0)
GREEN = (0, 255, 0, 0)

# Measurements
SCREEN_W = 1280
SCREEN_H = 720


# Set up font
def get_font(size, font=paths.MAIN_FONT):
    return pygame.font.Font(font, size)


# Labels presets
def label_creation(text, size, color, pos, alignment="center"):
    label = get_font(size).render(text, True, color)
    rect = label.get_rect()
    setattr(rect, alignment, pos)
    return label, rect


def header(text, pos=(640, 85), color=MAIN_CLR):
    return label_creation(text, 70, color, pos)


def subhead(text, size=30, pos=(640, 135), color=SECONDARY_CLR):
    return label_creation(text, size, color, pos)


def keyboard_key(text, color, pos):
    return label_creation(text, 12, color, pos.center)


def attribute_header(text, color, pos, size):
    return label_creation(text, size, color, pos, "topleft")


def train_info(text, pos, alignment="center", size=40):
    font = pygame.font.Font(paths.TRAIN_FONT, size)
    label = font.render(text, True, WHITE)
    rect = label.get_rect()
    setattr(rect, alignment, pos)
    return label, rect
