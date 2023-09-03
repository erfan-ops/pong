from screen import Screen
from settings import *
from random import choice
import pygame

class Paddle(Screen):
    def __init__(self, pos: list, speed: int|float, size: int|float) -> None:
        super().__init__()
        self.DEFAULT_SPEED: float = SCREEN_HEIGHT/1080*speed
        self.img: pygame.Surface = pygame.image.load("assets/paddle.png").convert_alpha()
        self.img: pygame.Surface = pygame.transform.rotozoom(self.img, 0, size*self.height_ratio/self.img.get_height())
        self.rect: pygame.Rect = self.img.get_rect()
        self.position: tuple = pos
        self.is_going_up: bool = False
        self.is_going_down: bool = False
        self.score = 0
        self.reset()
    
    
    def init(self, fps):
        self.speed = 60 / fps * self.DEFAULT_SPEED
    
    
    def up(self) -> None:
        self.rect.y -= self.speed
    
    
    def down(self) -> None:
        self.rect.y += self.speed
    
    
    def reset(self) -> None:
        self.rect.center = self.position
        self.is_going_down = False
        self.is_going_up = False


class Ball(Screen):
    def __init__(self, size: int|float) -> None:
        super().__init__()
        self.img = pygame.image.load("assets/ball.png").convert_alpha()
        self.img = pygame.transform.rotozoom(self.img, 0, size*self.height_ratio/self.img.get_height())
        self.rect: pygame.Rect = self.img.get_rect()
        self.max_y_speed: int|float = 38*self.height_ratio
        self.default_speed_x: float = BALL_SPEED*self.width_ratio
        self.default_speed_y: float = 0
        self.reset()
    
    
    def init(self, fps):
        self.speed_x = 60 / fps * self.default_speed_x
        self.speed_y = 60 / fps * self.default_speed_y
    
    
    def reset(self) -> None:
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.default_speed_y = 0
        self.go_right: bool = choice((True, False))
        self.default_speed_x = 15*self.width_ratio
    
    
    def calc_angle(self, collide_rect: pygame.Rect) -> None:
        min = collide_rect.top
        size = collide_rect.bottom - min
        collide_point = self.rect.center[1] - min
        self.default_speed_y = collide_point/size*self.max_y_speed - self.max_y_speed/2