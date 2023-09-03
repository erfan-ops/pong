from settings import *
import pygame
from time import sleep

class Screen:
    def __init__(self) -> None:
        self.width_ratio = SCREEN_WIDTH/1920
        self.height_ratio = SCREEN_HEIGHT/1080
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))
        self.bg_color = BG_COLOR
    
    
    def render(self, *args) -> None:
            for obj in args:
                self.screen.blit(obj.img, obj.rect)
    
    
    def start_screen(self) -> None:
        loading_img = pygame.image.load("assets/loading_screen.png").convert()
        size = loading_img.get_size()
        width_ratio = SCREEN_WIDTH/size[0]
        loading_img = pygame.transform.rotozoom(loading_img, 0, width_ratio)
        loading_img_rect = loading_img.get_rect()
        loading_line_width = 0
        space_from_edge = SCREEN_WIDTH/12
        line_rect = [space_from_edge, SCREEN_HEIGHT-SCREEN_HEIGHT/8, loading_line_width, 20]
        self.screen.fill("#000000")
        self.screen.blit(loading_img, loading_img_rect)
        pygame.display.flip()
        while True:
            self.check_game_quit()
            self.get_fps()
            pygame.draw.rect(self.screen, "#ffffff", line_rect)
            line_rect[2] += 360*width_ratio/self.FPS
            pygame.display.update(line_rect)
            self.clock.tick(self.FPS)
            if line_rect[2] >= SCREEN_WIDTH-(space_from_edge)*2:
                del loading_img
                return None
    
    
    def count_down(self, c_speed:float):
            c_speed /= 3
            for i in range(3, 0, -1):
                self.check_game_quit()
                self.screen.fill(self.bg_color)
                timer = self.timer_font.render(str(i), True, "#ffffff")
                timer_rect = timer.get_rect()
                self.screen.blit(timer, (int(SCREEN_WIDTH/2-timer_rect.width/2), int(SCREEN_HEIGHT/2-timer_rect.height/2)))
                pygame.display.flip()
                sleep(c_speed)
    
    
    def show_score(self, score_img: pygame.Surface, score_rect: pygame.Rect):
        self.screen.blit(score_img, (int(SCREEN_WIDTH/2-score_rect.width/2), SCREEN_HEIGHT//27))
        pygame.display.flip()