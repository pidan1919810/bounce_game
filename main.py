import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255), (0, 0, 800, 600))
    pygame.display.flip()

pygame.quit()