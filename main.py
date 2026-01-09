import pygame
from setting import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import level

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Brick Breaker")

level.init()

clock = pygame.time.Clock()
while level.is_running():
    level.update_level(screen)
    
    clock.tick(FPS)

pygame.quit()