import os
from assets.components.button import *
from assets.paths import *
from gui.game_options import selected_game

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from assets.extractors import *
from assets.error import *

pg.init()

SCREEN = pg.display.set_mode((SCREEN_W, SCREEN_H))
pg.display.set_caption("Menu")
BACKGROUND = pygame.image.load(BACKGROUND_IMAGE)

def main_menu():
    games_list = games_extractor()
    buttons = games_buttons(games_list)
    QUIT_BUTTON = back_btn("QUIT")
    while True:
        # Init screen
        pg.display.set_caption("Generic Arcade AI")
        SCREEN.blit(BACKGROUND, (0, 0))

        # Set mouse
        MENU_MOUSE_POS = pg.mouse.get_pos()

        # Labels
        MENU_TEXT, MENU_RECT = header("Generic Arcade AI")
        SECOND_MENU, SECOND_MENU_RECT = subhead("Pick Your Game of Choice", pos=(640, 150))

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(SECOND_MENU, SECOND_MENU_RECT)

        for button in [QUIT_BUTTON] + buttons:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button:
                for i, button in enumerate(buttons):
                    if button.check_input(MENU_MOUSE_POS):
                        selected_game(games_list[i][0], games_list[i][1])
                if QUIT_BUTTON.check_input(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        pg.display.update()


main_menu()
