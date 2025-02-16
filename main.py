import pygame
from setting import *
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True

pygame.display.set_caption("bounce_game")

class Ball():
    def __init__(self):
        self.x = 20
        self.y = 20

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
            self.diriction[1] *= -1
        if self.y - self.radius <= 0:
            fail()

def fail():
    global running
    running = False

ball = Ball()

while running:
    time.sleep(1/FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball.move()

    screen.fill((0, 0, 0), (0, 0, 800, 600))
    ball.draw(screen)
    pygame.display.flip()

pygame.quit()