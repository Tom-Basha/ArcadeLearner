import pygame
import constants as c


class BaseObject(pygame.sprite.Sprite):
    def __init__(self):
        super(BaseObject, self).__init__()
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 0


class Block(BaseObject):
    def __init__(self, block_type, pos, groups, obstacles, width, height):
        super(Block, self).__init__()
        self.type = block_type
        self.pos = pos
        self.health = int(self.type)
        self.color = c.COLOR_LEGEND[self.type]
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect.copy()
        self.groups = groups
        self.obstacles = obstacles


class Ball(BaseObject):
    def __init__(self, groups, obstacles, player, surf_rect):
        super(Ball, self).__init__()
        # self.block_collision_sound = SoundEffect(c.IMPACT_1)
        # self.player_collision_sound = SoundEffect(c.IMPACT_2)
        # self.shoot_sound = SoundEffect(c.SHOOT_BALL_SOUND)
        self.surf_rect = surf_rect
        self.color = pygame.Color("lightblue")
        self.radius = 12
        self.ball_rect = int(self.radius * 2 ** 0.5)
        # self.rect = pygame.Rect(rnd(self.ball_rect, c.WIDTH - self.ball_rect), c.HEIGHT // 2, self.ball_rect,
        #                         self.ball_rect)
        self.old_rect = self.rect.copy()
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5
        self.active = False
        # self.aim = "right" if np.random.random() <= 0.5 else "left"
        self.groups = groups
        self.obstacles = obstacles
        self.player = player
        # self.last_brick = time.time()
        self.inc_s = False


class Player(BaseObject):
    def __init__(self, groups, obstacles):
        super(Player, self).__init__()
        self.x = 1280 / 2
        self.y = 688
        self.width = 120
        self.height = 27
        self.speed = 8
        self.speed_x = 0
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.rect.center = (self.x, self.y)
        self.color = pygame.Color("white")
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        self.old_rect = self.rect.copy()
        self.groups = groups
        self.obstacles = obstacles
        self.lives = 1
        self.score = 0


class ScreenShake:
    def __init__(self):
        self.timer = 0
        self.timer = 0
        self.offset_x = 0
        self.offset_4x = 0
        self.offset_y1 = 0

