import pygame
from .base_object import Base_object
from pygame.event import Event
from setting import BRICK_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

class Brick(Base_object):
    def __init__(self, x:float, y:float) -> None:
        self.x:float = x
        self.y:float = y
        self.size = BRICK_SIZE
    
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, (200, 200, 200), (self.x+1, self.y+1, self.size-1, self.size-1))
        pygame.draw.lines(screen, (255, 255, 255), True, [(self.x, self.y), (self.x+self.size, self.y), (self.x+self.size, self.y+self.size), (self.x, self.y+self.size)], 1)

    def update(self, events:list[Event]) -> None:
        pass
    
    def get_size(self) -> float:
        return self.size
    

class Brick_manager:
    bricks:list[Brick]
    
    def __init__(self) -> None:
        self.bricks = []
        self.make_brick()
    
    def break_brick(self, brick:Brick) -> bool:
        #返回是否成功
        if not self.is_brick_alive(brick):
            return False
        self.bricks.remove(brick)
        return True

    def is_brick_alive(self, brick:Brick) -> bool:
        return brick in self.bricks
    
    def make_brick(self) -> None:
        for x in range(0, SCREEN_WIDTH, BRICK_SIZE):
            for y in range(0, 200, BRICK_SIZE):
                self.bricks.append(Brick(x, y))
    
    def get_bricks(self) -> tuple[Brick, ...]:
        return tuple(self.bricks)
    
    def update(self, events:list[pygame.event.Event]) -> None:
        pass
    
    def draw(self, screen:pygame.Surface) -> None:
        for brick in self.bricks:
            brick.draw(screen)


brick_manager = Brick_manager()