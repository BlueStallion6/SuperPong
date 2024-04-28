#~MAIN FILE START
try:
    import os
    from time import time
    import pygame
    import colored
    import sys
    import screeninfo
    import json
    from screeninfo import get_monitors

    import resources.pygameResources as assets
    from keywords import *
    from Constants import *
except ImportError:
    print("ImportError >> Please run 'pip install -r requirements.txt' in this project's directory.")
    exit()

##########################################################################################################################################
#~WINDOW INIT~
pygame.init()
pygame.display.set_caption('SuperPong')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), FLAGS)
##########################################################################################################################################

if CONFIG["settings"]["window_perc"] is None:
    W_PERC = int(input(f"{c_white}~Please specify the window size (1-100): {c_rst}"))
    if input(f"{c_white}~Do you want to save your selection for the next time? (y/n): ").lower() == "y":
        CONFIG["settings"]["window_perc"] = W_PERC
        with open("config.json", "w") as file:
            # print_debug(str(config))
            json.dump(CONFIG, file, indent=4)
            file.close()


class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, Colors.LIGHT_GRAY, (self.x, self.y, self.width, self.height))


left_paddle = Paddle(PADDLE_SPACING, W_HEIGHT/2 - PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT * LP_HEIGHT_MULT)
right_paddle = Paddle(W_WIDTH - PADDLE_SPACING - PADDLE_WIDTH, W_HEIGHT/2 - PADDLE_HEIGHT/ 2, PADDLE_WIDTH, PADDLE_HEIGHT * RP_HEIGHT_MULT)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = CONFIG["play_configs"]["ball_radius"]

    def draw(self, win):
        pygame.draw.circle(win, Colors.WHITE, (self.x, self.y, self.radius))

class Score:
    def __init__(self, x, y):
        self.count = 0
        self.x = x
        self.y = y

    def get(self):
        return self.count

    def inc(self, amount):
        self.count += amount

    def dec(self, amount):
        self.count -= amount

running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print_success("Closing the game...")
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print_success("Closing the game...")
                pygame.quit()
                exit()

    left_paddle.draw(screen)
    right_paddle.draw(screen)
    for i in range(0, MID_LINES_COUNT):
        LINE_START = i * 2 * W_HEIGHT / (MID_LINES_COUNT * 2)
        LINE_END = (i * 2 + 1) * W_HEIGHT / (MID_LINES_COUNT * 2)
        pygame.draw.line(screen, Colors.WAY_TOO_DARK_GRAY, (W_WIDTH/2, LINE_START), (W_WIDTH/2, LINE_END), 2)

    #Controls
    KEYS_PRESSED = pygame.key.get_pressed()
    if KEYS_PRESSED[pygame.K_UP]:
        if DEBUG_MODE:
            # print_debug("Keydown: UP")
            print_debug(int(time() * 1000))
        if right_paddle.y > 0:
            right_paddle.y -= PADDLE_SPEED * RP_SPEED_MULT / TPS

    if KEYS_PRESSED[pygame.K_DOWN]:
        if DEBUG_MODE: print_debug("Keydown: DOWN")
        if right_paddle.y < W_HEIGHT - PADDLE_HEIGHT:
            right_paddle.y += PADDLE_SPEED * RP_SPEED_MULT / TPS

    if KEYS_PRESSED[pygame.K_w]:
        if DEBUG_MODE: print_debug("Keydown: W")
        if left_paddle.y > 0:
            left_paddle.y -= PADDLE_SPEED * LP_SPEED_MULT / TPS
    if KEYS_PRESSED[pygame.K_s]:
        if DEBUG_MODE: print_debug("Keydown: S")
        if left_paddle.y < W_HEIGHT - PADDLE_HEIGHT:
            left_paddle.y += PADDLE_SPEED * LP_SPEED_MULT / TPS


    #pygame.display.flip()
    pygame.display.update()

    #Set the ticks per second for the game
    clock.tick(TPS)






