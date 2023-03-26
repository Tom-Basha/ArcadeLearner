import pygame
import pygame.gfxdraw
from assets.button import *
from assets.paths import *

class FeatureSelection:
    def __init__(self, features):
        # Define some constants for the colors and sizes of the keys
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_MARGIN = 20

        self.curr_x = 640
        self.curr_y = 250

        # Create a Pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Attributes")

        self.features = features

        self.clicked_features = set()
        self.GREEN = (0, 255, 0, 0)
        self.WHITE = (255, 255, 255, 0)
        self.font = pygame.font.Font(MAIN_FONT, 12)

    def draw_features(self):
        # Draw the features as buttons
        for i, feature in enumerate(self.features):
            button_rect = pygame.Rect(self.curr_x - self.BUTTON_WIDTH / 2,
                                      self.curr_y + i * (self.BUTTON_HEIGHT + self.BUTTON_MARGIN), self.BUTTON_WIDTH,
                                      self.BUTTON_HEIGHT)

            feature_color = GREEN if feature in clicked_features else WHITE
            pygame.gfxdraw.box(SCREEN, button_rect, feature_color)

            # Draw the key's border
            border_rect = button_rect.inflate(-1, -1)
            pygame.draw.rect(SCREEN, feature_color, border_rect, 3, border_radius=10)

            # Draw the key label
            feature_label = get_font(12).render(feature, True, feature_color)
            feature_rect = feature_label.get_rect(center=button_rect.center)
            SCREEN.blit(feature_label, feature_rect)


    def handle_click(self, pos):
        # Check if a feature button is clicked
        for i, feature in enumerate(self.features):
            button_rect = pygame.Rect(self.curr_x - self.BUTTON_WIDTH / 2,
                                      self.curr_y + i * (self.BUTTON_HEIGHT + self.BUTTON_MARGIN), self.BUTTON_WIDTH,
                                      self.BUTTON_HEIGHT)
            if button_rect.collidepoint(pos):
                if feature in clicked_features:
                    clicked_features.remove(feature)
                else:
                    clicked_features.add(feature)
                if len(clicked_features) == 0:
                    print('{}')
                else:
                    print("Selected keys: ", clicked_features)
                    print("Selected keys amount: ", len(clicked_features))

                return

        # Check if the "Play" button is clicked
        play_button_rect = pygame.Rect(self.curr_x - self.BUTTON_WIDTH / 2,
                                       self.curr_y + len(self.features) * (self.BUTTON_HEIGHT + self.BUTTON_MARGIN),
                                       self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        if play_button_rect.collidepoint(pos):
            if len(self.clicked_features) == 0:
                print("Please select at least one feature.")
            else:
                print("Selected features: ", self.clicked_features)
                return


def feature_selection(features):
    global SCREEN, clicked_features
    fs = FeatureSelection(features)
    SCREEN = fs.screen
    BG = pygame.image.load(BACKGROUND_IMAGE)

    HEADER, HEADER_RECT = header("ATTRIBUTES")
    SUBHEAD, SUBHEAD_RECT = subhead("SELECT THE RELEVANT ATTRIBUTES FOR YOUR GAME", 16)
    clicked_features = {"player"}
    # Start the main game loop
    while True:
        MENU_MOUSE_POS = pg.mouse.get_pos()

        BACK_BTN = back_btn()
        BACK_BTN.change_color(MENU_MOUSE_POS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                fs.handle_click(MENU_MOUSE_POS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is over the button
                if BACK_BTN.check_input(MENU_MOUSE_POS):
                    return None

        # Draw the features and update the display
        SCREEN.blit(BG, (0, 0))
        fs.draw_features()

        BACK_BTN.update(SCREEN)
        SCREEN.blit(HEADER, HEADER_RECT)
        SCREEN.blit(SUBHEAD, SUBHEAD_RECT)

        pygame.display.flip()
