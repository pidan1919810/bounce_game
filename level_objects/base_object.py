import pygame
from pygame.event import Event
from typing import Self
from abc import ABC, abstractmethod


class Base_object(ABC):
    """
        定义了所有的物体基类
    """
    x:float
    y:float
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
    
    @abstractmethod
    def draw(self, screen:pygame.Surface) -> None:
        pass
    
    @abstractmethod
    def update(self, events:list[Event]) -> None:
        pass
    
    @classmethod
    def create(cls, x:float, y:float) -> Self:
        return cls(x,y)
    
    def get_x(self) -> float:
        return self.x
    def get_y(self) -> float:
        return self.y
    def get_pos(self) -> pygame.Vector2:
        return pygame.Vector2(self.x, self.y)
    
class Base_image(Base_object, ABC):
    """
        包含了渲染图片的的逻辑
        未实现
    """