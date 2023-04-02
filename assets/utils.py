import pygame as pg
from assets import paths

pg.font.init()

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
def get_font(size):
    return pg.font.Font(paths.MAIN_FONT, size)


# Labels presets
def label_creation(text, size, color, pos, alignment="center"):
    label = get_font(size).render(text, True, color)
    rect = label.get_rect()
    setattr(rect, alignment, pos)
    return label, rect


def header(text, pos=(640, 85)):
    return label_creation(text, 70, MAIN_CLR, pos)


def subhead(text, size=30, pos=(640, 135)):
    return label_creation(text, size, SECONDARY_CLR, pos)


def keyboard_key(text, color, pos):
    return label_creation(text, 12, color, pos.center)


def attribute_header(text, color, pos, size):
    return label_creation(text, size, color, pos, "topleft")
