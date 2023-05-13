import os
import pickle
import socket
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import sys

pygame.init()

fps = 60
size = (700, 500)
screen = pygame.display.set_mode(size, pygame.NOFRAME)


class Player:
    def __init__(self, color, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.width = width
        self.height = height
        self.speed = speed
        self.score = 0
        self.lives = 1

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move_up(self):
        self.rect.y = max(self.rect.y - self.speed, 30)

    def move_down(self):
        self.rect.y = min(self.rect.y + self.speed, screen.get_height() - self.height)


class Opponent:
    def __init__(self, color, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, ball):
        if ball.rect.y < self.rect.y + self.height / 2:
            self.rect.y = max(self.rect.y - self.speed, 30)
        elif ball.rect.y > self.rect.y + self.height / 2:
            self.rect.y = min(self.rect.y + self.speed, screen.get_height() - self.height)


class Ball:
    def __init__(self, color, x, y, radius):
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.color = color
        self.radius = radius
        self.curr_speed = 3
        self.speed = [self.curr_speed, self.curr_speed]
        self.hits = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.top <= 30 or self.rect.bottom >= size[1]:
            self.speed[1] *= -1

    def reset(self):
        self.rect.x = size[0] // 2
        self.rect.y = (size[1] - 30) // 2
        self.speed = [-speed for speed in self.speed]


def draw_field():
    screen.fill((0, 0, 0))
    dash_length = 8
    gap_length = 4
    x1, y1 = [size[0] // 2, 30]
    x2, y2 = [size[0] // 2, size[1]]

    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))

    dx = dx / distance
    dy = dy / distance

    x, y = x1, y1
    for _ in range(distance):
        pygame.draw.line(screen, (255, 255, 255), (round(x), round(y)),
                         (round(x + dx * dash_length), round(y + dy * dash_length)), 1)
        x += dx * (dash_length + gap_length)
        y += dy * (dash_length + gap_length)
    pygame.draw.line(screen, (255, 255, 255), (0, 30), (700, 30), 2)


def update(player, ball):
    font = pygame.font.Font(None, 34)

    score_text = font.render("Score: " + str(player.score), True, (255, 255, 255))
    rect = score_text.get_rect(topleft=(10, 5))
    screen.blit(score_text, rect)

    speed_text = font.render("Ball Speed: " + str(ball.curr_speed), True, (255, 255, 255))
    rect = speed_text.get_rect(midtop=(size[0] // 2, 5))
    screen.blit(speed_text, rect)

    lives_text = font.render("Lives: " + str(player.lives), True, (255, 255, 255))
    rect = lives_text.get_rect(topright=(690, 5))
    screen.blit(lives_text, rect)


def handle_collision(ball, player, opponent):
    if ball.rect.colliderect(player.rect):
        ball.hits += 1
        if ball.hits % 5 == 0:
            ball.curr_speed += 1
        if player.rect.top < ball.rect.centery < player.rect.bottom:
            # The ball hit the side of the paddle
            ball.rect.right = player.rect.left
            if ball.rect.centery <= player.rect.centery:
                ball.speed = [-ball.curr_speed, -ball.curr_speed]
            else:
                ball.speed = [-ball.curr_speed, ball.curr_speed]
        else:
            # The ball hit the corners of the paddle
            if ball.rect.centery < player.rect.centery:
                ball.rect.bottom = player.rect.top
            else:
                ball.rect.top = player.rect.bottom
            ball.speed[1] *= -1

    if ball.rect.colliderect(opponent.rect):
        ball.hits += 1
        if ball.hits % 5 == 0:
            ball.curr_speed += 1
        if opponent.rect.top < ball.rect.centery < opponent.rect.bottom:
            # The ball hit the side of the paddle
            ball.rect.left = opponent.rect.right
            if ball.rect.centery <= opponent.rect.centery:
                ball.speed = [ball.curr_speed, -ball.curr_speed]
            else:
                ball.speed = [ball.curr_speed, ball.curr_speed]
        else:
            # The ball hit the corners of the paddle
            if ball.rect.centery < opponent.rect.centery:
                ball.rect.bottom = opponent.rect.top
            else:
                ball.rect.top = opponent.rect.bottom
            ball.speed[1] *= -1

    if ball.rect.left <= 0:
        player.score += 1
        ball.reset()

    if ball.rect.right >= size[0]:
        player.lives -= 1
        if player.lives == 0:
            pygame.quit()
            sys.exit()
        ball.reset()


def main():
    global fps
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    try:
        s.connect(('localhost', 8888))
        instructions = pickle.loads(s.recv(4096))
        connected = True
        fps = 0
    except ConnectionRefusedError:
        pass

    clock = pygame.time.Clock()

    ball = Ball((255, 255, 255), 350, 250, 10)
    player = Player((255, 255, 255), 650, 250, 10, 60, 7)
    opponent = Opponent((255, 255, 255), 40, 250, 10, 60, 5)

    entities = [player, opponent, ball]

    active_objects = [player, opponent, ball]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP:
                    player.move_up()
                elif event.key == pygame.K_DOWN:
                    player.move_down()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()

        draw_field()
        ball.move()
        opponent.move(ball)

        for obj in entities:
            obj.draw()

        handle_collision(ball, player, opponent)
        update(player, ball)
        pygame.display.flip()
        clock.tick(fps)

        if connected:
            data = []
            for class_name, attributes in instructions.items():
                for obj in active_objects:
                    if obj.__class__.__name__ == class_name and obj is not None:
                        for attr in attributes:
                            temp_obj = obj
                            temp_attr = attr
                            if "." in attr:
                                parts = attr.split(".")
                                temp_obj = getattr(obj, str(parts[0]))
                                temp_attr = parts[1]
                            if hasattr(temp_obj, temp_attr):
                                data.append((attr, str(getattr(temp_obj, temp_attr))))

            # print(data)

            s.sendall(pickle.dumps(data))
            action = s.recv(4096)
            if action:
                action = pickle.loads(action)
                if action != 0:
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=eval(action)))
            else:
                break
            time.sleep(0.001)

    s.close()


if __name__ == "__main__":
    main()
