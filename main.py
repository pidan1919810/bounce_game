import pygame
from setting import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("bounce_game")

level.init()

clock = pygame.time.Clock()
while level.is_running():
    level.update_level(screen)
    
    clock.tick(FPS)

pygame.quit()