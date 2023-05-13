import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import subprocess
import sys
import key_selection as ks
from agents.NEAT.train import Trainer
from agents.NEAT.watch_ai import AI_Player
from assets.components.button import *
from assets.error import error_msg
from assets.extractors import *
from attribute_selection import *
from train_setting import *

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
BACKGROUND = pygame.image.load(BACKGROUND_IMAGE)

selected_keys = {}
selected_attributes = {}


def selected_game(game, path):
    global selected_keys, selected_attributes
    game_path = path
    selected_keys = keys_extractor(game_path)

    threshold = 250
    population = 50
    generations = 10000
    start_gen = -1
    hidden_layers = 3

    HEADER, HEADER_RECT = header(game)

    PLAY_BTN = manu_btn("Play", (270, 280))
    WATCH_BTN = manu_btn("Watch AI", (640, 280))
    TRAIN_BTN = manu_btn("Train AI", (1010, 280))
    CONTROLS_BTN = manu_btn("Controls", (270, 440))
    ATTRIBUTES_BTN = manu_btn("Attributes", (640, 440))
    SETTINGS = manu_btn("Settings", (1010, 440))
    BACK = back_btn()

    buttons = [PLAY_BTN, WATCH_BTN, TRAIN_BTN, CONTROLS_BTN, ATTRIBUTES_BTN, BACK, SETTINGS]

    game_attributes = attribute_extractor(game_path)
    selected_attributes = match_attributes(game_attributes)

    while True:
        pygame.display.set_caption(game)
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(HEADER, HEADER_RECT)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for button in buttons:
            button.change_color(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PLAY_BTN.check_input(MENU_MOUSE_POS):
                    subprocess.run(["python", game_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

                if WATCH_BTN.check_input(MENU_MOUSE_POS):
                    ai_player = AI_Player(game, path, selected_attributes, selected_keys)
                    trained = ai_player.neat_setup()
                    if not trained:
                        error_msg(['Trained AI was not found.', 'Make sure to train your AI first.'])

                if TRAIN_BTN.check_input(MENU_MOUSE_POS):
                    print(
                        f"\nSetting up training for {game}.\nSelected keys: {selected_keys}\nSelected attributes: {selected_attributes}")
                    trainer = Trainer(game, path, selected_attributes, selected_keys, threshold, generations, population, start_gen, hidden_layers)
                    trainer.neat_setup()

                if CONTROLS_BTN.check_input(MENU_MOUSE_POS):
                    selected_keys = ks.key_selection(selected_keys)

                if ATTRIBUTES_BTN.check_input(MENU_MOUSE_POS):
                    selected_attributes = attribute_selection(game_attributes, selected_attributes)

                if SETTINGS.check_input(MENU_MOUSE_POS):
                    threshold, generations, population, start_gen, hidden_layers = train_setting(game, threshold, generations, population, start_gen, hidden_layers)

                if BACK.check_input(MENU_MOUSE_POS):
                    return

        pygame.display.update()
