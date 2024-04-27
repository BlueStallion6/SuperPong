#Dupa ce instalezi importurile baga in consola "pip freeze > requirements.txt"
try:
    import os
    import pygame
    import colored
    from keywords import *
    import sys
    import resources.pygameResources as assets
    import screeninfo
    import json
    from screeninfo import get_monitors
except ImportError:
    print("ImportError >> Please run 'pip install -r requirements.txt' in this project's directory.")
    exit()

pygame.init()

try:
    open("config.json")
except FileNotFoundError:
    print_error("Config file not found, creating one...")
    with open("config.json", "a") as file:
        json.dump('{"settings":{"window_perc": null,"debug_mode": 1}}', file, indent=4)
        file.close()


pygame.display.set_caption('SuperPong')
clock = pygame.time.Clock()

monitors = get_monitors()
primary_monitor = monitors[0]

with open("config.json", "r") as file:
    config = json.load(file)
    # print_debug(str(config["settings"]))
    file.close()

if config["settings"]["window_perc"] is None:
    w_perc = int(input(f"{c_white}~Please specify the window size (1-100): {c_rst}"))
    if input(f"{c_white}~Do you want to save your selection for the next time? (y/n): ").lower() == "y":
        config["settings"]["window_perc"] = w_perc
        with open("config.json", "w") as file:
            # print_debug(str(config))
            json.dump(config, file, indent=4)
            file.close()
else:
    w_perc = config["settings"]["window_perc"] / 100

flags = pygame.HWSURFACE | pygame.DOUBLEBUF

DEBUG_MODE = config["settings"]["debug_mode"]
W_WIDTH = primary_monitor.width * w_perc
W_HEIGHT = primary_monitor.height * w_perc
PADDLE_WIDTH, PADDLE_HEIGHT = config["play_configs"]["paddle_width"] * w_perc, config["play_configs"]["paddle_height"] * w_perc
TPS = config["settings"]["tps"]
PADDLE_SPEED = config["play_configs"]["paddle_speed"] * w_perc

RP_MULT = 1
LP_MULT = 1

screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), flags)


class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, Colors.LIGHT_GRAY, (self.x, self.y, self.width, self.height))


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = config["play_configs"]["ball_radius"]

    def draw(self, win):
        pygame.draw.circle(win, Colors.WHITE, (self.x, self.y, self.radius))


left_paddle = Paddle(20, W_HEIGHT/2 - PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT * LP_MULT)
right_paddle = Paddle(W_WIDTH - 20 - PADDLE_WIDTH, W_HEIGHT/2 - PADDLE_HEIGHT/ 2, PADDLE_WIDTH, PADDLE_HEIGHT * RP_MULT)



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

    #Controls
    KEYS_PRESSED = pygame.key.get_pressed()
    if KEYS_PRESSED[pygame.K_UP]:
        if DEBUG_MODE: print_debug("Keydown: UP")
        if right_paddle.y > 0:
            right_paddle.y -= PADDLE_SPEED / TPS

    if KEYS_PRESSED[pygame.K_DOWN]:
        if DEBUG_MODE: print_debug("Keydown: DOWN")
        if right_paddle.y < W_HEIGHT - PADDLE_HEIGHT:
            right_paddle.y += PADDLE_SPEED / TPS

    if KEYS_PRESSED[pygame.K_w]:
        if DEBUG_MODE: print_debug("Keydown: W")
        if left_paddle.y > 0:
            left_paddle.y -= PADDLE_SPEED / TPS
    if KEYS_PRESSED[pygame.K_s]:
        if DEBUG_MODE: print_debug("Keydown: S")
        if left_paddle.y < W_HEIGHT - PADDLE_HEIGHT:
            left_paddle.y += PADDLE_SPEED / TPS


    #pygame.display.flip()
    pygame.display.update()

    #Set the ticks per second for the game
    clock.tick(TPS)





