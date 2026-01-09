import pygame, random

from pygame import Vector2
from pygame.event import Event
from abc import ABC, abstractmethod
from typing import override

from .base_object import Base_object
from setting import *

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
        self.direction = Vector2(0,0)
        
    def set_direction(self, dir:Vector2) -> None:
        self.direction = dir
        
    def random_direction(self) -> None:
        import math
        random_angle = random.randint(30,150)
        angle_rad = math.radians(random_angle)
        self.direction = pygame.Vector2(
            math.cos(angle_rad),
            -math.sin(angle_rad)
        )
        
    def move(self) -> None:
        self.direction.normalize_ip()
        speed = self.speed
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed
    
    def bounce(self) -> None:
        delta_move_x = random.randint(-20,20)/100
        delta_move_y = random.randint(-20,20)/100
        #左右墙反弹
        if self.x + self.raduis >= SCREEN_WIDTH or self.x-self.raduis <= 0:
            self.direction.x *= -1 + delta_move_x
        #低于屏幕
        if self.y + self.raduis >= SCREEN_HEIGHT:
            self.out_screen()

        #上墙反弹
        if self.y <= 0:
            self.direction.y *= -1 + delta_move_y
            
        from .board import board
        #弹版反弹
        if self.x + self.raduis >= board.get_x() and self.x - self.raduis <= board.get_x() + board.get_length():
            if self.y + self.raduis >= board.get_y() and self.y - self.raduis <= board.get_y():
                self.direction.y *= -1 + delta_move_y
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
                
                if abs(dx) > abs(dy):
                    self.direction.x *= -1 + delta_move_x
                else:
                    self.direction.y *= -1 + delta_move_y

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
        
        self.random_direction()
        
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
            from level import add_score
            add_score(10)
            #随机生成分裂球
            if random.random() <= EFFECT_BALL_GENRATE_PERCENTAGE:
                from .board import board
                ball_manager.extend(Effect_ball, board.get_pos() + Vector2(0,-40))


class Effect_ball(Base_balls):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x,y)
        #self.effect:str = effect
        self.raduis = 10
        self.speed = 8
        self.random_direction()
        
        self.color = pygame.Color(255,0,0)
        
    def update(self, events: list[Event]) -> None:
        self.move()
        self.bounce()
    
    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.raduis)
    
    def touch_object(self, object: Base_object | None) -> None:
        self.effect()
        ball_manager.delete_ball(self)
        from level import add_score
        add_score(10)
        
    def effect(self) -> None:
        ball_manager.extend(Normal_ball,(self.x-20,self.y),(self.x,self.y),(self.x+20,self.y))
    
    def out_screen(self) -> None:
        return super().out_screen()
    

class Ball_manager(Base_object):
    balls:list[Base_balls]
    ball_count:int
    
    def __init__(self) -> None:
        self.init()
    
    def init(self) -> None:
        self.ball_count = 0
        self.balls = []
        self.start = False
    
    def extend( 
            self, 
            cls:type[Base_balls], 
            *args:tuple[float, float] | Vector2
        ) -> bool:
        
        if self.get_cout() <= BALL_NUMBER_LIMIT:
            for pos in args:
                self.ball_count += 1
                self.balls.append(cls.create(pos[0], pos[1]))
            return True
        else:
            return False
    
    def update(self, events) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if cheat.SPAWN_ELEMENT:
                    if event.key == pygame.K_n:
                        self.extend(Normal_ball,(300,500))
                    if event.key == pygame.K_m:
                        self.extend(Effect_ball,(300,500))

        #发射方向计算
        if cheat.BALL_FOLLOW_MOUSE or not self.start:
            if pygame.mouse.get_pressed()[0]:
                for ball in self.balls:
                    ball_pos = ball.get_pos()
                    mouse_pos = Vector2(pygame.mouse.get_pos())
                    direction = mouse_pos - ball_pos
                    ball.set_direction(direction.normalize())
                self.start = True
        
        for ball in self.balls:
            ball.update(events)
            
    def draw(self, screen:pygame.Surface) -> None:
        for ball in self.balls:
            ball.draw(screen)
            
            #绘制发射方向指示
            if not self.start:
                ball_pos = ball.get_pos()
                mouse_pos = Vector2(pygame.mouse.get_pos())
                direction = mouse_pos - ball_pos
                instruction_pos = ball_pos + direction.normalize()*INSTRUCTION_LINE_LENGTH
                pygame.draw.line(screen, (128,128,128), ball_pos, instruction_pos, 5)
            
            
    def delete_ball(self, ball:Base_balls) -> None:
        self.ball_count -= 1
        self.balls.remove(ball)
        
    def get_cout(self) -> int:
        return self.ball_count
        
    def clear(self) -> None:
        self.ball_count = 0
        self.balls = []
        self.start = False


ball_manager = Ball_manager()