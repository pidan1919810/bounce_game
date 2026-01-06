import pygame
from setting import BRICK_SIZE, SCREEN_HIGHT, SCREEN_WIDTH

class Brick_manager:
    bricks:list[Brick]
    def break_brick(self, brick) -> bool:
        #返回是否成功
        pass

    def is_brick_alive(self, brick) -> bool:
        pass
    
    def make_brick(self):
        for x in range(0, SCREEN_WIDTH, 20):
            for y in range(0, 200, 20):
                self.bricks.append(Brick(x, y))
    
    def get_bricks(self) -> tuple[Brick]:
        return tuple(self.bricks)
    
class Brick():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = BRICK_SIZE
    
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.x+1, self.y+1, self.size-1, self.size-1))
        pygame.draw.lines(screen, (255, 255, 255), True, [(self.x, self.y), (self.x+self.size, self.y), (self.x+self.size, self.y+self.size), (self.x, self.y+self.size)], 1)

    def get_x_y_size(self):
        return self.x, self.y, self.size

brick_manager = Brick_manager()