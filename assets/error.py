import sys
import pygame
from assets.utils import *

BLINK_EVENT = pygame.USEREVENT + 0


def error_msg(message_lines):
    # Get the current Pygame screen
    screen = pygame.display.get_surface()

    # Save the current background
    background = screen.copy()

    # Create a surface to dim the screen
    dimmer = pygame.Surface((SCREEN_W, SCREEN_H))
    dimmer.fill(BLACK)
    dimmer.set_alpha(230)
    y_offset = SCREEN_H // 2   # Set the starting Y offset for the first line of the error message

    # Create the error title label and rect
    error_title, error_rect = label_creation("ERROR", 40, ERROR_CLR, (SCREEN_W // 2, y_offset - (len(message_lines) * 25)))

    # Create an array to store the message labels and rects
    msg_labels = []

    # Create a label and rect for each line in message_lines
    for line in message_lines:
        msg_label, msg_rect = label_creation(line, 30, WHITE, (SCREEN_W // 2, y_offset))
        msg_labels.append((msg_label, msg_rect))
        y_offset += 40  # Increase the Y offset for the next line of the error message

    # Create the 'Press any key to return' label and rect
    inst, inst_rect = label_creation("PRESS ANY KEY TO RETURN", 12, SECONDARY_CLR, (SCREEN_W // 2, y_offset))

    visible = True
    pygame.time.set_timer(BLINK_EVENT, 700)

    # Wait for a mouse click or keyboard click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == BLINK_EVENT:
                visible = not visible

        # Restore the background
        screen.blit(background, (0, 0))

        # Draw the dimmer, error title, and error message on the screen
        screen.blit(dimmer, (0, 0))
        screen.blit(error_title, error_rect)
        for msg_label, msg_rect in msg_labels:
            screen.blit(msg_label, msg_rect)

        if visible:
            screen.blit(inst, inst_rect)

        pygame.display.update()

        # Tick the Pygame clock
        pygame.time.Clock().tick(60)

