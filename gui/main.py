import os
import sys
import key_selection as ks
from button import Button
import pygame as pg
from assets import paths

pg.init()

SCREEN = pg.display.set_mode((1280, 720))
pg.display.set_caption("Menu")

BACKGROUND = pg.image.load(paths.BACKGROUND_IMAGE)
selected_keys = {}


def play():
    while True:
        PLAY_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pg.display.update()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pg.font.Font(paths.MAIN_FONT, size)


def selected_game(game):
    global selected_keys
    selected_keys = {}
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))
        pg.display.set_caption(game)

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(70).render(game, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(pos=(230, 250),
                             text_input="Play The Game", font=get_font(26), base_color="#d7fcd4",
                             hovering_color="White")
        WATCH_BUTTON = Button(pos=(640, 250),
                              text_input="Watch Train AI", font=get_font(26), base_color="#d7fcd4",
                              hovering_color="White")
        TRAIN_BUTTON = Button(pos=(1050, 250),
                              text_input="Train AI", font=get_font(26), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(pos=(310, 420),
                                text_input="Controls", font=get_font(35), base_color="#d7fcd4",
                                hovering_color="White")
        FEATURES_BUTTON = Button(pos=(960, 420),
                                 text_input="Attributes", font=get_font(35), base_color="#d7fcd4",
                                 hovering_color="White")
        PLAY_BACK = Button(image=pg.image.load(paths.QUIT_BG), pos=(640, 580),
                           text_input="BACK", font=get_font(55), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, WATCH_BUTTON, TRAIN_BUTTON, OPTIONS_BUTTON, FEATURES_BUTTON, PLAY_BACK]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    WIP()
                if WATCH_BUTTON.checkForInput(MENU_MOUSE_POS):
                    WIP()
                if TRAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    WIP()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_keys = ks.key_selection(selected_keys)
                if FEATURES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # attributs = extract_features('game.py')
                    print("ATT")
                if PLAY_BACK.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pg.display.update()


def WIP():
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("WORK IN PROGRESS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return

        pg.display.update()


def main_menu():
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(70).render("Generic Arcade AI", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SECOND_MENU = get_font(30).render("Pick Your Game of Choice", True, "#f6fcd4")
        SECOND_MENU_RECT = SECOND_MENU.get_rect(center=(640, 185))

        Game1 = Button(pos=(230, 300), text_input="Breakout", font=get_font(26), base_color="#d7fcd4", hovering_color="White")
        Game2 = Button(pos=(640, 300), text_input="Snake", font=get_font(26), base_color="#d7fcd4", hovering_color="White")
        Game3 = Button(pos=(1050, 300), text_input="Donkey Kong", font=get_font(26), base_color="#d7fcd4",
                       hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 640), text_input="QUIT", font=get_font(55), base_color="#b68f40",
                             hovering_color="#f6fcd4")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(SECOND_MENU, SECOND_MENU_RECT)

        for button in [Game1, Game2, Game3, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if Game1.checkForInput(MENU_MOUSE_POS):
                    selected_game("Breakout")
                if Game2.checkForInput(MENU_MOUSE_POS):
                    selected_game("Snake")
                if Game3.checkForInput(MENU_MOUSE_POS):
                    selected_game("Donkey Kong")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        pg.display.update()


main_menu()
