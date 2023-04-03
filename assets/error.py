import sys
import pygame
from assets.utils import *

BLINK_EVENT = pygame.USEREVENT + 0


def error_msg(message):
    def adjust_font_size(message, min_size, max_size, max_width):
        font_size = max_size
        while font_size >= min_size:
            font = pygame.font.Font(None, font_size)
            msg_lines = wrap_text(message, font, max_width)
            if len(msg_lines) * font.get_linesize() <= max_width:
                return font, msg_lines
            font_size -= 1
        return None, []

    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            new_line = ' '.join(current_line + [word])
            if font.size(new_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return lines

    # Get the current Pygame screen
    screen = pygame.display.get_surface()
    width, height = screen.get_size()

    # Save the current background
    background = screen.copy()

    # Create a surface to dim the screen
    dimmer = pygame.Surface((width, height))
    dimmer.fill(BLACK)
    dimmer.set_alpha(230)

    # Calculate the font size and wrap the message
    max_width = 400  # Set the width limit you want for the message
    font, message_lines = adjust_font_size(message, 12, 25, max_width)

    if not font:
        print("Error: Unable to fit the message within the specified width limit.")
        return

    error_title, error_rect = label_creation("ERROR", 40, ERROR_CLR, (SCREEN_W // 2, SCREEN_H // 2 - 45))

    msg_labels = []
    for i, line in enumerate(message_lines):
        msg_label, msg_rect = label_creation(line, font.get_height(), WHITE, (SCREEN_W // 2, 720 // 2 - font.get_height() * len(message_lines) // 2 + i * font.get_height()))
        msg_labels.append((msg_label, msg_rect))

    # Calculate the position of 'inst' to show it below the messages
    inst_y = msg_labels[-1][1].bottom + 10
    inst, inst_rect = label_creation("PRESS ANY KEY TO RETURN", 12, SECONDARY_CLR, (SCREEN_W // 2, inst_y))

    visible = True
    pygame.time.set_timer(BLINK_EVENT, 700)

    # Wait for a mouse click, keyboard click, or timeout
    while True:
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == BLINK_EVENT:
                visible = not visible

        # Restore the background
        screen.blit(background, (0, 0))

        # Draw the dimmer and message on the screen
        screen.blit(dimmer, (0, 0))
        screen.blit(error_title, error_rect)
        for msg_label, msg_rect in msg_labels:
            screen.blit(msg_label, msg_rect)

        if visible:
            screen.blit(inst, inst_rect)

        pygame.display.update()

        # Tick the Pygame clock
        pygame.time.Clock().tick(60)
