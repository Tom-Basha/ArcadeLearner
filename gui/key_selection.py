import pygame
import pygame.gfxdraw
from assets import paths

class KeySelection():
    def __init__(self, keys):
        # Define some constants for the colors and sizes of the keys
        self.button_rect = None
        self.button_text = None
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0, 128)
        self.KEY_WIDTH = 50
        self.KEY_HEIGHT = 50
        self.KEY_MARGIN = 1
        self.KEY_FONT_SIZE = 12
        self.KEY_DEPTH = 10

        self.curr_x = 183
        self.curr_y = 200

        # Initialize Pygame
        # pygame.init()

        # Create a Pygame window
        self.screen = pygame.display.set_mode((1280, 720))
        self.font = pygame.font.Font(paths.MAIN_FONT, self.KEY_FONT_SIZE)

        pygame.display.set_caption("Controls")
        # BG = pygame.image.load("assets/Background.png")
        #
        # # Create a font for the key labels
        # self.font = pygame.font.Font("assets/font.ttf", self.KEY_FONT_SIZE)

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
                key_name = "pygame.K_" + key.lower()
                draw_key(key_name, key, 0)

        def next_row():
            self.curr_y += self.KEY_HEIGHT + self.KEY_MARGIN
            self.curr_x = 183

        # esc row
        draw_key('pygame.K_ESC', 'ESC', 0)
        self.curr_x += 45
        draw_key('pygame.K_F1', 'F1', 0)
        draw_key('pygame.K_F2', 'F2', 0)
        draw_key('pygame.K_F3', 'F3', 0)
        draw_key('pygame.K_F4', 'F4', 0)
        self.curr_x += 25
        draw_key('pygame.K_F5', 'F5', 0)
        draw_key('pygame.K_F6', 'F6', 0)
        draw_key('pygame.K_F7', 'F7', 0)
        draw_key('pygame.K_F8', 'F8', 0)
        self.curr_x += 25
        draw_key('pygame.K_F9', 'F9', 0)
        draw_key('pygame.K_F10', 'F10', 0)
        draw_key('pygame.K_F11', 'F11', 0)
        draw_key('pygame.K_F12', 'F12', 0)
        self.curr_y += 30
        next_row()

        # numbers row
        draw_key('pygame.K_BACKQUOTE', '`', 0)
        draw_row(self.row_1)
        draw_key('pygame.K_MINUS', '-', 0)
        draw_key('pygame.K_EQUALS', '=', 0)
        draw_key('pygame.K_BACKSPACE', '\u2190', 45)
        self.curr_x += 20
        draw_key('pygame.K_INSERT', 'Ins', 0)
        draw_key('pygame.K_HOME', 'Home', 0)
        draw_key('pygame.K_PAGEUP', 'Pg\u2191', 0)
        next_row()

        # tab row
        draw_key('pygame.K_TAB', 'TAB', 20)
        draw_row(self.row_2)
        draw_key('pygame.K_LEFTBRACKET', '[', 0)
        draw_key('pygame.K_RIGHTBRACKET', ']', 0)
        draw_key('pygame.K_BACKSLASH', '\\', 25)
        self.curr_x += 20
        draw_key('pygame.K_DELETE', 'Del', 0)
        draw_key('pygame.K_END', 'End', 0)
        draw_key('pygame.K_PAGEDOWN', 'Pg\u2193', 0)
        next_row()

        # caps row
        draw_key('pygame.K_CAPSLOCK', 'CAPS', 30)
        draw_row(self.row_3)
        draw_key('pygame.K_SEMICOLON', ';', 0)
        draw_key('pygame.K_QUOTE', '\'', 0)
        draw_key('pygame.K_RETURN', 'ENTER', 65)
        next_row()

        # shift row
        draw_key('pygame.K_LSHIFT', 'SHIFT', 50)
        draw_row(self.row_4)
        draw_key('pygame.K_COMMA', ',', 0)
        draw_key('pygame.K_PERIOD', '.', 0)
        draw_key('pygame.K_SLASH', '/', 0)
        draw_key('pygame.K_RSHIFT', 'SHIFT', 95)
        self.curr_x += 70
        draw_key('pygame.K_UP', '\u2191', 0)
        next_row()

        # ctrl row
        draw_key('pygame.K_LCTRL', 'CTRL', 20)
        draw_key('pygame.K_LMETA', 'WIN', 0)
        draw_key('pygame.K_LALT', 'ALT', 10)
        draw_key('pygame.K_SPACE', '', 270)
        draw_key('pygame.K_RALT', 'ALT', 15)
        draw_key('pygame.K_RMETA', 'FN', 0)
        draw_key('pygame.K_MENU', 'OPT', 0)
        draw_key('pygame.K_RCTRL', 'CTRL', 30)
        self.curr_x += 20
        draw_key('pygame.K_LEFT', '\u2190', 0)
        draw_key('pygame.K_DOWN', '\u2193', 0)
        draw_key('pygame.K_RIGHT', '\u2192', 0)

    def draw_keyboard(self):
        keyboard_boarder = pygame.Rect(165, 180, 950, 370)
        pygame.draw.rect(screen, self.WHITE, keyboard_boarder, 2, border_radius=15)

        # Draw the keys
        for key, (rect, disp_name) in self.key_rects.items():
            # Draw the key's top surface
            key_color = (0, 255, 0, 0) if key in clicked_keys else (255, 255, 255, 0)
            pygame.gfxdraw.box(screen, rect, key_color)

            # Draw the key's black border
            border_rect = rect.inflate(-1, -1)
            pygame.draw.rect(screen, key_color, border_rect, 3, border_radius=10)

            # Draw the key label
            label = self.font.render(disp_name, True, key_color)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        font = pygame.font.Font(paths.MAIN_FONT, 60)
        label = font.render("CONTROLS", True, "#b68f40")
        label_rect = label.get_rect(center=(640, 85))
        screen.blit(label, label_rect)

        font = pygame.font.Font(paths.MAIN_FONT, 12)
        label = font.render("SELECT THE RELEVANT KEYS FOR THE GAME YOU HAVE CHOSEN", True, "#f6fcd4")
        label_rect = label.get_rect(center=(640, 125))
        screen.blit(label, label_rect)

        font = pygame.font.Font(paths.MAIN_FONT, 45)
        self.button_text = font.render("BACK", True, "#b68f40")
        self.button_text_hover = font.render("BACK", True, "#f6fcd4")
        self.button_rect = self.button_text.get_rect(center=(640, 640))
        screen.blit(self.button_text, self.button_rect)


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


def key_selection(keys):
    global clicked_keys, screen
    ks = KeySelection(keys)
    screen = ks.screen
    BG = pygame.image.load(paths.BACKGROUND_IMAGE)

    # Create a set to store the clicked keys
    if len(keys) == 0:
        keys = {'pygame.K_SPACE', 'pygame.K_UP', 'pygame.K_DOWN', 'pygame.K_RIGHT', 'pygame.K_LEFT'}
    clicked_keys = keys

    # Start the main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ks.handle_click(pos)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the button
                if ks.button_rect.collidepoint(event.pos):
                    running = False

        mouse_pos = pygame.mouse.get_pos()


        # Draw the keyboard and update the display
        screen.blit(BG, (0, 0))
        ks.draw_keyboard()


        font = pygame.font.Font(paths.MAIN_FONT, 45)
        # Check if the mouse is hovering over the text
        if ks.button_rect.collidepoint(mouse_pos):
            # Change the text color to red if hovering
            screen.blit(ks.button_text_hover, ks.button_rect)

        else:
            screen.blit(ks.button_text, ks.button_rect)

        pygame.display.flip()

    return clicked_keys
