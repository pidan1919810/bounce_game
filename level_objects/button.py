import pygame, enum, types
from .base_object import Base_object
from easy_types import *

class Button(Base_object):
    class Status(enum.Enum):
        normal = 1
        enter = 2
        clicked = 3
        
    status:Status
    events:types.FunctionType
    
    w: float
    h: float
    text:str
    on_or_off:bool
    click_on:bool
    
    def __init__(
        self, 
        x:float, 
        y:float, 
        w:float, 
        h:float, 
        text:str = '', 
        on_or_off=False
    ) -> None:
        
        super().__init__(x,y)
        self.w: float = w
        self.h: float = h
        
        self.status = self.Status.normal
        
        self.text = text
        self.on_or_off = on_or_off #Call the events when click on(True) or after click on
        self.click_on = False
        
    def get_rect(self) -> Rect:
        return Rect(self.x, self.y, self.w, self.h)
        
    def add_event(self, event:types.FunctionType) -> None:
        self.event = event
        
    def is_enter(self, x, y) -> bool:
        return x > self.x and x < self.x+self.w and y > self.y and y < self.y + self.h
    
    def is_click(self, event:pygame.event.Event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN
                    
    def draw(self, screen:pygame.Surface) -> None:
        if self.status == self.Status.enter:
            #print("enter")
            screen.fill(pygame.color.Color(255,100,0), self.get_rect())
        else:
            screen.fill("white", self.get_rect())
            
        if self.text != '':
            from setting import TEXT_FONT
            font = pygame.font.Font(TEXT_FONT,22)
            
            max_width = self.w - 2
            current_line = ''
            lines = []
            for char in self.text:
                # 检查当前行加上新字符是否超出最大宽度
                test_line = current_line + char
                test_width, _ = font.size(test_line)
                if test_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)  # 将当前行加入列表
                    current_line = char  # 开始新的一行

            lines.append(current_line)
            
            y = (self.h-4)/(len(lines)+1)-font.size(lines[0])[1]/2
            for t in lines:
                t_s: pygame.Surface = font.render(t, True, (0,0,0))
                screen.blit(t_s,(self.x+(self.w-4-t_s.get_size()[0])//2, self.y+y))
                y += font.size(t)[1] + 2
        
    def update(self, events:list[pygame.event.Event]) -> None:
        for event in events:
            self.status = self.Status.normal
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #print(self.status)
            if self.on_or_off:
                if self.is_enter(mouse_x, mouse_y):
                    self.status = self.Status.enter
                    if self.is_click(event):
                        self.status = self.Status.clicked
                        self.on_click()
            else:
                if self.is_enter(mouse_x, mouse_y):
                    self.status = self.Status.enter
                    if self.is_click(event):
                        self.click_on = True
                    if not self.is_click(event) and self.click_on:
                        self.click_on = False
                        self.status = self.Status.clicked
                        self.on_click()
                else:
                    self.click_on = False

    def on_click(self) -> None:
        self.event()
        
    def set_text(self, text:str):
        self.text = text