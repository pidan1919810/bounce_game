import pygame
from setting import *
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True

pygame.display.set_caption("bounce_game")

class Ball():
    def __init__(self):
        self.x = 200
        self.y = 200

        self.radius = 10
        self.color = (255, 255, 255)
        
        self.diriction = [1, 1] # [x, y]
        self.speed = 5 

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    # move the ball ,rebounce on wall, change diriction
    def move(self):
        speed = self.speed
        self.x += self.diriction[0]*speed
        self.y += self.diriction[1]*speed

        if self.x + self.radius >= screen.get_width() or self.x-self.radius <= 0:
            self.diriction[0] *= -1
        if self.y + self.radius >= screen.get_height():
            fail()
        if self.y - self.radius <= 0:
            self.diriction[1] *= -1

        if self.x + self.radius >= board.get_x_y_length()[0] and self.x - self.radius <= board.get_x_y_length()[0] + board.get_x_y_length()[2]:
            if self.y + self.radius >= board.get_x_y_length()[1] and self.y - self.radius <= board.get_x_y_length()[1] + 10:
                self.diriction[1] *= -1

class Board():
    def __init__(self):
        self.x = 400
        self.y = 500
        self.length = 100

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

class Brick():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 10, 10))

def make_brick():
    for i in range()

is_fail = False

def fail():
    global is_fail
    is_fail = True

ball = Ball()
board = Board()

while running:
    time.sleep(1/FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not is_fail:
        ball.move()
        board.input(event)

        screen.fill((0, 0, 0), (0, 0, 800, 600))
        ball.draw(screen)
        board.draw(screen)
        
    else:
        font = pygame.font.SysFont(None, 50)
        text = font.render("You Fail!", True, (255, 255, 255))
        screen.blit(text, (400, 250))

    pygame.display.flip()

pygame.quit()