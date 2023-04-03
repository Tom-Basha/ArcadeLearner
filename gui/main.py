import key_selection as ks
from attribute_selection import *
from games import snake
from assets.extractors import *
from assets.error import *

pg.init()

SCREEN = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu")

BACKGROUND = pg.image.load(paths.BACKGROUND_IMAGE)
selected_keys = {}



def play():
    # Irrelevant at the moment
    return


def selected_game(game, path):
    global selected_keys, selected_attributes
    game_path = path
    selected_keys = {}
    selected_attributes = set()

    PLAY_BTN = manu_btn("Play", (270, 280))
    WATCH_BTN = manu_btn("Watch AI", (640, 280))
    TRAIN_BTN = manu_btn("Train AI", (1010, 280))
    CONTROLS_BTN = manu_btn("Controls", (450, 440))
    ATTRIBUTES_BTN = manu_btn("Attributes", (820, 440))
    PLAY_BACK = back_btn()

    while True:
        SCREEN = pg.display.set_mode((1280, 720))
        pg.display.set_caption(game)
        SCREEN.blit(BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        HEADER, HEADER_RECT = header(game)
        SCREEN.blit(HEADER, HEADER_RECT)

        for button in [PLAY_BTN, WATCH_BTN, TRAIN_BTN, CONTROLS_BTN, ATTRIBUTES_BTN, PLAY_BACK]:
            button.change_color(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if PLAY_BTN.check_input(MENU_MOUSE_POS):
                    try:
                        with open(game_path, 'r') as f:
                            code = f.read()
                            exec(code, globals())
                    except Exception as e:
                        pg.display.set_mode((1280, 720))
                        error_msg(f"Error while running {game_path}: {e}")

                if WATCH_BTN.check_input(MENU_MOUSE_POS):
                    error_msg("PAGE NOT FOUND: WORK IN PROGRESS")

                    # PLACEHOLDER - AI WATCH

                if TRAIN_BTN.check_input(MENU_MOUSE_POS):
                    error_msg("PAGE NOT FOUND: WORK IN PROGRESS")

                    # PLACEHOLDER - AI train

                if CONTROLS_BTN.check_input(MENU_MOUSE_POS):
                    if len(selected_keys) == 0:
                        selected_keys = keys_extractor(game_path)
                    selected_keys = ks.key_selection(selected_keys)
                if ATTRIBUTES_BTN.check_input(MENU_MOUSE_POS):
                    game_attributes = attribute_extractor(game_path)

                    # PLACEHOLDER - function that automatically select attributes

                    selected_attributes = attribute_selection(game_attributes, selected_attributes)
                if PLAY_BACK.check_input(MENU_MOUSE_POS):
                    main_menu()

        pg.display.update()


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
