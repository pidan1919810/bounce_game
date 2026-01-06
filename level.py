import pygame
from setting import SCREEN_HEIGHT, SCREEN_WIDTH
from level_objects.ball import ball_manager
from level_objects.board import board
from level_objects.brick import brick_manager

running:bool = True
objects:list = []

def init() -> None:
    objects.append(brick_manager)
    
    objects.append(ball_manager)
    ball_manager.extend(1)
    
    objects.append(board)

def is_running() -> bool:
    return running

def in_game() -> None:
    pass

def update_level(screen) -> None:
    global running
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    for object in objects:
        object.update(events)

    screen.fill((0, 0, 0))

    for object in objects:
        object.draw(screen)

    pygame.display.flip()