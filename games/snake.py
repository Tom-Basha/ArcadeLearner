import pygame
import random
import sys


class GameSnake:
    def __init__(self):
        # Difficulty settings
        # Easy      ->  10
        # Medium    ->  25
        # Hard      ->  40
        # Harder    ->  60
        # Impossible->  120
        self.difficulty = 25

        # Window size
        self.frame_size_x = 720
        self.frame_size_y = 480

        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')

        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

        # Colors (R, G, B)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                         random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True

        self.score = 0
        self.direction = 'RIGHT'
        self.change_to = self.direction

    # Game Over
    def game_over(self):
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, self.red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 4)
        self.game_window.fill(self.black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(0, self.red, 'times', 20)
        pygame.display.flip()
        return

    # Score
    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.frame_size_x / 10, 15)
        else:
            score_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 1.25)
        self.game_window.blit(score_surface, score_rect)
        # pygame.display.flip()

    # Main game loop
    def run(self):
        while True:
            # Handling key events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'
                    # Esc -> Create event to quit the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # If two keys pressed simultaneously
            # we don't want snake to move into two directions
            # simultaneously
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Moving the snake
            if self.direction == 'UP':
                self.snake_pos[1] -= 10
            if self.direction == 'DOWN':
                self.snake_pos[1] += 10
            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

            # Snake body growing mechanism
            # if snake head is in the same position as the food
            if self.food_spawn:
                self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                                 random.randrange(1, (self.frame_size_y // 10)) * 10]
            self.food_spawn = False
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos == self.food_pos:
                self.food_spawn = True
                self.score += 1
            else:
                self.snake_body.pop()

            # Background
            self.game_window.fill(self.black)

            # Draw Snake
            for pos in self.snake_body:
                pygame.draw.rect(self.game_window, self.green, pygame.Rect(
                    pos[0], pos[1], 10, 10))

            # Draw Food
            pygame.draw.rect(self.game_window, self.white, pygame.Rect(
                self.food_pos[0], self.food_pos[1], 10, 10))

            # Game Over conditions
            if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
                self.game_over()
            if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
                self.game_over()
            # Touching the snake body
            for block in self.snake_body[1:]:
                if self.snake_pos == block:
                    self.game_over()

            # Score Display
            self.show_score(1, self.white, 'consolas', 20)
            # Refresh game screen
            pygame.display.update()
            # Frame Per Second /Refresh Rate
            self.fps_controller.tick(self.difficulty)


if __name__ == "__main__":
    game = GameSnake()
    # Game Run
    game.run()
