import pygame
from pygame import Vector2
from setting import BOARD_LENGTH, SCREEN_WIDTH, BOARD_MOVEING_SPEED

class Board():
    def __init__(self) -> None:
        self.x:float = 0
        self.y:float = 600
        self.move_delta:pygame.Vector2 = Vector2(0,0)
        self.speed:float = BOARD_MOVEING_SPEED
        self.length = BOARD_LENGTH

        self.color = (255,100,100)

    def get_x(self) -> float:
        return self.x
    def get_y(self) -> float:
        return self.y
    def get_length(self) -> float:
        return self.length

    def update(self, events:list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_delta = Vector2(-1,0)
                if event.key == pygame.K_RIGHT:
                    self.move_delta = Vector2(1,0)
            if event.type == pygame.KEYUP:
                self.move_delta = Vector2(0,0)
                
        self.move()
                
    def move(self) -> None:
        self.x += self.speed * self.move_delta.x
        
        if self.x+self.length >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.length
        if self.x <= 0:
            self.x = 0

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, 10))

board = Board()