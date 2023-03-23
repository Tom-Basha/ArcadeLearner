import pygame as pg
from assets import paths

pg.font.init()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font(paths.MAIN_FONT, size)
