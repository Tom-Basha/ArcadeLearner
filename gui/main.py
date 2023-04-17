import key_selection as ks
from agents.NEAT.train import Trainer
from attribute_selection import *
from assets.extractors import *
from assets.error import *
from testings.attribute_value import *

pg.init()

SCREEN = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu")

BACKGROUND = pg.image.load(paths.BACKGROUND_IMAGE)
selected_keys = {}


def selected_game(game, path):
    global selected_keys, selected_attributes
    game_path = path
    selected_keys = keys_extractor(game_path)
    selected_attributes = {}

    PLAY_BTN = manu_btn("Play", (270, 280))
    WATCH_BTN = manu_btn("Watch AI", (640, 280))
    TRAIN_BTN = manu_btn("Train AI", (1010, 280))
    CONTROLS_BTN = manu_btn("Controls", (450, 440))
    ATTRIBUTES_BTN = manu_btn("Attributes", (820, 440))
    PLAY_BACK = back_btn()

    game_attributes = attribute_extractor(game_path)
    # selected_attributes = attributes_extractor(game_attributes)

    selected_attributes = {'Bird': ['score', 'x', 'y'], 'Pillar': ['x_pos', 'bottom_height', 'gap_height']}

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
                    subprocess.run(["python", game_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

                if WATCH_BTN.check_input(MENU_MOUSE_POS):
                    error_msg("PAGE NOT FOUND: WORK IN PROGRESS")

                    # PLACEHOLDER - AI WATCH

                if TRAIN_BTN.check_input(MENU_MOUSE_POS):
                    print(selected_keys)
                    trainer = Trainer(game, path, selected_attributes, selected_keys)
                    trainer.neat_setup()
                    error_msg("PAGE NOT FOUND: WORK IN PROGRESS")

                    # PLACEHOLDER - AI train

                if CONTROLS_BTN.check_input(MENU_MOUSE_POS):
                    selected_keys = ks.key_selection(selected_keys)
                if ATTRIBUTES_BTN.check_input(MENU_MOUSE_POS):

                    # PLACEHOLDER - function that automatically select attributes

                    selected_attributes = attribute_selection(game_attributes, selected_attributes)
                    print(selected_attributes)

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
