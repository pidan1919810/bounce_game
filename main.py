import pygame
from setting import *
import time
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True

pygame.display.set_caption("bounce_game")

class Ball():
    def __init__(self):
        self.x = 400
        self.y = 250 

        self.radius = 10
        self.color = (255, 255, 255)
        
        self.diriction = [random.randrange(-1,2,2), 1] # [x, y]
        self.speed = 5 

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    # move the ball ,rebounce on wall, change diriction
    def move(self,brick,board):
        rad = random.random()*10%2-1
        print(rad)

        speed = self.speed
        self.x += self.diriction[0]*speed
        self.y += self.diriction[1]*speed

        if self.x + self.radius >= screen.get_width() or self.x-self.radius <= 0:
            self.diriction[0] *= -1
            self.diriction[1] += rad
        if self.y + self.radius >= screen.get_height():
            fail()
        if self.y  <= 0:
            self.diriction[1] *= -1
            self.diriction[1] += rad

        if self.x + self.radius >= board.get_x_y_length()[0] and self.x - self.radius <= board.get_x_y_length()[0] + board.get_x_y_length()[2]:
            if self.y + self.radius >= board.get_x_y_length()[1] and self.y - self.radius <= board.get_x_y_length()[1] + 10:
                self.diriction[1] *= -1
                self.diriction[1] += rad

        for b in brick:
            global brick_list
            if self.x + self.radius >= b.get_x_y_size()[0] and self.x - self.radius <= b.get_x_y_size()[0] + b.get_x_y_size()[2]:
                if self.y + self.radius >= b.get_x_y_size()[1] and self.y - self.radius <= b.get_x_y_size()[1] + b.get_x_y_size()[2]:
                    self.diriction[1] *= -1 
                    self.diriction[1] += rad
                    brick_list.remove(b)
                    break

            if self.y + self.radius >= b.get_x_y_size()[1] and self.y - self.radius <= b.get_x_y_size()[1] + b.get_x_y_size()[2]:
                if self.x + self.radius >= b.get_x_y_size()[0] and self.x - self.radius <= b.get_x_y_size()[0] + b.get_x_y_size()[2]:
                    self.diriction[0] *= -1 
                    self.diriction[1] += rad
                    if b in brick_list:
                        brick_list.remove(b)
                        break
            

class Board():
    def __init__(self):
        self.x = 400
        self.y = 500
        self.length = 400

        self.color = (255,100,100)

    def get_x_y_length(self):
        return self.x, self.y, self.length

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x -= 10
            if event.key == pygame.K_RIGHT:
                self.x += 10

            if self.x+self.length >= 800:
                self.x = 800 - self.length
            if self.x <= 0:
                self.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, 10))

brick_size = 20

class Brick():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = brick_size
    
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.x+1, self.y+1, self.size-1, self.size-1))
        pygame.draw.lines(screen, (255, 255, 255), True, [(self.x, self.y), (self.x+self.size, self.y), (self.x+self.size, self.y+self.size), (self.x, self.y+self.size)], 1)

    def get_x_y_size(self):
        return self.x, self.y, self.size
    
brick_list = []

def make_brick():
    for x in range(0, 800, 20):
        for y in range(0, 200, 20):
            brick_list.append(Brick(x, y))

is_fail = False

def fail():
    global is_fail
    is_fail = True

ball = Ball()
board = Board()

make_brick()

coutner = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time.sleep(1/FPS)

    coutner += 1
    if coutner <= 3*FPS:
        sec = coutner//FPS

        screen.fill((0, 0, 0), (0, 0, 800, 600))
        font = pygame.font.SysFont(None, 50)
        text = font.render(f"game will be start in {3-sec} seconds", True, (255, 255, 255))
        screen.blit(text, (200, 250))
        pygame.display.flip()
        continue

    

    if not is_fail:
        ball.move(brick_list,board)
        board.input(event)

        screen.fill((0, 0, 0), (0, 0, 800, 600))
        ball.draw(screen)

        for b in brick_list:
            b.draw(screen)

        board.draw(screen)
        
    else:
        font = pygame.font.SysFont(None, 50)
        text = font.render("You Fail!", True, (255, 255, 255))
        screen.blit(text, (400, 250))

    pygame.display.flip()

pygame.quit()