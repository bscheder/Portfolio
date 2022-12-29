import pygame
from classes.game import Game

class Screen:
    window_surface = None
    background_color = 'black'
    background = None
    scr_width = 800
    scr_heigth = 600
    paddle_length = 80
    paddle_width = 20
    paddle_pos_x = scr_width / 2 - paddle_length / 2 
    paddle_pos_y = scr_heigth - 50
    game = Game(paddle_pos_x,paddle_pos_y,paddle_width,paddle_length,
                scr_width / 2,paddle_pos_y - paddle_width/2,scr_width,scr_heigth)

    def draw_bricks(self):
        for brick in self.game.bricks:
            brick.rect = pygame.rect.Rect(
                         brick.pos_x, brick.pos_y, brick.width, brick.length)
            pygame.draw.rect(surface=self.background, color=brick.color,
                         rect=brick.rect, width=brick.width)

    def draw_paddle(self):
        paddle = self.game.paddle
        paddle.rect = pygame.rect.Rect(
                      paddle.pos_x, paddle.pos_y, paddle.width, paddle.length)
        pygame.draw.rect(surface=self.background, color=paddle.color,
                         rect=paddle.rect, width=paddle.width)
    def draw_ball(self):
        ball = self.game.ball
        self.game.move_ball()
        pygame.draw.circle(surface=self.background, color=ball.color, center=(ball.pos_x, ball.pos_y),
                           radius=ball.radius, width=ball.width)

    def draw_text(self,text,pos_x,pos_y):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(text, True,
                           self.game.paddle_color, self.background_color)
        text_rect = text.get_rect()
        text_rect.center = (pos_x, pos_y)

        self.window_surface.blit(text, text_rect)

    def draw_info_bar(self):
        self.draw_text('Scores:',70,30)
        self.draw_text(str(self.game.scores),170,30)
        self.draw_text('Lifes:',720,30)
        self.draw_text(str(self.game.lifes),780,30)

    def check_end_of_game(self):
        if len(self.game.bricks) == 0 \
           or self.game.lifes == 0:
           self.draw_text('GAME OVER',self.scr_width / 2, self.scr_heigth / 2)

    def init_screen(self):
        pygame.init()
        pygame.display.set_caption('Breakout')
        self.window_surface = pygame.display.set_mode(
            (self.scr_width, self.scr_heigth))

        self.background = pygame.Surface((self.scr_width, self.scr_heigth))
        self.background.fill(pygame.Color(self.background_color))

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.is_running = False
            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_SPACE:
                    self.game.start_ball()
                  if event.key == pygame.K_LEFT:
                    self.game.move_paddle_left(0,self.game.ball.is_inactive)
                  if event.key == pygame.K_RIGHT:
                    self.game.move_paddle_rigth(self.scr_width - self.paddle_length,self.game.ball.is_inactive)
        
        self.window_surface.blit(self.background, (0, 0))
        self.background.fill(self.background_color)
        self.draw_bricks()
        self.draw_paddle()
        self.draw_ball()
        self.draw_info_bar()
        self.check_end_of_game()

        pygame.display.update()
