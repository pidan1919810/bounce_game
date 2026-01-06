import pygame
from setting import BOARD_LENGTH

class Board():
    def __init__(self):
        self.x = 0
        self.y = 500
        self.length = BOARD_LENGTH

        self.color = (255,100,100)

    def get_x(self) -> int:
        return self.x
    def get_y(self) -> int:
        return self.y
    def get_length(self) -> int:
        return self.length

    def update(self, event):
        print(event)
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.x -= 10
            if event.key == pygame.K_RIGHT:
                self.x += 10

        if event.type == pygame.TEXTINPUT:
            if event.text == 'a':
                self.x -= 10
            if event.text == 'd':
                self.x += 10

        if self.x+self.length >= 800:
            self.x = 800 - self.length
        if self.x <= 0:
            self.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, 10))

board = Board()