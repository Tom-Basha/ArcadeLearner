import pygame
import sys
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Number Range Input with Scroll Example")

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the input box and number range
input_box = pygame.Rect(50, 50, 300, 40)
min_num = 1
max_num = 10
input_text = ""
input_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse clicked on input box
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            # Check if input box is active
                if input_active:
                    # Check if input is a digit
                    if event.unicode.isdigit():
                        input_text += event.unicode

                    # Check if input is within the number range
                    if input_text.isdigit():
                        num = int(input_text)
                        if num < min_num:
                            input_text = str(min_num)
                        elif num > max_num:
                            input_text = str(max_num)

                    # Check for up arrow key
                    if event.key == pygame.K_UP:
                        num = int(input_text)
                        if num < max_num:
                            num += 1
                        input_text = str(num)

                    # Check for down arrow key
                    if event.key == pygame.K_DOWN:
                        num = int(input_text)
                        if num > min_num:
                            num -= 1
                        input_text = str(num)




    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.flip()
