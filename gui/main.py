import os
import subprocess

from assets.components.button import *
from attribute_selection import *

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import key_selection as ks
from agents.NEAT.train import Trainer
from agents.NEAT.watch_ai import AI_Player

from assets.extractors import *
from assets.error import *

pg.init()

SCREEN = pg.display.set_mode((SCREEN_W, SCREEN_H))
pg.display.set_caption("Menu")

BACKGROUND = pg.image.load(paths.BACKGROUND_IMAGE)
selected_keys = {}
selected_attributes = {}


def selected_game(game, path):
    global selected_keys, selected_attributes
    game_path = path
    selected_keys = keys_extractor(game_path)

    PLAY_BTN = manu_btn("Play", (270, 280))
    WATCH_BTN = manu_btn("Watch AI", (640, 280))
    TRAIN_BTN = manu_btn("Train AI", (1010, 280))
    CONTROLS_BTN = manu_btn("Controls", (450, 440))
    ATTRIBUTES_BTN = manu_btn("Attributes", (820, 440))
    PLAY_BACK = back_btn()

    game_attributes = attribute_extractor(game_path)
    selected_attributes = match_attributes(game_attributes)

    print(selected_attributes)
    # selected_attributes = {'PacMan': ['position', 'map'], 'Ghost': ['position']}
    # selected_attributes = {'Snake': ['rect.center'], 'Food': ['rect.center']}
    # selected_attributes = {'Bird': ['rect.center'], 'Pillar': ['x_pos', 'gap_top', 'gap_bottom']}
    # selected_attributes = {'Player': ['rect.center'], 'Ball': ['rect.center']}

    while True:
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
                    ai_player = AI_Player(game, path, selected_attributes, selected_keys)
                    trained = ai_player.neat_setup()
                    if not trained:
                        error_msg(['Trained AI was not found.', 'Make sure to train your AI first.'])
                if TRAIN_BTN.check_input(MENU_MOUSE_POS):
                    print(f"\nSetting up training for {game}.\nSelected keys: {selected_keys}\nSelected attributes: {selected_attributes}")

                    trainer = Trainer(game, path, selected_attributes, selected_keys)
                    trainer.neat_setup()

                if CONTROLS_BTN.check_input(MENU_MOUSE_POS):
                    selected_keys = ks.key_selection(selected_keys)
                if ATTRIBUTES_BTN.check_input(MENU_MOUSE_POS):
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
