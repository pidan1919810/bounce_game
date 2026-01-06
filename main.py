import pygame
from setting import *
import level
import time
import random

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))

running = True

pygame.display.set_caption("bounce_game")





class effect_ball():
    def __init__(self, effect:str):
        self.effect:str = effect
        self.x = random.randint(0,800)
        self.y = 0
    
    def draw(self):
        pygame.draw




is_fail = False

def fail():
    global is_fail
    is_fail = True

def is_win():
    if len(brick_list) == 0:
        return True



make_brick()

coutner = 0
time_start = 0
while running:
    time.sleep(1/FPS)
    level.update_level(screen)

    

pygame.quit()