import pygame
from sys import exit
from random import choice

#########################################################
#                        _oo0oo_                        #
#                       o8888888o                       #
#                       88" . "88                       #
#                       (| -_- |)                       #
#                       0\  =  /0                       #
#                     ___/`---'\___                     #
#                   .' \|     |// '.                    #
#                  / \|||  :  |||// \                   #
#                 / _||||| -:- |||||- \                 #
#                |   | \\  -  /// |   |                 #
#                | \_|  ''\---/''  |_/ |                #
#                \  .-\__  '-'  ___/-. /                #
#              ___'. .'  /--.--\  `. .'___              #
#           ."" '<  `.___\_<|>_/___.' >' "".            #
#          | | :  `- \`.;`\ _ /`;.`/ - ` : | |          #
#          \  \ `_.   \_ __\ /__ _/   .-` /  /          #
#      =====`-.____`.___ \_____/___.-`___.-'=====       #
#                        `=---='                        #
#########################################################

pygame.init()

WIDTH = 1100
HEIGHT = 750
FPS = 120
CLOCK = pygame.time.Clock()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('JDPong')

GREY = pygame.Color('grey')
GAME_FONT = pygame.font.Font('VINERITC.TTF', 45)


class Paddle:
    def __init__(self, type_: str):
        self.type = type_
        if self.type == 'Player':
            self.rect = pygame.Rect(10, HEIGHT / 2 - 60, 10, 120)
        elif self.type == 'AI':
            self.rect = pygame.Rect(WIDTH - 20, HEIGHT / 2 - 60, 10, 120)
        self.vel = 0
        self.score = 0

    def draw(self, ball):
        pygame.draw.rect(WIN, GREY, self.rect)
        self.move(ball)

    def move(self, ball):
        if self.type == 'Player':
            self.rect.y += self.vel
        elif self.type == 'AI' and ball.rect.x > WIDTH / 2 and ball.xvel > 0:
            if self.rect.top <= ball.rect.y:
                self.rect.y += 2
            elif self.rect.bottom >= ball.rect.y:
                self.rect.y -= 2
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH / 2 - 16, HEIGHT / 2 - 16, 32, 32)
        self.xvel = 0
        self.yvel = 0

    def draw(self):
        pygame.draw.ellipse(WIN, GREY, self.rect)
        pygame.draw.aaline(WIN, GREY, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
        self.move()

    def move(self):
        self.rect.centerx += self.xvel
        self.rect.centery += self.yvel
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.yvel = -self.yvel

    def check_hit(self, pd1: Paddle, pd2: Paddle):
        if self.rect.left <= 0:
            pd1.score += 1
            self.__init__()
        elif self.rect.right >= WIDTH:
            pd2.score += 1
            self.__init__()

        if self.rect.colliderect(pd1) or self.rect.colliderect(pd2):
            self.xvel = -self.xvel


def main():
    running = True

    ball = Ball()
    player = Paddle('Player')
    ai = Paddle('AI')

    def draw_win():
        WIN.fill((0, 0, 0))

        player.draw(ball)
        ai.draw(ball)

        ball.draw()
        ball.check_hit(player, ai)

        player_scr = GAME_FONT.render(f'{player.score}', False, GREY)
        ai_scr = GAME_FONT.render(f'{ai.score}', False, GREY)
        WIN.blit(ai_scr, (WIDTH / 2 - ai_scr.get_width() / 2 - 30, HEIGHT / 2 - ai_scr.get_height() / 2))
        WIN.blit(player_scr, (WIDTH / 2 - player_scr.get_width() / 2 + 30, HEIGHT / 2 - player_scr.get_height() / 2))

    while running:
        CLOCK.tick(FPS)
        pygame.display.update()
        draw_win()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.vel = -3
                if event.key == pygame.K_DOWN:
                    player.vel = 3
                if event.key == pygame.K_SPACE and ball.xvel == 0 and ball.yvel == 0:
                    ball.xvel = 3 * choice([1, -1])
                    ball.yvel = 4 * choice([1, -1])
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    player.vel = 0


if __name__ == '__main__':
    main()
