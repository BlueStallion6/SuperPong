#~MAIN FILE START
try:
    import os
    from time import time
    from time import sleep
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

#################################################################################################################################################

#~WINDOW INIT~
pygame.init()
pygame.display.set_caption('SuperPong')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), FLAGS)

################################################################################################################################################

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

###############################################################################################################################################

ball_velocity_x = 1330 * W_PERC / TPS
ball_velocity_y = -10 * W_PERC / TPS
velocity_inc_rate = 1.8
velocity_inc_flat = 30 * W_PERC / TPS

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.x_vel = ball_velocity_x
        self.y_vel = ball_velocity_y

    def reset(self):
        self.x = W_WIDTH // 2
        self.y = W_HEIGHT // 2

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


        if ball.y + ball.radius >= W_HEIGHT:  # lower barrier
            ball.y_vel *= -1
            ball.y_vel = ball.y_vel - (velocity_inc_flat / 2)
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1
            ball.y_vel = ball.y_vel - (velocity_inc_flat / 2)


        #LEFT PADDLE COLLISION - 1/7 = upper side,  6/7 = lower side
        if left_paddle.x - PADDLE_WIDTH <= ball.x - ball.radius <= left_paddle.x + left_paddle.width and left_paddle.y - ball.radius < ball.y < left_paddle.y + left_paddle.height + ball.radius:
            if ball.y < left_paddle.y + left_paddle.height * 1 / 8:
                ball.y_vel = (-1) * ball_velocity_x + velocity_inc_flat

            elif ball.y < left_paddle.y + left_paddle.height * 2 / 8:
                ball.y_vel = (-3/5) * ball_velocity_x

            elif ball.y < left_paddle.y + left_paddle.height * 3 / 8:
                ball.y_vel = (-3 / 10) * ball_velocity_x

            elif ball.y < left_paddle.y + left_paddle.height * 4 / 8:
                ball.y_vel = ball_velocity_y
            elif ball.y < left_paddle.y + left_paddle.height * 5 / 8:
                ball.y_vel = (3 / 10) * ball_velocity_x

            elif ball.y < left_paddle.y + left_paddle.height * 6 / 8:
                ball.y_vel = (3 / 5) * ball_velocity_x

            elif ball.y > left_paddle.y + left_paddle.height * 7 / 8:
                ball.y_vel = 1 * ball_velocity_x - velocity_inc_flat

            ball.x_vel *= - 1
            ball.x_vel += velocity_inc_flat
            ball.x = left_paddle.x + PADDLE_WIDTH + ball.radius + 1 * W_PERC

        if ball.x <= 0:   #Left_side
            RIGHT_SCORE.inc(1)
            ball.reset()
            ball.moving = False
            ball.x_vel = - ball_velocity_x
            ball.y_vel = - ball_velocity_y
            print_success(f"Score for the right: {LEFT_SCORE.get()} : {RIGHT_SCORE.get()}")


        #RIGHT PADDLE COLLISION
        if right_paddle.x + PADDLE_WIDTH >= ball.x + ball.radius >= right_paddle.x and right_paddle.y - ball.radius < ball.y  < right_paddle.y + right_paddle.height + ball.radius:

            if ball.y < right_paddle.y + right_paddle.height * 1 / 8:
                ball.y_vel = (-1) * ball_velocity_x + velocity_inc_flat

            elif ball.y < right_paddle.y + right_paddle.height * 2 / 8:
                ball.y_vel = (-3/5) * ball_velocity_x

            elif ball.y < right_paddle.y + right_paddle.height * 3 / 8:
                ball.y_vel = (-3 / 10) * ball_velocity_x
            elif ball.y < right_paddle.y + right_paddle.height * 4 / 8:
                ball.y_vel = ball_velocity_y

            elif ball.y < right_paddle.y + right_paddle.height * 5 / 8:
                ball.y_vel = (3 / 10) * ball_velocity_x

            elif ball.y < right_paddle.y + right_paddle.height * 6 / 8:
                ball.y_vel = (3 / 5) * ball_velocity_x

            elif ball.y > right_paddle.y + right_paddle.height * 7 / 8:
                ball.y_vel = (1) * ball_velocity_x - velocity_inc_flat

            ball.x_vel *= -1
            ball.x_vel -= velocity_inc_flat
            ball.x = right_paddle.x - ball.radius - 1 * W_PERC

        if ball.x >= right_paddle.x + PADDLE_WIDTH + PADDLE_SPACING:
            LEFT_SCORE.inc(1)
            ball.reset()
            ball.moving = False
            ball.x_vel = ball_velocity_x
            ball.y_vel = ball_velocity_y
            print_success(f"Score for the left: {LEFT_SCORE.get()} : {RIGHT_SCORE.get()}")

    def draw(self, screen):
        pygame.draw.circle(screen, Colors.LIGHTER_GRAY, (self.x, self.y), self.radius, width = 0)

ball = Ball(W_WIDTH // 2, W_HEIGHT // 2, BALL_RADIUS)

###################################################################################################################################################################################

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

    def draw(self):
        a = 0

LEFT_SCORE = Score(0, 0)
RIGHT_SCORE = Score(0, 0)

###############################################################################################################################################

midlines_draw = False
ball.moving = False
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


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball.moving = True
                midlines_draw = True

    # Draws

    if midlines_draw:
        for i in range(0, MID_LINES_COUNT):
            LINE_START = i * 2 * W_HEIGHT / (MID_LINES_COUNT * 2)
            LINE_END = (i * 2 + 1) * W_HEIGHT / (MID_LINES_COUNT * 2)
            pygame.draw.line(screen, Colors.WAY_TOO_DARK_GRAY, (W_WIDTH/2, LINE_START), (W_WIDTH/2, LINE_END), 2)

    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)
    if ball.moving:
        ball.move()

    # Controls
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







    #Set the ticks per second for the game
    pygame.display.update()
    clock.tick(TPS)






