import pygame
from classes.data import Game

LEFT_BUTTON = 1

class Screen:
    window_surface = None
    background_color = '#FFFFFF'
    dark_red = '#800000'
    background = None
    width = 600
    heigth = 600
    running = True
    game = Game()
    p1_scoreboard = {'text': None, 'text_rect': None, 'score': 0}
    p2_scoreboard = {'text': None, 'text_rect': None, 'score': 0}
    score_pos_x1 = 100
    score_pos_x2 = 450
    score_pos_y = 30
    table_pos_x = 50
    table_pos_y = 75

    def draw_scores(self, pos_x, pos_y, board, score):
         font = pygame.font.Font('fonts/sofachrome.rg-italic.ttf', 32)
         text = font.render(str(board['score']), True,
                            self.dark_red, self.background_color)
         text_rect = text.get_rect()
         text_rect.center = (pos_x, pos_y)

         board['score'] = score
         board['text'] = text
         board['text_rect'] = text_rect

    def reset_screen(self):
        self.background = pygame.Surface((self.width, self.heigth))
        self.background.fill(pygame.Color(self.background_color))

        table_img = pygame.image.load('images/table.png').convert_alpha()
        self.background.blit(table_img,(self.table_pos_x,self.table_pos_y))

    def init_screen(self):
        pygame.init()
        pygame.display.set_caption('TicTacToe')
        self.window_surface = pygame.display.set_mode(
            (self.width, self.heigth))

        self.reset_screen()

        self.draw_scores(self.score_pos_x1,self.score_pos_y,self.p1_scoreboard,self.game.p1.score)
        self.draw_scores(self.score_pos_x2,self.score_pos_y,self.p2_scoreboard,self.game.p1.score)
    
    def handle_clicks(self,pos_x,pos_y):
        for column_index in range(0,len(self.game.cells)):
            column = self.game.cells[column_index]
            
            for row_index in range(0,len(column)):
                cell = column[row_index]
                if (pos_x > cell.pos_x - cell.pos_offset  and pos_x < cell.pos_x + cell.pos_offset) \
                   and (pos_y > cell.pos_y - cell.pos_offset  and pos_y < cell.pos_y + cell.pos_offset):
                   self.game.cells[column_index][row_index].img = self.game.player.symbol
      
                   if self.game.player == self.game.p1:
                        self.game.player = self.game.p2
                   else:
                        self.game.player = self.game.p1
                    
                   self.game.number_of_cells +=1

                   break

    def draw_cells(self):
        for column in self.game.cells:
            for cell in column:
                try:
                    cell_img = pygame.image.load(cell.img).convert_alpha()
                    self.background.blit(cell_img,(cell.pos_x,cell.pos_y))
                except:
                    pass

    def end_run(self,message):
        font = pygame.font.Font('fonts/sofachrome.rg-italic.ttf', 32)
        text = font.render(message, True,
                            self.dark_red, self.background_color)
        text_rect = text.get_rect()
        text_rect.center = (300, 300)

        self.window_surface.blit(text, text_rect)
        
    def check_reset(self):
        if self.game.new_turn is True or self.game.number_of_cells == 9:
            self.game.number_of_cells = 0
            self.game.player = self.game.p1
            self.game.new_turn = False
            self.reset_cells()
            self.reset_screen()

    def increment_score(self,symbol):
        if self.game.new_turn is False and symbol == self.game.p1.symbol:
            self.game.p1.score += 1
        elif self.game.new_turn is False and symbol == self.game.p2.symbol:
            self.game.p2.score += 1
        
        self.game.new_turn = True

    def reset_cells(self):
         for column_index in range(0,len(self.game.cells)):
                column = self.game.cells[column_index]           
                for row_index in range(0,len(column)):
                    self.game.cells[column_index][row_index].img = None

    def check_wins(self,symbol):
        for index in range(0,3):
            if self.game.cells[index][0].img == symbol and \
               self.game.cells[index][1].img == symbol and \
               self.game.cells[index][2].img == symbol:
                self.increment_score(symbol)
                return True

        for index in range(0,3):
            if self.game.cells[0][index].img == symbol and \
               self.game.cells[1][index].img == symbol and \
               self.game.cells[2][index].img == symbol:
                self.increment_score(symbol)
                return True
        
        if self.game.cells[0][0].img == symbol and \
           self.game.cells[1][1].img == symbol and \
           self.game.cells[2][2].img == symbol:
            self.increment_score(symbol)
            return True

        if self.game.cells[2][0].img == symbol and \
           self.game.cells[1][1].img == symbol and \
           self.game.cells[0][2].img == symbol:
            self.increment_score(symbol)
            return True

        return False
    
    def check_ending(self):
        if self.check_wins(self.game.p1.symbol):
            self.end_run('PLAYER1 WINS!')

        elif self.check_wins(self.game.p2.symbol):
            self.end_run('PLAYER2 WINS!')
        
        elif self.game.number_of_cells == 9:
            self.end_run('DRAW!')
            
    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN \
               and event.button == LEFT_BUTTON:
                self.check_reset()
                self.handle_clicks(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

        self.window_surface.blit(self.background, (0, 0))
        self.window_surface.blit(self.p1_scoreboard.get(
            'text'), self.p1_scoreboard.get('text_rect'))
        self.window_surface.blit(self.p2_scoreboard.get(
            'text'), self.p2_scoreboard.get('text_rect'))
        
        self.draw_cells()
        self.draw_scores(self.score_pos_x1,self.score_pos_y,self.p1_scoreboard,self.game.p1.score)
        self.draw_scores(self.score_pos_x2,self.score_pos_y,self.p2_scoreboard,self.game.p2.score)
        self.check_ending()

        pygame.display.update()
