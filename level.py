import pygame
from level_objects.base_object import Base_object
from setting import FAILED_TEXT_SIZE, IN_GAME_TEXT_SIZE, TEXT_FONT, WON_TEXT_SIZE
from level_objects.ball import ball_manager, Normal_ball
from level_objects.board import board
from level_objects.brick import brick_manager, Brick

running:bool = True
objects:list = []
score:int = 0

def init() -> None:
    global score, objects
    score = 0
    
    objects.clear()
    objects.append(brick_manager)
    
    ball_manager.clear()
    objects.append(ball_manager)
    ball_manager.extend(Normal_ball,(300,500))
    
    objects.append(board)

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
        
    fonts = pygame.font.SysFont(TEXT_FONT, IN_GAME_TEXT_SIZE)
    text = fonts.render(f"Score:{score}", False, (128,128,128))
    screen.blit(text,(0,0))
        
def failed_screen(screen:pygame.Surface) -> None:
    for object in objects:
        object.draw(screen)

    fonts = pygame.font.SysFont(TEXT_FONT, FAILED_TEXT_SIZE)
    text = fonts.render("你输了", False, (128,128,128))
    screen.blit(text,(200,400))
    
def won_screen(screen:pygame.Surface) -> None:
    for object in objects:
        object.draw(screen)

    fonts = pygame.font.SysFont(TEXT_FONT, WON_TEXT_SIZE)
    text = fonts.render("你赢了", False, (128,128,128))
    screen.blit(text,(200,400))
    
def is_fail() -> bool:
    if ball_manager.get_cout() < 1:
        return True
    else:
        return False
    
def is_win() -> bool:
    if brick_manager.get_brick_cout() <= 0:
        return True
    else:
        return False

def update_level(screen) -> None:
    global running
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0, 0, 0))

    if is_fail():
        failed_screen(screen)
    elif is_win():
        won_screen(screen)
    else:
        in_game(screen, events)

    pygame.display.flip()