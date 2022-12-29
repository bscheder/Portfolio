import pygame
from dataclasses import dataclass
from random import randrange, uniform
from math import sqrt


@dataclass
class Paddles:
    pos_x: int
    pos_y: int
    width: int
    length: int
    velocity = 25
    paddle_rect = None

    def move_paddle_up(self, border_pos):
        if self.pos_y - self.velocity >= border_pos:
            self.pos_y = self.pos_y - self.velocity

    def move_paddle_down(self, border_pos):
        if self.pos_y + self.velocity <= border_pos - self.length:
            self.pos_y = self.pos_y + self.velocity


@dataclass
class Keys:
    up: int
    down: int


@dataclass
class Ball:
    position_x = 400
    position_y = 300
    speed = 1
    radius = 10
    width = 20
    directon_y = 1
    paddle_touch = 0
    is_active = False
    ball_rect = False
    displmnt_x = None
    displmnt_y = None
    directon_x = None
    speed_offset = None

    def calculate_speed_offset(self):
        self.speed_offset = sqrt(
            pow(self.displmnt_x, 2) + pow(self.displmnt_y, 2))

    def paddle_touched(self, pos_y_paddle):
        if self.position_y >= pos_y_paddle and self.position_y <= pos_y_paddle + 50:
            self.displmnt_y = uniform(0.8, 1.2)
        elif self.position_y >= pos_y_paddle + 70 and self.position_y <= pos_y_paddle + 120:
            self.displmnt_y = uniform(-1.2, -0.8)
        else:
            self.displmnt_y = 0.01

        self.displmnt_x *= -1
        self.paddle_touch += 1

    def obstacle_check(self, pos_y_l_paddle, pos_y_r_paddle, screen_width, border_width):
        if self.position_y >= pos_y_l_paddle - self.radius and self.position_y <= pos_y_l_paddle + 120 + self.radius and round(self.position_x) == 60:
            self.paddle_touched(pos_y_l_paddle)
        elif self.position_y >= pos_y_r_paddle - self.radius and self.position_y <= pos_y_r_paddle + 120 + self.radius and round(self.position_x) == 740:
            self.paddle_touched(pos_y_r_paddle)
        elif self.position_y <= border_width:
            self.displmnt_y *= -1
        elif self.position_y >= screen_width-border_width:
            self.displmnt_y *= -1

        self.calculate_speed_offset()

    def move_ball(self):
        if self.is_active:
            self.position_x = self.position_x + \
                (self.displmnt_x * self.directon_x) / \
                self.speed_offset * self.speed
            self.position_y = self.position_y + \
                (self.displmnt_y * self.directon_y) / \
                self.speed_offset * self.speed

        if self.paddle_touch > 5:
            self.speed = 1.5

    def start_ball(self, surface, color, direction=None):
        self.ball_rect = pygame.draw.circle(surface=surface, color=color, center=(
            self.position_x, self.position_y), radius=self.radius, width=self.width)
        self.is_active = True
        self.speed = 1
        self.paddle_touch = 0

        self.displmnt_x = 1
        self.displmnt_y = round(uniform(0.01, 0.5), 2)
        self.calculate_speed_offset()

        self.directon_x = randrange(-1, 1)
        if self.directon_x == 0:
            self.directon_x = 1

        self.directon_y = randrange(-1, 1)
        if self.directon_y == 0:
            self.directon_y = 1

    def reset_ball(self):
        self.position_x = 400
        self.position_y = 300

    def change_angle():
        pass


@dataclass
class Game:
    p1_score = 0
    p2_score = 0
    running = False
    p1_keys = Keys(up=pygame.K_w, down=pygame.K_s)
    p2_keys = Keys(up=pygame.K_o, down=pygame.K_l)
    paddle_1 = Paddles(pos_x=30, pos_y=240, width=30, length=120)
    paddle_2 = Paddles(pos_x=740, pos_y=240, width=30, length=120)
    ball = Ball()

    def score_check(self, width):
        ball = self.ball
        if ball.position_x < 0:
            self.p2_score += 1
            return True
        elif ball.position_x > width:
            self.p1_score += 1
            return True
        return False
