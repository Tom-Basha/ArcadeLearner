import pygame

from assets.components.button import back_btn
from assets.components.scrollbar import Scrollbar
from assets.paths import *
from assets.utils import *
from assets.components.slider import Slider

BACKGROUND = pygame.image.load(BACKGROUND_IMAGE)
BACKGROUND_COVER = pygame.image.load(SCROLLBAR_BG)


class Settings:
    def __init__(self, fitness=250, generations=1000, population=50, start_cp=-1, hidden_layers=3):
        pygame.init()

        # Screen creation
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Training Settings")

        # List settings
        self.top_margin = 200
        self.bottom_margin = 150
        self.list_window = SCREEN_H - self.top_margin - self.bottom_margin
        self.item_height = 150
        self.item_width = 600
        self.items_spacing = 20
        self.slider_x = SCREEN_W // 2 - 250
        # Items
        self.items = [
            ("Fitness Threshold", "Recommended: 250 - 350", Slider(self.slider_x, self.top_margin + 0 * (self.item_height + self.items_spacing), 500, 100, 1000, 50, fitness)),
            ("Generations", "Recommended: 1000", Slider(self.slider_x, self.top_margin + 1 * (self.item_height + self.items_spacing), 500, 50, 1000, 50, generations)),
            ("Population", "Recommended: 50", Slider(self.slider_x, self.top_margin + 2 * (self.item_height + self.items_spacing), 500, 20, 100, 5, population)),
            ("Start Checkpoint", "Set to -1 for a new training", Slider(self.slider_x, self.top_margin + 3 * (self.item_height + self.items_spacing), 500, -1, 50, 1, start_cp)),
            ("Neural Network Hidden Layers", "Recommended: 2 - 3", Slider(self.slider_x, self.top_margin + 4 * (self.item_height + self.items_spacing), 500, 1, 5, 1, hidden_layers))
        ]
        self.values = [fitness, generations, population, start_cp, hidden_layers]

        self.num_items = len(self.items)
        # Sliders
        self.sliders = [
            self.items[0][2],
            self.items[1][2],
            self.items[2][2],
            self.items[3][2],
            self.items[4][2]
                        ]

        # Scrollbar creation
        self.scrollbar = Scrollbar(self.screen,
                                   self.num_items * (self.item_height + self.items_spacing) - self.items_spacing,
                                   self.list_window, self.top_margin, self.bottom_margin)

        # Font
        self.font = pygame.font.Font(None, 36)

    def draw_item(self, item, sub_item, y, slider):
        # Set the dimensions and position of the rectangle
        rect_width = 750
        rect_height = 150
        x = SCREEN_W // 2 - rect_width // 2  # center the rectangle horizontally
        item_rect = pygame.Rect(x, y, rect_width, rect_height)

        # Create a new Surface with the SRCALPHA flag
        item_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)

        # Fill the Surface with a semi-transparent color
        item_surface.fill((0, 0, 0, 0))

        # Create a mask and a temporary surface for the rectangle with rounded corners
        mask = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 128))  # semi-transparent color
        pygame.draw.rect(mask, (0, 0, 0, 128), mask.get_rect(), border_radius=15)  # punch a hole in the mask

        # Create another temporary surface and draw the rectangle with rounded corners onto it
        temp = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        pygame.draw.rect(temp, (0, 0, 0, 128), temp.get_rect(), border_radius=15)

        # Apply the mask onto the temporary surface
        temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        # Draw the rectangle border with a border radius
        pygame.draw.rect(temp, MAIN_CLR, temp.get_rect(), width=3, border_radius=15)

        # Draw the temporary surface onto the item surface
        item_surface.blit(temp, (0, 0))

        # Render the text
        font = pygame.font.Font(None, 36)
        text = font.render(item, True, MAIN_CLR)
        surface_midtop = item_surface.get_rect().midtop

        text_rect = text.get_rect(midtop=(surface_midtop[0], surface_midtop[1] + 20))  # center the text

        # Draw the text onto the Surface
        item_surface.blit(text, text_rect)

        # Render the subtext
        sub_font = pygame.font.Font(None, 20)
        subtext = sub_font.render(sub_item, True, SECONDARY_CLR)
        subtext_rect = subtext.get_rect(midtop=(surface_midtop[0], surface_midtop[1] + 45))  # center the text

        # Draw the subtext onto the Surface
        item_surface.blit(subtext, subtext_rect)

        # Draw the Surface onto the screen
        self.screen.blit(item_surface, (x, y))

        # Draw the slider
        slider.y = 15 + y + self.item_height // 2  # update the slider's y-position
        slider.draw(self.screen)

    def run(self):
        HEADER, HEADER_RECT = header("SETTINGS")
        SUBHEAD, SUBHEAD_RECT = subhead("SELECT YOUR TRAINING PREFERENCES", 16)
        BACK_BTN = back_btn()

        while True:
            self.values = [
                item[2].value for i, item in enumerate(self.items)
            ]
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            BACK_BTN.change_color(MENU_MOUSE_POS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check if the mouse is over the button
                    if BACK_BTN.check_input(MENU_MOUSE_POS):
                        print(self.values)
                        # return self.values
                self.scrollbar.handle_event(event)

                # Handle events for the sliders
                for slider in self.sliders:
                    slider.handle_event(event)

            self.screen.blit(BACKGROUND, (0, 0))

            y = self.top_margin + self.scrollbar.scroll_offset
            for i, item in enumerate(self.items):
                self.draw_item(self.items[i][0], self.items[i][1], y, self.items[i][2])
                y += self.item_height + self.items_spacing

            self.scrollbar.draw()
            self.screen.blit(BACKGROUND_COVER, (0, 0))
            BACK_BTN.update(self.screen)
            self.screen.blit(HEADER, HEADER_RECT)
            self.screen.blit(SUBHEAD, SUBHEAD_RECT)

            pygame.display.flip()


# Create an instance of AnotherPage with the height of the content
another_page = Settings()

# Run the page
another_page.run()
