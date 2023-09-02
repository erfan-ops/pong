from settings import *
import pygame

class Screen:
    def __init__(self) -> None:
        self.width_ratio = SCREEN_WIDTH/1920
        self.height_ratio = SCREEN_HEIGHT/1080
        self.screen = pygame.display.set_mode(RES)
        self.bg_color = BG_COLOR
    
    
    def render(self, *args) -> None:
            self.screen.fill(self.bg_color)
            for obj in args:
                self.screen.blit(obj.img, obj.rect)