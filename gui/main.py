import sys
import key_selection as ks
from assets.button import *

pg.init()

SCREEN = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu")

BACKGROUND = pg.image.load(paths.BACKGROUND_IMAGE)
selected_keys = {}


def play():
    # Irrelevant at the moment
    return

    # while True:
    #    PLAY_MOUSE_POS = pg.mouse.get_pos()
#
    #    SCREEN.fill("black")
#
    #    PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
    #    PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
    #    SCREEN.blit(PLAY_TEXT, PLAY_RECT)
#
    #    PLAY_BACK = Button(bg=None, pos=(640, 460),
    #                       text="BACK", font=get_font(75), color="White", hover_color="Green")
#
    #    PLAY_BACK.change_color(PLAY_MOUSE_POS)
    #    PLAY_BACK.update(SCREEN)
#
    #    for event in pg.event.get():
    #        if event.type == pg.QUIT:
    #            pg.quit()
    #            sys.exit()
    #        if event.type == pg.MOUSEBUTTONDOWN:
    #            if PLAY_BACK.check_input(PLAY_MOUSE_POS):
    #                main_menu()
#
    #    pg.display.update()


def selected_game(game):
    global selected_keys
    selected_keys = {}
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))
        pg.display.set_caption(game)

        MENU_MOUSE_POS = pg.mouse.get_pos()

        HEADER, HEADER_RECT = header(game)
        SCREEN.blit(HEADER, HEADER_RECT)

        PLAY_BUTTON = manu_btn("Play", (230, 250))
        WATCH_BUTTON = manu_btn("Watch AI", (640, 250))
        TRAIN_BUTTON = manu_btn("Train AI", (1050, 250))
        OPTIONS_BUTTON = manu_btn("Controls", (430, 420))
        FEATURES_BUTTON = manu_btn("Attributes", (840, 420))
        PLAY_BACK = back_btn()

        for button in [PLAY_BUTTON, WATCH_BUTTON, TRAIN_BUTTON, OPTIONS_BUTTON, FEATURES_BUTTON, PLAY_BACK]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_input(MENU_MOUSE_POS):
                    WIP()
                if WATCH_BUTTON.check_input(MENU_MOUSE_POS):
                    WIP()
                if TRAIN_BUTTON.check_input(MENU_MOUSE_POS):
                    WIP()
                if OPTIONS_BUTTON.check_input(MENU_MOUSE_POS):
                    selected_keys = ks.key_selection(selected_keys)
                if FEATURES_BUTTON.check_input(MENU_MOUSE_POS):
                    # attributs = extract_features('game.py')
                    WIP()
                if PLAY_BACK.check_input(MENU_MOUSE_POS):
                    main_menu()

        pg.display.update()


# Delete WIP after initiating **ALL** buttons functions
def WIP():
    BG = pg.image.load(BACKGROUND_IMAGE)

    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT, OPTIONS_RECT = subhead("WORK IN PROGRESS", pos=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = back_btn()
        OPTIONS_BACK.change_color(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.check_input(OPTIONS_MOUSE_POS):
                    return

        pg.display.update()


def main_menu():
    while True:
        # Init screen
        pg.display.set_caption("Generic Arcade AI")
        SCREEN.blit(BACKGROUND, (0, 0))

        # Set mouse
        MENU_MOUSE_POS = pg.mouse.get_pos()

        # Labels
        MENU_TEXT, MENU_RECT = header("Generic Arcade AI")
        SECOND_MENU, SECOND_MENU_RECT = subhead("Pick Your Game of Choice", pos=(640, 270))

        # Game selection
        # A function with auto game detection will replace this sector
        Game1 = manu_btn("Breakout", (230, 400))
        Game2 = manu_btn("Snake", (640, 400))
        Game3 = manu_btn("DonkeyKong", (1050, 400))

        QUIT_BUTTON = quit_btn()

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(SECOND_MENU, SECOND_MENU_RECT)

        for button in [Game1, Game2, Game3, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if Game1.check_input(MENU_MOUSE_POS):
                    selected_game("Breakout")
                if Game2.check_input(MENU_MOUSE_POS):
                    selected_game("Snake")
                if Game3.check_input(MENU_MOUSE_POS):
                    selected_game("Donkey Kong")
                if QUIT_BUTTON.check_input(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        pg.display.update()


main_menu()
