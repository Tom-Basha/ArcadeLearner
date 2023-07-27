import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import math
from assets.components.button import back_btn
from assets.paths import BACKGROUND_IMAGE
from assets.components.scrollbar import Scrollbar

from assets.utils import *


class AttributeList:
    def __init__(self, game_attributes, game_classes):
        # List settings
        self.classes = game_classes
        self.attributes = game_attributes
        self.item_h = 50
        self.item_w = 250
        self.items_spacing = 2
        self.top_margin = 200
        self.bottom_margin = 150
        self.list_window = SCREEN_H - self.top_margin - self.bottom_margin
        self.columns = 3
        self.column_spacing = SCREEN_W // 4
        self.list_height = 0
        for i, class_info in enumerate(self.classes):
            self.items_per_column = math.ceil(len(class_info[1]) / self.columns)
            self.list_height += self.items_per_column * (self.item_h + self.items_spacing)
        self.list_height += len(self.classes) * 70
        if len(self.classes) > 1:
            self.list_height += (len(self.classes) - 1) * 80
        self.headers_space = 70
        self.classes_space = 150

        # Screen creation.
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Attributes")

        # Scrollbar creation.
        self.scrollbar = Scrollbar(self.screen, self.list_height, self.list_window, self.top_margin, self.bottom_margin)

    def add_headers(self, class_name, rects, x=190, y=200):
        label, rect = attribute_header("Class Name: \'" + class_name + "\'", SECONDARY_CLR, (x, y), 25)
        if self.top_margin <= rect.y <= SCREEN_H - self.bottom_margin - rect.height:
            self.screen.blit(label, rect)

        y += 30

        label, rect = attribute_header("Attributes:", SECONDARY_CLR, (x, y), 25)
        if self.top_margin <= rect.y <= SCREEN_H - self.bottom_margin - rect.height:
            self.screen.blit(label, rect)

    def render_list(self, selected_items):
        position = (SCREEN_W // 8 + 30, self.scrollbar.scroll_offset)
        curr_y = self.top_margin
        rects = []
        for j, class_info in enumerate(self.classes):
            class_name = class_info[0]
            class_attributes = class_info[1]
            items_per_column = math.ceil(len(class_attributes) / self.columns)
            for i, item in enumerate(class_attributes):
                column_index = i // items_per_column
                item_index = i % items_per_column
                x = position[0] + column_index * self.column_spacing
                y = position[1] + (self.items_spacing + self.item_h) * item_index + curr_y

                if i == 0:
                    self.add_headers(class_name, rects, y=y)

                y += self.headers_space
                if class_name in selected_items:
                    text_color = GREEN if item in selected_items[class_name] else WHITE
                else:
                    text_color = WHITE
                rect = pygame.Rect(x, y, self.item_w, self.item_h)
                attribute_label, attribute_rect = keyboard_key(item, text_color, rect)
                rects.append((rect, class_name, item))
                if self.top_margin <= attribute_rect.y <= SCREEN_H - self.bottom_margin - attribute_rect.height:
                    self.screen.blit(attribute_label, attribute_rect)
                    pygame.gfxdraw.box(self.screen, rect, text_color)

                    # Draw the key's border.
                    border_rect = rect.inflate(-1, -1)
                    pygame.draw.rect(self.screen, text_color, border_rect, 3, border_radius=10)

                if i == len(class_attributes) - 1:
                    curr_y += (self.items_spacing + self.item_h) * items_per_column + self.classes_space

        return rects


def attribute_selection(game_classes, selected_attributes):
    global text_rects
    clock = pygame.time.Clock()
    game_attributes = game_classes[0][1]
    selected_items = set() if selected_attributes == 0 else selected_attributes

    HEADER, HEADER_RECT = header("ATTRIBUTES")
    SUBHEAD, SUBHEAD_RECT = subhead("SELECT THE RELEVANT ATTRIBUTES FOR THE AI LEARNING PROCESS", 16)

    att_list = AttributeList(game_attributes, game_classes)
    SCREEN = att_list.screen

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        BACK_BTN = back_btn()
        BACK_BTN.change_color(MENU_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return selected_items

            att_list.scrollbar.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the button.
                if BACK_BTN.check_input(MENU_MOUSE_POS):
                    return selected_items
                for i, text_rect in enumerate(text_rects):
                    in_range = att_list.top_margin < MENU_MOUSE_POS[1] < att_list.top_margin + att_list.list_window
                    if text_rect[0].collidepoint(MENU_MOUSE_POS) and in_range:
                        if text_rect[1] in selected_items:
                            if text_rect[2] in selected_items[text_rect[1]]:
                                selected_items[text_rect[1]].remove(text_rect[2])
                                if not selected_items[text_rect[1]]:
                                    del selected_items[text_rect[1]]
                            else:
                                selected_items[text_rect[1]].append(text_rect[2])
                            if len(selected_items) == 0:
                                print('{}')
                            else:
                                print("Selected Attributes: ", selected_items)
                                print("Selected Attributes amount: ", len(selected_items))
                        else:
                            selected_items[text_rect[1]] = [text_rect[2]]

        BG = pygame.image.load(BACKGROUND_IMAGE)
        SCREEN.blit(BG, (0, 0))

        text_rects = att_list.render_list(selected_items)

        att_list.scrollbar.draw()

        BACK_BTN.update(SCREEN)
        SCREEN.blit(HEADER, HEADER_RECT)
        SCREEN.blit(SUBHEAD, SUBHEAD_RECT)

        pygame.display.flip()
        clock.tick(60)
