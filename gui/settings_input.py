import sys
from assets.button import *
from assets.utils import *
from assets.paths import *

pg.init()
screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
pg.display.set_caption("Settings")
COLOR_INACTIVE = pg.Color(WHITE)
COLOR_ACTIVE = pg.Color(GREEN)
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text='', pop_size=0, fitness_threshold=0, hidden_layers=0):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.pop_size = pop_size  # initial value for population
        self.fitness_threshold = fitness_threshold  # initial value for threshold
        self.hidden_layers = hidden_layers  # initial value for threshold
        self.MIN_POP_SIZE = 30
        self.MAX_POP_SIZE = 100
        self.MIN_FITNESS_THRESHOLD = 100
        self.MAX_FITNESS_THRESHOLD = 1000
        self.MIN_HIDDEN_LAYERS = 1
        self.MAX_HIDDEN_LAYERS = 5

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        elif event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    # Update the corresponding value based on the text in the input box
                    if self.rect.y == 200:  # Input box for pop_size
                        # Check if input is within the number range
                        # Check if input is a digit
                        if self.text.isdigit():
                            num = int(self.text)
                            if num < self.MIN_POP_SIZE:
                                self.text = str(self.MIN_POP_SIZE)
                            elif num > self.MAX_POP_SIZE:
                                self.text = str(self.MAX_POP_SIZE)
                            self.pop_size = num
                            print("pop_size: ", self.pop_size)
                    elif self.rect.y == 300:  # Input box for fitness_threshold
                        if self.text.isdigit():
                            num = int(self.text)
                            if num < self.MIN_FITNESS_THRESHOLD:
                                self.text = str(self.MIN_FITNESS_THRESHOLD)
                            elif num > self.MAX_FITNESS_THRESHOLD:
                                self.text = str(self.MAX_FITNESS_THRESHOLD)
                            self.fitness_threshold = num
                            print("fitness_threshold: ", self.fitness_threshold)
                    elif self.rect.y == 400:  # Input box for hidden_layers
                        if self.text.isdigit():
                            num = int(self.text)
                            if num < self.MIN_HIDDEN_LAYERS:
                                self.text = str(self.MIN_HIDDEN_LAYERS)
                            elif num > self.MAX_HIDDEN_LAYERS:
                                self.text = str(self.MAX_HIDDEN_LAYERS)
                            self.hidden_layers = num
                            print("hidden_layers: ", self.hidden_layers)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_UP:
                    if self.rect.y == 200:  # Input box for pop_size
                        num = int(self.text)
                        if num < self.MAX_POP_SIZE:
                            num += 5
                        self.pop_size = num
                        self.text = str(num)
                    elif self.rect.y == 300:  # Input box for fitness_threshold
                        num = int(self.text)
                        if num < self.MAX_FITNESS_THRESHOLD:
                            num += 50
                        self.fitness_threshold = num
                        self.text = str(num)
                    elif self.rect.y == 400:  # Input box for hidden_layers
                        num = int(self.text)
                        if num < self.MAX_HIDDEN_LAYERS:
                            num += 1
                        self.hidden_layers = num
                        self.text = str(num)
                elif event.key == pg.K_DOWN:
                    if self.rect.y == 200:  # Input box for pop_size
                        num = int(self.text)
                        if num > self.MIN_POP_SIZE:
                            num -= 5
                        self.pop_size = num
                        self.text = str(num)
                    elif self.rect.y == 300:  # Input box for fitness_threshold
                        num = int(self.text)
                        if num > self.MIN_FITNESS_THRESHOLD:
                            num -= 50
                        self.fitness_threshold = num
                        self.text = str(num)
                    elif self.rect.y == 400:  # Input box for hidden_layers
                        num = int(self.text)
                        if num > self.MIN_HIDDEN_LAYERS:
                            num -= 1
                        self.hidden_layers = num
                        self.text = str(num)
                else:
                    self.text += event.unicode
                    # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

        # Draw values on screen
        font = pg.font.Font(None, 36)
        pop_text = font.render("pop_size: ", True, (255, 255, 255))
        thresh_text = font.render("fitness_threshold: ", True, (255, 255, 255))
        hid_text = font.render("hidden_layers: ", True, (255, 255, 255))
        screen.blit(pop_text, (50, 200))
        screen.blit(thresh_text, (50, 300))
        screen.blit(hid_text, (50, 400))


def main():
    clock = pg.time.Clock()
    input_box1 = InputBox(400, 200, 140, 32)
    input_box2 = InputBox(400, 300, 140, 32)
    input_box3 = InputBox(400, 400, 140, 32)
    input_boxes = [input_box1, input_box2, input_box3]
    done = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        MENU_MOUSE_POS = pg.mouse.get_pos()

        BACK_BTN = back_btn()
        BACK_BTN.change_color(MENU_MOUSE_POS)

        BG = pg.image.load(BACKGROUND_IMAGE)
        screen.blit(BG, (0, 0))

        BACK_BTN.update(screen)
        HEADER, HEADER_RECT = header("SETTINGS")
        SUBHEAD, SUBHEAD_RECT = subhead("SELECT THE RELEVANT ATTRIBUTES FOR THE AI LEARNING PROCESS", 16)
        screen.blit(HEADER, HEADER_RECT)
        screen.blit(SUBHEAD, SUBHEAD_RECT)

        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()
