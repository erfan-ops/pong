import pygame
from sys import exit

class Logic:
    def quit_game(self):
        pygame.quit()
        exit()
    
    
    def check_game_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.quit_game()
    
    
    def reset(self, *args) -> None:
        for obj in args:
            obj.reset()
        self.count_down(1.2)