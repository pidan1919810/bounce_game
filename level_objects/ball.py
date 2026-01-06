import pygame, random
from setting import BALL_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH

class Ball():
    def __init__(self) -> None:
        self.x = 400
        self.y = 250 

        self.radius = 10
        self.color = (255, 255, 255)
        
        self.direction = pygame.Vector2(random.randint(0,1),-1)
        if self.direction.x == 0:
            self.direction.x = -1
        self.speed = BALL_SPEED
        
        self.start = False
        
    def update(self, events:list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start = True
                
        if self.start:
            self.move()

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    # move the ball ,rebounce on wall, change diriction
    def move(self) -> None:
        #rad = random.choice(range(-1,2,2))/10

        speed = self.speed
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed

        #左右墙反弹
        if self.x + self.radius >= SCREEN_WIDTH or self.x-self.radius <= 0:
            self.direction.x *= -1
        #低于屏幕
        if self.y + self.radius >= SCREEN_HEIGHT:
            ball_manager.delete_ball(self)
        
        #上墙反弹
        if self.y <= 0:
            self.direction.y *= -1
            
        from .board import board

        if self.x + self.radius >= board.get_x() and self.x - self.radius <= board.get_x() + board.get_length():
            if self.y + self.radius >= board.get_y() and self.y - self.radius <= board.get_y():
                self.direction.y *= -1
        
        from .brick import brick_manager
        bricks = brick_manager.get_bricks()

        for brick in bricks:
            # 检查是否碰撞
            if (self.x + self.radius >= brick.get_x() and self.x - self.radius <= brick.get_x() + brick.get_size() and
                self.y + self.radius >= brick.get_y() and self.y - self.radius <= brick.get_y() + brick.get_size()):

                # 计算球中心与砖块中心的偏移
                brick_center_x = brick.get_x() + brick.get_size() / 2
                brick_center_y = brick.get_y() + brick.get_size() / 2

                dx = self.x - brick_center_x
                dy = self.y - brick_center_y

                # 根据偏移判断是水平碰撞还是垂直碰撞
                if abs(dx) > abs(dy):
                    self.direction.x *= -1
                else:
                    self.direction.y *= -1

                brick_manager.break_brick(brick)
                break  # 一次只处理一个砖块

                    
class Effect_ball(Ball):
    def __init__(self, effect:str) -> None:
        self.effect:str = effect
        self.x = random.randint(0,800)
        self.y = 0
    
    def draw(self, screen) -> None:
        pass

class Ball_manager():
    balls:list[Ball]
    ball_count:int
    
    def __init__(self) -> None:
        self.ball_count = 0
        self.balls = []
    
    def extend(self,number:int) -> None:
        for _ in range(number):
            self.balls.append(Ball())
    
    def update(self, events) -> None:
        for ball in self.balls:
            ball.update(events)
            
    def draw(self, screen:pygame.Surface) -> None:
        for ball in self.balls:
            ball.draw(screen)
            
    def delete_ball(self, ball):
        self.ball_count -= 1
        self.balls.remove(ball)


ball_manager = Ball_manager()