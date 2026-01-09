from typing import List
import pygame
from pygame.event import Event
from level_objects.base_object import Base_object
from setting import *
from level_objects.ball import ball_manager, Normal_ball
from level_objects.board import board
from level_objects.brick import brick_manager, Brick
from level_objects.button import Button

restart_button:Button
running:bool = True
objects:list = []
score:int = 0

def init() -> None:
    global score, objects, restart_button
    score = 0
    
    brick_manager.clear()
    brick_manager.init()
    
    ball_manager.clear()
    ball_manager.init()
    
    objects.clear()
    objects.append(brick_manager)
    
    ball_manager.clear()
    objects.append(ball_manager)
    ball_manager.extend(Normal_ball, (300, BOARD_Y-40))
    
    objects.append(board)
    
    restart_button = Button(225,400,150,50)
    restart_button.set_text("再来一次")
    restart_button.add_event(init)


def is_running() -> bool:
    return running

def add_score(addend:int) -> None:
    global score
    score += addend


def in_game(screen:pygame.Surface, events:list[pygame.event.Event]) -> None:
    for object in objects:
        object.update(events)
        
    for object in objects:
        object.draw(screen)
        
    fonts = pygame.font.Font(TEXT_FONT, IN_GAME_TEXT_SIZE)
    text = fonts.render(f"Score:{score}", False, (128,128,128))
    screen.blit(text,(0,0))


def failed_screen(screen:pygame.Surface) -> None:
    for object in objects:
        object.draw(screen)

    fonts = pygame.font.Font(TEXT_FONT, FAILED_TEXT_SIZE)
    text = fonts.render("你输了", False, (128,128,128))
    screen.blit(text,(200,350))
    
    restart_button.draw(screen)


def won_screen(screen:pygame.Surface) -> None:
    for object in objects:
        object.draw(screen)

    fonts = pygame.font.Font(TEXT_FONT, WON_TEXT_SIZE)
    text = fonts.render("你赢了", False, (128,128,128))
    screen.blit(text,(200,350))
    
    restart_button.draw(screen)


def is_fail() -> bool:
    #return True
    if ball_manager.get_cout() < 1:
        return True
    else:
        return False
    
def is_win() -> bool:
    if brick_manager.get_brick_cout() <= 0:
        return True
    else:
        return False

def update_level(screen:pygame.Surface) -> None:
    global running
    events: List[Event] = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if cheat.SPAWN_ELEMENT:
                    if event.key == pygame.K_l:
                        brick_manager.new_line()
                        
    screen.fill((0, 0, 0))

    if is_fail():
        restart_button.update(events)
        failed_screen(screen)
    elif is_win():
        restart_button.update(events)
        won_screen(screen)
    else:
        in_game(screen, events)
    
    pygame.display.flip()