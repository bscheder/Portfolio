import pygame
from classes.data import Game


class Screen:
    window_surface = None
    background_color = '#022D36'
    white = '#FFFFFF'
    background = None
    width = 800
    heigth = 600
    game = Game()
    p1_scoreboard = {'text': None, 'text_rect': None, 'score': 0}
    p2_scoreboard = {'text': None, 'text_rect': None, 'score': 0}

    def draw_scores(self, pos_x, pos_y, board, score):
        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render(str(board.get('score')), True,
                           self.white, self.background_color)
        text_rect = text.get_rect()
        text_rect.center = (pos_x, pos_y)

        board['score'] = score
        board['text'] = text
        board['text_rect'] = text_rect

    def draw_paddle(self, paddle):
        paddle.paddle_rect = pygame.rect.Rect(
            paddle.pos_x, paddle.pos_y, paddle.width, paddle.length)
        pygame.draw.rect(surface=self.background, color=self.white,
                         rect=paddle.paddle_rect, width=paddle.width)

    def draw_net(self, surface, x_pos, round_number, width):
        for round in range(0, round_number):
            if round % 2 != 0:
                start_pos = (x_pos, round*10)
                end_pos = (x_pos, start_pos[1] + 8)
                pygame.draw.line(surface=surface, color=self.white,
                                 start_pos=start_pos, end_pos=end_pos, width=width)

    def draw_borders(self, surface, width):
        pygame.draw.line(surface=surface, color=self.white, start_pos=(
            0, width), end_pos=(self.width, width), width=width)
        pygame.draw.line(surface=surface, color=self.white, start_pos=(
            0, self.heigth - width), end_pos=(self.width, self.heigth - width), width=width)

    def draw_ball(self):
        ball = self.game.ball

        if ball.is_active:
            self.game.ball.obstacle_check(
                self.game.paddle_1.pos_y, self.game.paddle_2.pos_y, self.heigth, 4)
            ball.move_ball()
            pygame.draw.circle(surface=self.background, color=self.white, center=(ball.position_x, ball.position_y),
                               radius=ball.radius, width=ball.width)

            if self.game.score_check(self.width):
                self.game.ball.reset_ball()
                self.game.ball.start_ball(self.background, self.white)

    def draw_elements(self):
        self.background.fill(self.background_color)
        self.draw_net(self.background, int(
            self.width / 2), int(self.heigth / 10), 4)
        self.draw_borders(self.background, 4)
        self.draw_paddle(self.game.paddle_1)
        self.draw_paddle(self.game.paddle_2)
        self.draw_scores(self.width / 4, 40,
                         self.p1_scoreboard, self.game.p1_score)
        self.draw_scores(self.width - self.width / 4, 40,
                         self.p2_scoreboard, self.game.p2_score)
        self.draw_ball()

    def init_screen(self):
        pygame.init()
        pygame.display.set_caption('Pong')
        self.window_surface = pygame.display.set_mode(
            (self.width, self.heigth))

        self.background = pygame.Surface((self.width, self.heigth))
        self.background.fill(pygame.Color(self.background_color))
        self.game.running = True

        self.draw_elements()

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE \
                        and not self.game.ball.is_active:
                    self.game.ball.start_ball(self.background, self.white)
                if event.key == self.game.p1_keys.up:
                    self.game.paddle_1.move_paddle_up(0)
                elif event.key == self.game.p1_keys.down:
                    self.game.paddle_1.move_paddle_down(self.heigth)
                elif event.key == self.game.p2_keys.up:
                    self.game.paddle_2.move_paddle_up(0)
                elif event.key == self.game.p2_keys.down:
                    self.game.paddle_2.move_paddle_down(self.heigth)

        self.window_surface.blit(self.background, (0, 0))
        self.window_surface.blit(self.p1_scoreboard.get(
            'text'), self.p1_scoreboard.get('text_rect'))
        self.window_surface.blit(self.p2_scoreboard.get(
            'text'), self.p2_scoreboard.get('text_rect'))
        self.draw_elements()

        pygame.display.update()
