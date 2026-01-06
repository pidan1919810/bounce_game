import pygame
from setting import *
import time
import random

SCREEN_WIDTH = 600
SCREEN_HIGHT = 800
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))

running = True

pygame.display.set_caption("bounce_game")

num_of_ball = 0
def dellete_ball(b):
    global num_of_ball
    num_of_ball -= 1
    ball.remove(b)

class Ball():
    def __init__(self):
        global num_of_ball
        num_of_ball += 1
        
        self.x = 400
        self.y = 250 

        self.radius = 10
        self.color = (255, 255, 255)
        
        self.direction = pygame.Vector2(1,1)
        self.speed = 20

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    # move the ball ,rebounce on wall, change diriction
    def move(self,brick,board):
        global num_of_ball
        #rad = random.choice(range(-1,2,2))/10

        speed = self.speed
        self.x += self.direction.x*speed
        self.y += self.direction.y*speed

        #左右墙反弹
        if self.x + self.radius >= screen.get_width() or self.x-self.radius <= 0:
            self.direction.x *= -1
        #低于屏幕
        if self.y + self.radius >= screen.get_height():
            if num_of_ball == 1:
                fail()
            else:
                dellete_ball(self)
        #上墙反弹
        if self.y <= 0:
            self.direction.y *= -1

        if self.x + self.radius >= board.get_x_y_length()[0] and self.x - self.radius <= board.get_x_y_length()[0] + board.get_x_y_length()[2]:
            if self.y + self.radius >= board.get_x_y_length()[1] and self.y - self.radius <= board.get_x_y_length()[1]:
                self.direction.y *= -1

        for b in brick:
            global brick_list
            if self.x + self.radius >= b.get_x_y_size()[0] and self.x - self.radius <= b.get_x_y_size()[0] + b.get_x_y_size()[2]:
                if self.y + self.radius >= b.get_x_y_size()[1] and self.y - self.radius <= b.get_x_y_size()[1] + b.get_x_y_size()[2]:
                    self.direction.y *= -1 
                    brick_list.remove(b)
                    break

            if self.y + self.radius >= b.get_x_y_size()[1] and self.y - self.radius <= b.get_x_y_size()[1] + b.get_x_y_size()[2]:
                if self.x + self.radius >= b.get_x_y_size()[0] and self.x - self.radius <= b.get_x_y_size()[0] + b.get_x_y_size()[2]:
                    self.direction.x *= -1 
                    if b in brick_list:
                        brick_list.remove(b)
                        break
            

class Board():
    def __init__(self):
        self.x = 0
        self.y = 500
        self.length = 150

        self.color = (255,100,100)

    def get_x_y_length(self):
        return self.x, self.y, self.length

    def input(self, event):
        print(event)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.x -= 10
            if event.key == pygame.K_RIGHT:
                self.x += 10

        if event.type == pygame.TEXTINPUT:
            if event.text == 'a':
                self.x -= 10
            if event.text == 'd':
                self.x += 10

            if event.text == ' ':
                print('a')
                global ball,num_of_ball
                num_of_ball += 1
                ball.append(Ball())

        if self.x+self.length >= 800:
            self.x = 800 - self.length
        if self.x <= 0:
            self.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, 10))

BRICK_SIZE = 20

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

class effect_ball():
    def __init__(self, effect:str):
        self.effect:str = effect
        self.x = random.randint(0,800)
        self.y = 0
    
    def draw(self):
        pygame.draw

brick_list = []

def make_brick():
    for x in range(0, SCREEN_WIDTH, 20):
        for y in range(0, 200, 20):
            brick_list.append(Brick(x, y))

is_fail = False

def fail():
    global is_fail
    is_fail = True

def is_win():
    if len(brick_list) == 0:
        return True

ball:list[Ball] = []
ball.extend([Ball() for i in range(3)])
board = Board()

make_brick()

coutner = 0
time_start = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time.sleep(1/FPS)

    #coutner += 1
    #if coutner <= (time_start)*FPS:
    #    sec = coutner//FPS

    #    screen.fill((0, 0, 0), (0, 0, 800, 600))
    #    font = pygame.font.SysFont(None, 50)
    #    text = font.render(f"game will be start in {3-sec} seconds", True, (255, 255, 255))
    #    screen.blit(text, (200, 250))
    #    pygame.display.flip()
    #    continue

    if not is_fail:
        for ba in ball:
            ba.move(brick_list,board)
        board.input(event)

        if is_win():
            font = pygame.font.SysFont(None, 50)
            text = font.render("You Win!", True, (255, 255, 255))
            screen.blit(text, (400, 250))
            break

        screen.fill((0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HIGHT))
        for ba in ball:
            ba.draw(screen)

        for b in brick_list:
            b.draw(screen)

        board.draw(screen)
        
    else:
        font = pygame.font.SysFont(None, 50)
        text = font.render("You Fail!", True, (255, 255, 255))
        screen.blit(text, (400, 250))

    pygame.display.flip()
    

    

pygame.quit()