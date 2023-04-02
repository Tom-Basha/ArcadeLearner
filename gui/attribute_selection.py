import math

import pygame
import sys

from assets.button import *
from assets.utils import *
from assets.paths import *

pygame.init()


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
        # self.items_per_column = len(self.attributes) // self.columns if len(game_attributes) >= self.columns else 1
        self.list_height = 0
        for i, class_info in enumerate(self.classes):
            self.items_per_column = math.ceil(len(class_info[1]) / self.columns)
            self.list_height += self.items_per_column * (self.item_h + self.items_spacing)
        self.list_height += len(self.classes) * 70
        if len(self.classes) > 1:
            self.list_height += (len(self.classes) - 1) * 80
        # Screen creation
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Attributes")

        #  Scrollbar settings
        self.scrollbar_width = 20
        self.scrollbar_x = SCREEN_W
        self.scrollbar_y = 0
        self.scrollbar_height = 0
        if self.list_height > self.list_window:
            self.scrollbar_height = self.list_window * self.list_window / self.list_height
            self.scrollbar_x = SCREEN_W - self.scrollbar_width - 10
        self.min_offset = -self.list_height + SCREEN_H - self.top_margin - self.bottom_margin
        self.max_offset = 0
        self.scroll_offset = 0
        self.scrollbar_position = 0
        self.scroll_speed = 30

    def update(self, scroll_offset):
        ratio = (scroll_offset - self.max_offset) / (self.min_offset - self.max_offset)
        self.scrollbar_position = ratio * (
                SCREEN_H - self.scrollbar_height - self.top_margin - self.bottom_margin) + self.top_margin

    def draw(self):
        pygame.draw.rect(self.screen, MAIN_CLR,
                         (self.scrollbar_x, self.top_margin, self.scrollbar_width, self.list_window), border_radius=10)
        pygame.draw.rect(self.screen, SECONDARY_CLR, (
            self.scrollbar_x, self.scrollbar_y + self.scrollbar_position, self.scrollbar_width, self.scrollbar_height),
                         border_radius=10)

    def add_headers(self, class_name, rects, x=190, y=200):
        label = get_font(25).render("Class Name: \'" + class_name + "\'", True, SECONDARY_CLR)
        rect = label.get_rect(topleft=(x, y))
        if self.top_margin <= rect.y <= SCREEN_H - self.bottom_margin - rect.height:
            self.screen.blit(label, rect)

        y += 30

        label = get_font(25).render("Attributes:", True, SECONDARY_CLR)
        rect = label.get_rect(topleft=(x, y))
        if self.top_margin <= rect.y <= SCREEN_H - self.bottom_margin - rect.height:
            self.screen.blit(label, rect)

    def render_list(self, selected_items):
        position = (SCREEN_W // 8 + 30, self.scroll_offset)
        headers_space = 70
        classes_space = 150
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

                y += headers_space
                item_text = class_name + "." + item
                text_color = GREEN if item_text in selected_items else WHITE
                rect = pygame.Rect(x, y, self.item_w, self.item_h)
                attribute_label, attribute_rect = keyboard_key(item, text_color, rect)
                rects.append((rect, class_name + "." + item))
                if self.top_margin <= attribute_rect.y <= SCREEN_H - self.bottom_margin - attribute_rect.height:
                    self.screen.blit(attribute_label, attribute_rect)
                    pygame.gfxdraw.box(self.screen, rect, text_color)

                    # Draw the key's border
                    border_rect = rect.inflate(-1, -1)
                    pygame.draw.rect(self.screen, text_color, border_rect, 3, border_radius=10)

                if i == len(class_attributes) - 1:
                    curr_y += (self.items_spacing + self.item_h) * items_per_column + classes_space
        return rects

    def handle_scrollbar(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * self.scroll_speed
            self.scroll_offset = min(max(self.scroll_offset, self.min_offset), self.max_offset)


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
        MENU_MOUSE_POS = pg.mouse.get_pos()

        BACK_BTN = back_btn()
        BACK_BTN.change_color(MENU_MOUSE_POS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return selected_items
            att_list.handle_scrollbar(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the mouse is over the button
                if BACK_BTN.check_input(MENU_MOUSE_POS):
                    return selected_items
                for i, text_rect in enumerate(text_rects):
                    in_range = att_list.top_margin < MENU_MOUSE_POS[1] < att_list.top_margin + att_list.list_window
                    if text_rect[0].collidepoint(MENU_MOUSE_POS) and in_range:
                        if text_rect[1] in selected_items:
                            selected_items.remove(text_rect[1])
                        else:
                            selected_items.add(text_rect[1])
                        if len(selected_items) == 0:
                            print('{}')
                        else:
                            print("Selected Attributes: ", selected_items)
                            print("Selected Attributes amount: ", len(selected_items))

        BG = pygame.image.load(BACKGROUND_IMAGE)
        SCREEN.blit(BG, (0, 0))

        text_rects = att_list.render_list(selected_items)

        att_list.update(att_list.scroll_offset)
        att_list.draw()

        BACK_BTN.update(SCREEN)
        SCREEN.blit(HEADER, HEADER_RECT)
        SCREEN.blit(SUBHEAD, SUBHEAD_RECT)

        pygame.display.flip()
        clock.tick(60)
