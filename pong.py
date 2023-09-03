import pygame
from settings import *
from random import choice, randint
from sys import exit as sysExit
from win32api import EnumDisplaySettings, EnumDisplayDevices
from screen import Screen
from gameObjects import *
from logic import Logic



class Game(Screen, Logic):
    def __init__(self) -> None:
        pygame.init()
        super().__init__()
        self.font = pygame.font.Font("fonts/Kablammo-Regular-VariableFont_MORF.ttf", 50)
        self.timer_font = pygame.font.Font("fonts/Kablammo-Regular-VariableFont_MORF.ttf", 200)
        self.clock = pygame.time.Clock()
        self._REFRESH_RATE: int = EnumDisplaySettings(EnumDisplayDevices().DeviceName, -1).DisplayFrequency
        self.TARGET_FPS = self._REFRESH_RATE
    
    
    def get_fps(self):
        self.FPS = self.clock.get_fps() if self.clock.get_fps() > 30 else float(self._REFRESH_RATE)
    

    def main(self) -> None:
        pygame.mouse.set_visible(False)
        
        # --variables-- #
        score_color = "#ffffff"
        
        # --sounds-- #
        start_game_sound: pygame.mixer.Sound = pygame.mixer.Sound("sounds/start.wav")
        collide_sound: pygame.mixer.Sound = pygame.mixer.Sound("sounds/collide.wav")
        lose_sound: pygame.mixer.Sound = pygame.mixer.Sound("sounds/lost.wav")
        win_sounds: tuple[pygame.mixer.Sound, pygame.mixer.Sound, pygame.mixer.Sound] = (pygame.mixer.Sound("sounds/won.wav"),
                                                                                         pygame.mixer.Sound("sounds/won2.wav"),
                                                                                         pygame.mixer.Sound("sounds/won3.wav"))
        
        # --colors-- #
        WHITE = "#ffffff"
        GREEN = "#20ff40"
        RED = "#ff3020"
        
        # game objects #
        # --paddles-- #
        SPACE_FROM_EDGE = SCREEN_WIDTH // PADDLE_SPACING
        player = Paddle((SCREEN_WIDTH - (SCREEN_WIDTH//SPACE_FROM_EDGE), SCREEN_HEIGHT//2), P_SPEED, P_SIZE)
        
        opponent = Paddle((SCREEN_WIDTH//SPACE_FROM_EDGE, SCREEN_HEIGHT//2), O_SPEED, O_SIZE)
        opponent.img = pygame.transform.flip(opponent.img, True, False)
        opponent.target = randint(0, opponent.rect.height)
        
        # --balls?-- #
        ball = Ball(BALL_SIZE)
        
        # --more variables-- #
        score_img = self.font.render(f"{opponent.score} | {player.score}", True, score_color)
        score_rect = score_img.get_rect()
        

        # game loop #
        start_game_sound.play()
        self.start_screen()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_RETURN:
                        player.is_going_up = False
                    
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_LSHIFT:
                        player.is_going_down = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_RETURN:
                        player.is_going_up = True
                    
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s or event.key == pygame.K_LSHIFT:
                        player.is_going_down = True
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_game()
                    
                    elif event.key == pygame.K_BACKQUOTE:
                        self.reset(ball, player, opponent)
                        player.score = 0
                        opponent.score = 0
                        score_img = self.font.render(f"{opponent.score} | {player.score}", True, score_color)
                        score_rect = score_img.get_rect()
                        score_color = WHITE
            
            
            self.get_fps()
            
            # rendering onjects
            self.screen.fill(self.bg_color)
            self.render(player,
                        opponent,
                        ball)
            self.show_score(score_img, score_rect)
            
            
            player.init(self.FPS)
            opponent.init(self.FPS)
            ball.init(self.FPS)
            
            if player.is_going_up and player.rect.top > 0:
                player.up()
            elif player.is_going_down and (not player.is_going_up) and player.rect.bottom < SCREEN_HEIGHT:
                player.down()
            
            
            # *bot AI* #
            if not ball.go_right:
                if ball.rect.top < opponent.rect.top + opponent.target and opponent.rect.top > 0:
                    opponent.up()
                elif ball.rect.bottom > opponent.target and opponent.rect.bottom < SCREEN_HEIGHT:
                    opponent.down()



            if ball.go_right:
                ball.rect.x += ball.speed_x
            else:
                ball.rect.x -= ball.speed_x
            ball.rect.y += ball.speed_y
            
            
            if ball.rect.bottom >= SCREEN_HEIGHT:
                ball.default_speed_y = -abs(ball.default_speed_y)
                collide_sound.play()
            elif ball.rect.top <= 0:
                ball.default_speed_y = abs(ball.default_speed_y)
                collide_sound.play()
            
            
            if ball.rect.collideobjectsall([player.rect, opponent.rect]):
                collide_sound.play()
                ball.default_speed_x += 1
                if ball.rect.colliderect(player.rect) and ball.go_right:
                    ball.calc_angle(player.rect)
                    ball.go_right = False
                
                elif ball.rect.colliderect(opponent.rect) and not ball.go_right:
                    ball.calc_angle(opponent.rect)
                    ball.go_right = True
                    print(opponent.target)
                    opponent.target = randint(0, opponent.rect.height)
            
            
            elif ball.rect.right >= SCREEN_WIDTH or ball.rect.left <= 0:
                if ball.rect.right >= SCREEN_WIDTH:
                    opponent.score += 1
                    lose_sound.play()
                elif ball.rect.left <= 0:
                    player.score += 1
                    choice(win_sounds).play()
                
                self.reset(ball, player, opponent)
                
                if player.score > opponent.score:
                    score_color = GREEN
                elif player.score < opponent.score:
                    score_color = RED
                else:
                    score_color = WHITE
                
                score_img = self.font.render(f"{opponent.score} | {player.score}", True, score_color)
                score_rect = score_img.get_rect()
            
            
            pygame.display.flip()
            self.clock.tick(self.TARGET_FPS)


if __name__ == "__main__":
    pong = Game()
    pong.main()
