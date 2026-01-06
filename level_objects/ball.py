import pygame
from setting import BALL_SPEED, SCREEN_HIGHT, SCREEN_WIDTH
from brick import brick_manager
class Ball_manager():
    balls:list[Ball]
    ball_count:int
    
    def __init__(self) -> None:
        self.ball_count = 0
        self.balls = []
    
    def extend(self,number:int) -> None:
        for _ in range(number):
            self.balls.append(Ball())
    
    def update(self, event) -> None:
        for ball in self.balls:
            ball.update(event)
    
class Ball():
    def __init__(self):
        self.x = 400
        self.y = 250 

        self.radius = 10
        self.color = (255, 255, 255)
        
        self.direction = pygame.Vector2(1,1)
        self.speed = BALL_SPEED
        
    def update(self, event):
        self.move()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    # move the ball ,rebounce on wall, change diriction
    def move(self):
        #rad = random.choice(range(-1,2,2))/10

        speed = self.speed
        self.x += self.direction.x * speed
        self.y += self.direction.y * speed

        #左右墙反弹
        if self.x + self.radius >= SCREEN_WIDTH or self.x-self.radius <= 0:
            self.direction.x *= -1
        #低于屏幕
        if self.y + self.radius >= SCREEN_HIGHT:
            pass #删除球
        
        #上墙反弹
        if self.y <= 0:
            self.direction.y *= -1
            
        from board import board

        if self.x + self.radius >= board.get_x() and self.x - self.radius <= board.get_x() + board.get_length():
            if self.y + self.radius >= board.get_y() and self.y - self.radius <= board.get_y():
                self.direction.y *= -1
        
        from brick import brick_manager
        bricks = brick_manager.get_bricks()

        for brick in bricks:
            if self.x + self.radius >= b.get_x_y_size()[0] and self.x - self.radius <= b.get_x_y_size()[0] + b.get_x_y_size()[2]:
                if self.y + self.radius >= b.get_x_y_size()[1] and self.y - self.radius <= b.get_x_y_size()[1] + b.get_x_y_size()[2]:
                    self.direction.y *= -1 
                    brick_manager.break_brick(b)

            if self.y + self.radius >= b.get_x_y_size()[1] and self.y - self.radius <= b.get_x_y_size()[1] + b.get_x_y_size()[2]:
                if self.x + self.radius >= b.get_x_y_size()[0] and self.x - self.radius <= b.get_x_y_size()[0] + b.get_x_y_size()[2]:
                    self.direction.x *= -1 
                    brick_manager.break_brick(b)

                        
ball_manager = Ball_manager()