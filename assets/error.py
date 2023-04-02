import pygame
from assets.utils import *

BLINK_EVENT = pygame.USEREVENT + 0


def error_msg(message):

    # Get the current Pygame screen
    screen = pygame.display.get_surface()
    # Save the current background
    background = screen.copy()

    width, height = screen.get_size()

    # Create a surface to dim the screen
    dimmer = pygame.Surface((width, height))
    dimmer.fill(BLACK)
    dimmer.set_alpha(230)

    # Create a font for the message

    error_title, error_rect = label_creation("ERROR", 35, ERROR_CLR, (SCREEN_W // 2, SCREEN_H // 2 - 40))
    msg, msg_rect = label_creation(message, 25, WHITE, (SCREEN_W // 2, 720 // 2))
    inst, inst_rect = label_creation("PRESS ANY KEY TO RETURN", 12, SECONDARY_CLR, (SCREEN_W // 2, 720 // 2 + 30))
    visible = True

    pygame.time.set_timer(BLINK_EVENT, 700)

    # Wait for a mouse click, keyboard click, or timeout
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == BLINK_EVENT:
                visible = not visible

        # Restore the background
        screen.blit(background, (0, 0))

        # Draw the dimmer and message on the screen
        screen.blit(dimmer, (0, 0))
        screen.blit(error_title, error_rect)
        screen.blit(msg, msg_rect)

        if visible:
            screen.blit(inst, inst_rect)
        pygame.display.update()

        # Tick the Pygame clock
        pygame.time.Clock().tick(60)
