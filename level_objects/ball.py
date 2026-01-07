import pygame, random

from pygame import Vector2
from pygame.event import Event
from abc import ABC, abstractmethod
from typing import override

from .base_object import Base_object
from setting import BALL_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH

class Base_balls(Base_object, ABC):
    """
        球的基类
    """
    direction:Vector2
    
    raduis:float
    color:pygame.Color
    speed:float
    
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y)
        self.direction = Vector2(1,0)
        
    def move(self) -> None:
        speed = self.speed
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed
    
    def bounce(self) -> None:
        #左右墙反弹
        if self.x + self.raduis >= SCREEN_WIDTH or self.x-self.raduis <= 0:
            self.direction.x *= -1
        #低于屏幕
        if self.y + self.raduis >= SCREEN_HEIGHT:
            self.out_screen()

        #上墙反弹
        if self.y <= 0:
            self.direction.y *= -1
            
        from .board import board
        #弹版反弹
        if self.x + self.raduis >= board.get_x() and self.x - self.raduis <= board.get_x() + board.get_length():
            if self.y + self.raduis >= board.get_y() and self.y - self.raduis <= board.get_y():
                self.direction.y *= -1
        #砖块反弹
        from .brick import brick_manager
        bricks = brick_manager.get_bricks()

        for brick in bricks:
            # 检查是否碰撞
            if (self.x + self.raduis >= brick.get_x() and self.x - self.raduis <= brick.get_x() + brick.get_size() and
                self.y + self.raduis >= brick.get_y() and self.y - self.raduis <= brick.get_y() + brick.get_size()):

                # 计算球中心与砖块中心的偏移
                brick_center_x = brick.get_x() + brick.get_size() / 2
                brick_center_y = brick.get_y() + brick.get_size() / 2

                dx = self.x - brick_center_x
                dy = self.y - brick_center_y

                # 根据偏移判断是水平碰撞还是垂直碰撞
                delta_move = random.randint(-10,10)/100
                if abs(dx) > abs(dy):
                    self.direction.x *= -1 + delta_move
                else:
                    self.direction.y *= -1 + delta_move

                self.direction.normalize()
                self.touch_object(brick)
                
                break  # 一次只处理一个砖块

    @abstractmethod
    def out_screen(self) -> None:
        pass

    @abstractmethod
    def touch_object(self, object:Base_object|None) -> None:
        pass

class Normal_ball(Base_balls):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x,y)
        
        self.raduis = 10
        self.color = pygame.Color(255, 255, 255)
        self.speed = BALL_SPEED
        
        self.direction = pygame.Vector2(random.randint(0,1),-1)
        if self.direction.x == 0:
            self.direction.x = -1
        
    def update(self, events:list[pygame.event.Event]) -> None:
        if ball_manager.start:
            self.move()
            self.bounce()

    def draw(self, screen:pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.raduis)

    def out_screen(self) -> None:
        ball_manager.delete_ball(self)
    
    def touch_object(self, object:Base_object|None) -> None:
        from .brick import brick_manager, Brick
        if isinstance(object, Brick):
            brick_manager.break_brick(object)

#class Effect_ball(Base_balls):
#    def __init__(self, x:float, y:float) -> None:
#        super().__init__(x,y)
#        #self.effect:str = effect
#        self.x = random.randint(0,800)
#        self.y = 0
    
#    def draw(self, screen) -> None:
#        super().draw(screen)
    
#    def bounce(self) -> None:
#        ball_manager.extend(Ball,(self.x-20,self.y),(self.x,self.y),(self.x+20,self.y))
#        ball_manager.delete_ball(self)
        
class Ball_manager():
    balls:list[Base_balls]
    ball_count:int
    
    def __init__(self) -> None:
        self.ball_count = 0
        self.balls = []
        self.start = False
    
    def extend( 
            self, 
            cls:type[Base_balls], 
            *args:tuple[float, float]
            ) -> None:
        
        for pos in args:
            self.balls.append(cls.create(pos[0], pos[1]))
    
    def update(self, events) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.start = True
        
        for ball in self.balls:
            ball.update(events)
            
    def draw(self, screen:pygame.Surface) -> None:
        for ball in self.balls:
            ball.draw(screen)
            
    def delete_ball(self, ball:Base_balls) -> None:
        self.ball_count -= 1
        self.balls.remove(ball)


ball_manager = Ball_manager()