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