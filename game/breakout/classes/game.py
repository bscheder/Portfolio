from classes.element import Brick,Paddle,Ball
from random import uniform
from math import sqrt

class Game:
    bricks = []
    brick_row_colors = ['#521fac','#363bdb','#4aac44','#d0a703','#d96638']
    brick_length = 30
    brick_width = 50
    paddle_color = '#6b7376'
    padding_x = 10.7
    padding_y = 10.7
    padding_y_first_line = 50
    ball_color = '#ffffff'

    def __init__(self,paddle_pos_x,paddle_pos_y,paddle_length, 
                 paddle_width,ball_pos_x,ball_pos_y,scr_width,scr_heigth):
        self.is_running = True
        self.build_up_bricks()
        self.paddle = Paddle(self.paddle_color,paddle_pos_x,paddle_pos_y,paddle_length,paddle_width)
        self.ball = Ball(ball_pos_x,ball_pos_y,self.ball_color)
        self.lifes = 3
        self.scores = 0
        self.scr_width = scr_width
        self.scr_heigth = scr_heigth
    
    def build_up_bricks(self):
        for row_index in range(0,5):
            row_color = self.brick_row_colors[row_index]
            for brick_offset in range(0,13):
                self.bricks.append(Brick(color=row_color, pos_x=self.padding_x + brick_offset*(self.padding_x + self.brick_width),
                pos_y=self.padding_y_first_line + self.padding_y + row_index*(self.padding_y+self.brick_length),width=self.brick_width,length=self.brick_length))    

    def move_paddle_left(self, border_pos, with_ball = True):
        if self.paddle.pos_x - self.paddle.velocity >= border_pos:
            self.paddle.pos_x = self.paddle.pos_x - self.paddle.velocity
            if with_ball:
                self.ball.pos_x = self.ball.pos_x - self.paddle.velocity
    
    def move_paddle_rigth(self, border_pos, with_ball = True):
        if self.paddle.pos_x + self.paddle.velocity <= border_pos:
            self.paddle.pos_x = self.paddle.pos_x + self.paddle.velocity
            if with_ball:
                self.ball.pos_x = self.ball.pos_x + self.paddle.velocity
    
    def calculate_speed_offset(self):
         self.ball.speed_offset = sqrt(
            pow(self.ball.displmnt_x, 2) + pow(self.ball.displmnt_y, 2))

    def start_ball(self):
        if self.ball.is_inactive:
            self.ball.is_inactive = False
            self.ball.displmnt_y = 1
            self.ball.displmnt_x = round(uniform(0.1, 0.9), 2)
            self.calculate_speed_offset()

    def restart_game(self):
        if self.lifes > 0:
            self.ball.pos_x = self.paddle.pos_x + self.paddle.width / 2
            self.ball.pos_y = self.paddle.pos_y - self.paddle.length / 2
            self.ball.is_inactive = True

    def is_brick(self,pos_x,pos_y):
        for brick in self.bricks:
            if brick.pos_y + brick.length >= pos_y and \
                (brick.pos_x <= pos_x and pos_x <= brick.pos_x + brick.width):
                self.bricks.remove(brick)
                self.ball.displmnt_x *= -1        
                self.ball.direction_up = False
                self.scores += 100
                break
    
    def is_upper_border(self):
        if self.ball.direction_up and self.ball.pos_y - self.ball.radius <= 0:
            self.ball.displmnt_x *= -1
            self.ball.direction_up = False

    def is_lower_border(self):
        if self.ball.direction_up is False \
           and self.ball.pos_y >= 600      \
           and self.lifes > 0: 
            self.lifes -= 1 
            self.restart_game()

    def is_side_border(self):
        if self.ball.pos_y < self.scr_heigth and \
          (self.ball.pos_x - self.ball.radius <= 0 or self.ball.pos_x + self.ball.radius >= self.scr_width):
            self.ball.displmnt_x *= -1

    def is_paddle(self):
        if self.paddle.pos_y <= self.ball.pos_y + self.ball.radius and \
            (self.paddle.pos_x <= self.ball.pos_x and \
             self.ball.pos_x <= self.paddle.pos_x + self.paddle.width):
            self.ball.direction_up = True
            self.ball.displmnt_x *= -1
            self.ball.displmnt_y = round(uniform(0.1, 0.9),2)
            self.calculate_speed_offset()

    def move_ball(self):
        if self.ball.is_inactive is False:
            self.is_upper_border()
            self.is_side_border()
            self.is_lower_border()
            self.is_brick(self.ball.pos_x,self.ball.pos_y - self.ball.velocity)
            if self.ball.direction_up:
                self.ball.pos_y = self.ball.pos_y - self.ball.velocity
                self.ball.pos_x = self.ball.pos_x - \
                self.ball.displmnt_x  / self.ball.speed_offset * self.ball.velocity
                self.ball.pos_y = self.ball.pos_y - \
                self.ball.displmnt_y  / self.ball.speed_offset * self.ball.velocity
            else:
                self.is_paddle()
                self.ball.pos_y = self.ball.pos_y + self.ball.velocity

                self.ball.pos_x = self.ball.pos_x + \
                self.ball.displmnt_x  / self.ball.speed_offset * self.ball.velocity
                self.ball.pos_y = self.ball.pos_y + \
                self.ball.displmnt_y  / self.ball.speed_offset * self.ball.velocity
