
class Cell:
    def __init__(self,img,pos_x,pos_y):
        self.img = img
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_offset = 65

class Player():
    def __init__(self,symbol):
        self.symbol = symbol
        self.score = 0

class Game:
    p1 = Player('images/x-sign.png')
    p2 = Player('images/circle.png')
    new_turn = False
  
    def __init__(self):
        self.player = self.p1
        self.cells = [[Cell(img=None,pos_x=73,pos_y=119),
                       Cell(img=None,pos_x=254.3,pos_y=129),
                       Cell(img=None,pos_x=428.3,pos_y=139)],
                      [Cell(img=None,pos_x=83.0,pos_y=274),
                       Cell(img=None,pos_x=263,pos_y=286),
                       Cell(img=None,pos_x=433.8,pos_y=284)],
                      [Cell(img=None,pos_x=93.0,pos_y=421),
                       Cell(img=None,pos_x=268.0,pos_y=437),
                       Cell(img=None,pos_x=433.3,pos_y=427.3)]]
        self.number_of_cells = 0
