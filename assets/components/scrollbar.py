import pygame

from assets.utils import MAIN_CLR, SECONDARY_CLR


class Scrollbar:
    def __init__(self, screen, list_height, list_window, top_margin, bottom_margin):
        # Screen settings
        self.screen = screen

        # Scrollbar settings
        self.scrollbar_width = 20
        self.scrollbar_x = self.screen.get_width() - self.scrollbar_width - 10
        self.scrollbar_y = top_margin
        self.top_margin = top_margin
        self.bottom_margin = self.screen.get_height() - bottom_margin
        self.scroll_speed = 30

        # Scrollbar height and position
        self.scrollbar_height = self.bottom_margin if list_height <= list_window else list_window * list_window / list_height
        self.scrollbar_position = self.scrollbar_y

        # List settings
        self.list_height = list_height
        self.list_window = list_window
        self.min_offset = -list_height + list_window
        self.max_offset = 0
        self.scroll_offset = 0

        # Mouse settings
        self.is_held = False
        self.mouse_y = 0

        self.scrollbar_rect = pygame.Rect(self.scrollbar_x, self.scrollbar_y, self.scrollbar_width,
                                          self.scrollbar_height+1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.scrollbar_rect.collidepoint(event.pos):
                self.is_held = True
                self.mouse_y = event.pos[1] - self.scrollbar_position
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_held = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_held:
                self.scrollbar_position = event.pos[1] - self.mouse_y
                self.clamp_position()
                self.update_scroll_offset()
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset += event.y * self.scroll_speed
            self.clamp_offset()
            self.update_scrollbar_position()

    def draw(self):
        pygame.draw.rect(self.screen, MAIN_CLR,
                         (self.scrollbar_x, self.top_margin, self.scrollbar_width, self.list_window), border_radius=10)
        pygame.draw.rect(self.screen, SECONDARY_CLR, self.scrollbar_rect, border_radius=10)

    def clamp_position(self):
        self.scrollbar_position = max(self.top_margin,
                                      min(self.scrollbar_position, self.bottom_margin - self.scrollbar_height))
        self.scrollbar_rect.y = self.scrollbar_position

    def clamp_offset(self):
        self.scroll_offset = min(max(self.scroll_offset, self.min_offset), self.max_offset)

    def update_scroll_offset(self):
        ratio = (self.scrollbar_position - self.top_margin) / (
                    self.bottom_margin - self.scrollbar_height - self.top_margin)
        self.scroll_offset = self.max_offset + ratio * (self.min_offset - self.max_offset)

    def update_scrollbar_position(self):
        ratio = (self.scroll_offset - self.max_offset) / (self.min_offset - self.max_offset)
        self.scrollbar_position = self.top_margin + ratio * (
                    self.bottom_margin - self.top_margin - self.scrollbar_height)
        self.scrollbar_rect.y = self.scrollbar_position
