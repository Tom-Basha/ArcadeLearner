import pygame

from assets import paths
from assets.paths import BACKGROUND_IMAGE

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Black Rectangle")
BACKGROUND = pygame.image.load(paths.BACKGROUND_IMAGE)
# Set colors
black = (0, 0, 0)
white = (255, 255, 255)

# Draw the white background
screen.blit(BACKGROUND, (0, 0))

# Draw the black rectangle
rectangle_width = 1280
rectangle_height = 370
rectangle_x = 0
rectangle_y = 200
rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)
pygame.draw.rect(screen, black, rectangle)

# Update the screen
pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # Save screenshot when 'S' key is pressed
                pygame.image.save(screen, "screenshot.png")

# Quit the program
pygame.quit()
