import pygame
from level_objects.ball import Ball
from level_objects.board import Board

running:bool = True
objects:list = []

board = Board()

def init():
    pass

def is_failed():
    return running

def in_game():
    

def update_level(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False

    for object in objects:
        object.update(event)

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

    pygame.display.flip()