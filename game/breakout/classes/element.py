class Brick:
    def __init__(self,color,pos_x,pos_y,length,width):
        self.length = length
        self.width = width
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_broken = False
        self.rect = None

class Paddle:
    def __init__(self,color,pos_x,pos_y,length,width):
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.length = length
        self.width = width
        self.velocity = 40
        self.rect = None

class Ball:
    def __init__(self,pos_x, pos_y,color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.velocity = 1
        self.speed_offset = None
        self.displmnt_x = None
        self.displmnt_y = None
        self.rect = None
        self.radius = 10
        self.width = 10
        self.is_inactive = True
        self.direction_up = True
