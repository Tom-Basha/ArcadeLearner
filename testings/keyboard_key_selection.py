import pygame
import pygame.gfxdraw
from assets.button import *
from assets.paths import *


class KeySelection:
    def __init__(self, keys):
        # Define some constants for the colors and sizes of the keys
        self.KEY_WIDTH = 50
        self.KEY_HEIGHT = 50
        self.KEY_MARGIN = 1

        self.curr_x = 183
        self.curr_y = 200

        # Create a Pygame window
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Controls")

        # Create a dictionary of key labels and their rectangles
        self.key_rects = {}
        self.row_1 = "1234567890"
        self.row_2 = "QWERTYUIOP"
        self.row_3 = "ASDFGHJKL"
        self.row_4 = "ZXCVBNM"

        self.clicked_keys = keys

        def draw_key(key, disp_name, w_add):
            rect = pygame.Rect(self.curr_x, self.curr_y, self.KEY_WIDTH + w_add, self.KEY_HEIGHT)
            self.curr_x += self.KEY_WIDTH + w_add
            self.key_rects[key] = rect, disp_name

        def draw_row(row):
            for i, key in enumerate(row):
                key_name = key.lower()
                draw_key(key_name, key, 0)

        def next_row():
            self.curr_y += self.KEY_HEIGHT + self.KEY_MARGIN
            self.curr_x = 183

        # esc row
        draw_key('escape', 'ESC', 0)
        self.curr_x += 45
        draw_key('F1', 'F1', 0)
        draw_key('F2', 'F2', 0)
        draw_key('F3', 'F3', 0)
        draw_key('F4', 'F4', 0)
        self.curr_x += 25
        draw_key('F5', 'F5', 0)
        draw_key('F6', 'F6', 0)
        draw_key('F7', 'F7', 0)
        draw_key('F8', 'F8', 0)
        self.curr_x += 25
        draw_key('F9', 'F9', 0)
        draw_key('F10', 'F10', 0)
        draw_key('F11', 'F11', 0)
        draw_key('F12', 'F12', 0)
        self.curr_y += 30
        next_row()

        # numbers row
        draw_key('`', '`', 0)
        draw_row(self.row_1)
        draw_key('-', '-', 0)
        draw_key('=', '=', 0)
        draw_key('backspace', '\u2190', 45)
        self.curr_x += 20
        draw_key('insert', 'Ins', 0)
        draw_key('home', 'Home', 0)
        draw_key('pageup', 'Pg\u2191', 0)
        next_row()

        # tab row
        draw_key('tab', 'TAB', 20)
        draw_row(self.row_2)
        draw_key('[', '[', 0)
        draw_key(']', ']', 0)
        draw_key('\\', '\\', 25)
        self.curr_x += 20
        draw_key('delete', 'Del', 0)
        draw_key('end', 'End', 0)
        draw_key('pagedown', 'Pg\u2193', 0)
        next_row()

        # caps row
        draw_key('capslock', 'CAPS', 30)
        draw_row(self.row_3)
        draw_key(';', ';', 0)
        draw_key('\'', '\'', 0)
        draw_key('enter', 'ENTER', 65)
        next_row()

        # shift row
        draw_key('leftshift', 'SHIFT', 50)
        draw_row(self.row_4)
        draw_key(',', ',', 0)
        draw_key('.', '.', 0)
        draw_key('/', '/', 0)
        draw_key('rightshift', 'SHIFT', 95)
        self.curr_x += 70
        draw_key('up', '\u2191', 0)
        next_row()

        # ctrl row
        draw_key('leftctrl', 'CTRL', 20)
        draw_key('leftmeta', 'WIN', 0)
        draw_key('leftalt', 'ALT', 10)
        draw_key('space', '', 270)
        draw_key('rightalt', 'ALT', 15)
        draw_key('rightmeta', 'FN', 0)
        draw_key('menu', 'OPT', 0)
        draw_key('rightctrl', 'CTRL', 30)
        self.curr_x += 20
        draw_key('left', '\u2190', 0)
        draw_key('down', '\u2193', 0)
        draw_key('right', '\u2192', 0)

    def draw_keyboard(self):
        keyboard_boarder = pygame.Rect(165, 180, 950, 370)
        pygame.draw.rect(SCREEN, WHITE, keyboard_boarder, 2, border_radius=15)
        # Draw the keys
        for key, (rect, disp_name) in self.key_rects.items():
            # Draw the key's top surface
            key_color = GREEN if key in clicked_keys else WHITE
            pygame.gfxdraw.box(SCREEN, rect, key_color)

            # Draw the key's border
            border_rect = rect.inflate(-1, -1)
            pygame.draw.rect(SCREEN, key_color, border_rect, 3, border_radius=10)

            # Draw the key label
            key_label, key_rect = keyboard_key(disp_name, key_color, rect)
            SCREEN.blit(key_label, key_rect)

    def handle_click(self, pos):
        # Check if the click is inside a key's rectangle
        for key, (rect, disp_name) in self.key_rects.items():
            if rect.collidepoint(pos):
                # Toggle the key's color and add/remove it from clicked_keys
                if key in clicked_keys:
                    clicked_keys.remove(key)
                else:
                    clicked_keys.add(key)
                # Print the selected keys
                if len(clicked_keys) == 0:
                    print('{}')
                else:
                    print("Selected keys: ", clicked_keys)
                    print("Selected keys amount: ", len(clicked_keys))

                return


def key_selection(keys):
    global clicked_keys, SCREEN
    ks = KeySelection(keys)
    SCREEN = ks.screen
    BG = pygame.image.load(BACKGROUND_IMAGE)

    # Create a set to store the clicked keys
    if len(keys) == 0:
        keys = {'space', 'up', 'down', 'right', 'left'}
    if "escape" in keys:
        keys.remove("escape")
    clicked_keys = keys

    HEADER, HEADER_RECT = header("CONTROLS")
    SUBHEAD, SUBHEAD_RECT = subhead("SELECT THE RELEVANT KEYS FOR YOUR GAME", 16)

    # Start the main game loop
    while True:
        MENU_MOUSE_POS = pg.mouse.get_pos()

        BACK_BTN = back_btn()
        BACK_BTN.change_color(MENU_MOUSE_POS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return clicked_keys
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ks.handle_click(MENU_MOUSE_POS)

                if BACK_BTN.check_input(MENU_MOUSE_POS):
                    return clicked_keys

        # Draw the keyboard and update the display
        SCREEN.blit(BG, (0, 0))

        BACK_BTN.update(SCREEN)
        SCREEN.blit(HEADER, HEADER_RECT)
        SCREEN.blit(SUBHEAD, SUBHEAD_RECT)

        ks.draw_keyboard()

        pygame.display.flip()

