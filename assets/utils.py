import pygame as pg
from assets import paths

pg.font.init()

# Colors Presets
MAIN_CLR = "#b68f40"
SECONDARY_CLR = "#f6fcd4"
WHITE = (255, 255, 255, 0)
GREEN = (0, 255, 0, 0)


# Set up font
def get_font(size):
    return pg.font.Font(paths.MAIN_FONT, size)


# Labels presets
def header(text, pos=(640, 85)):
    label = get_font(70).render(text, True, MAIN_CLR)
    rect = label.get_rect(center=pos)
    return label, rect


def subhead(text, size=30, pos=(640, 135)):
    label = get_font(size).render(text, True, SECONDARY_CLR)
    rect = label.get_rect(center=pos)
    return label, rect


def keyboard_key(text, color, pos):
    label = get_font(12).render(text, True, color)
    rect = label.get_rect(center=pos.center)
    return label, rect

