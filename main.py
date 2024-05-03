#  MAIN FILE

try:
    import os
    from time import time
    from time import sleep
    import pygame
    import colored
    import sys
    import screeninfo
    import json
    import resources.pygameResources as assets
    from screeninfo import get_monitors
    from resources.pygameResources import sfx
    from keywords import *
    from Constants import *
    #import Power_ups
    #from Power_ups import *

except ImportError:
    print("ImportError >> Please run 'pip install -r requirements.txt' in this project's directory.")
    exit()

#################################################################################################################################################

#~WINDOW INIT~
pygame.init()
pygame.display.set_caption('SuperPong')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), FLAGS)
score_font = pygame.font.Font(".\\resources\\pong-score.ttf", size=CONFIG["settings"]["font_size"])

################################################################################################################################################

class PowerUp:
    def __init__(self):
        self.active = False
        self.activation_time = 0

    def activate(self):
        self.active = True
        self.activation_time = time()

    def deactivate(self):
        self.active = False
        self.activation_time = 0

    def is_active(self):
        return self.active

    def update(self):
        if self.active and time() - self.activation_time > 10:
            self.deactivate()

class Score_Multiplier(PowerUp):
    def effect_score_multiplier(self, score_inc):
        if self.is_active():
            return score_inc
        else:
            return 1


powerup_score_multiplier_left = Score_Multiplier()
powerup_score_multiplier_right = Score_Multiplier()


############################################################################################################################################

class Paddle:
    def __init__(self, x, y, width, height, side):
        self.x = x
        self.y = y
        self.side = side
        self.width = width
        self.height = height

    def draw_right(self, win):
        pygame.draw.rect(win, Colors.MEGA_LIGHT_BLUE, (self.x, self.y, self.width, self.height))

    def draw_left(self, win):
        pygame.draw.rect(win, Colors.MEGA_LIGHT_RED, (self.x, self.y, self.width, self.height))

left_paddle = Paddle(PADDLE_SPACING, W_HEIGHT/2 - (PADDLE_HEIGHT * LEFT_PADDLE_HEIGHT_MULT)/2, PADDLE_WIDTH, PADDLE_HEIGHT * LEFT_PADDLE_HEIGHT_MULT, "LEFT")
right_paddle = Paddle(W_WIDTH - PADDLE_SPACING - PADDLE_WIDTH, W_HEIGHT/2 - (PADDLE_HEIGHT * RIGHT_PADDLE_HEIGHT_MULT)/2, PADDLE_WIDTH, PADDLE_HEIGHT * RIGHT_PADDLE_HEIGHT_MULT, "RIGHT")

################################################################################################################################################################

ball_velocity_x = 1340 * W_PERC / TPS
ball_velocity_y = -100 * W_PERC / TPS
velocity_inc_rate = 1.8
velocity_inc_flat = 32 * W_PERC / TPS

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
            ball.y = W_HEIGHT - ball.radius
            ball.y_vel = ball.y_vel - (velocity_inc_flat / 2)
            sfx.play(assets.MARGIN_HIT_SOUND)
        elif ball.y - ball.radius <= 0:
            ball.y_vel *= -1
            ball.y = ball.radius
            ball.y_vel = ball.y_vel - (velocity_inc_flat / 2)
            sfx.play(assets.MARGIN_HIT_SOUND)


        #LEFT PADDLE COLLISION - 1/8 = upper side,  7/8 = lower side
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



            sfx.play(assets.PADDLE_HIT_SOUND)
            ball.x_vel *= - 1
            ball.x_vel += velocity_inc_flat
            ball.x = left_paddle.x + PADDLE_WIDTH + ball.radius + 1 * W_PERC


        if ball.x <= 0:   #Left_side
            RIGHT_SCORE.inc(1 * RIGHT_SCORE_INCREASE_MULT)
            ball.reset()
            ball.moving = False
            ball.x_vel = - ball_velocity_x
            ball.y_vel = ball_velocity_y
            sfx.play(assets.WIN_LOSE_ROUND_SOUND)


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
                ball.y_vel = 1 * ball_velocity_x - velocity_inc_flat

            sfx.play(assets.PADDLE_HIT_SOUND)
            ball.x_vel *= -1
            ball.x_vel -= velocity_inc_flat
            ball.x = right_paddle.x - ball.radius - 1 * W_PERC

        if ball.x >= right_paddle.x + PADDLE_WIDTH + PADDLE_SPACING:   #right_side
            LEFT_SCORE.inc(1 * RIGHT_SCORE_INCREASE_MULT)
            ball.reset()
            ball.moving = False
            ball.x_vel = ball_velocity_x
            ball.y_vel = ball_velocity_y
            sfx.play(assets.WIN_LOSE_ROUND_SOUND)


    def draw(self, screen):
        pygame.draw.circle(screen, Colors.LIGHT_GRAY, (self.x, self.y), self.radius, width = 0)

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
        score_surface = score_font.render(str(self.get()), False, Colors.WHITE)
        screen.blit(score_surface, (self.x, self.y))


LEFT_SCORE = Score(W_WIDTH // 2 - TEXT_SPACING - 17 * W_PERC, TEXT_UP)
RIGHT_SCORE = Score(W_WIDTH // 2 + TEXT_SPACING, TEXT_UP)
WAY_ARROW_SEM = 0

###############################################################################################################################################

midlines_draw = True
ball.moving = False
player_won = False

running = True
while running:
    screen.fill((10, 10, 15))

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

    left_paddle.draw_left(screen)
    right_paddle.draw_right(screen)
    ball.draw(screen)
    LEFT_SCORE.draw()
    RIGHT_SCORE.draw()

    Press_space_sem = True
    print_arrows = True

    # WINNING SITUATION
    if LEFT_SCORE.get() >= WINNING_SCORE or RIGHT_SCORE.get() >= WINNING_SCORE:

        if LEFT_SCORE.get() >= WINNING_SCORE:
            Winning_font = pygame.font.Font(".\\resources\\SuperDream-ax3vE.ttf", 78)
            Left_won_text = Winning_font.render("RED SIDE WON !", True, Colors.RED)
            Left_won_text.set_alpha(255)
            screen.blit(Left_won_text, (W_WIDTH // 2 - Left_won_text.get_width() // 2, W_HEIGHT // 3))


        else:
            Winning_font = pygame.font.Font(".\\resources\\SuperDream-ax3vE.ttf", 78)
            Right_won_text = Winning_font.render("BLUE SIDE WON !", True, Colors.BLUE)
            Right_won_text.set_alpha(255)
            screen.blit(Right_won_text, (W_WIDTH // 2 - Right_won_text.get_width() // 2, W_HEIGHT // 3))


        Continue_font = pygame.font.Font(".\\resources\\SuperDream-ax3vE.ttf", 48)
        Continue_text = Continue_font.render("Press SPACE to Restart", True, Colors.GRAY)
        Continue_text.set_alpha(148)
        screen.blit(Continue_text, (W_WIDTH // 2 - Continue_text.get_width() // 2, W_HEIGHT // 2 + W_HEIGHT// 8 ))
        print_arrows = False

        player_won = True
        Press_space_sem = False

        if player_won and pygame.key.get_pressed()[pygame.K_SPACE]:
            LEFT_SCORE.count = 0
            RIGHT_SCORE.count = 0
            ball.reset()
            ball.moving = False
            player_won = False
            Press_space_sem = True
            print_arrows = False


    if ball.moving:
        ball.move()
    else:

        Press_space_font = pygame.font.Font(".\\resources\\SuperDream-ax3vE.ttf", 48)
        Press_space_text = Press_space_font.render("PRESS SPACE TO START", True, Colors.GRAY)

        Way_line_right_font = pygame.font.Font(".\\resources\\SuperDream-ax3vE.ttf", 28)
        Way_line_right_text = Press_space_font.render(">>>", True, Colors.WAY_TOO_DARK_GRAY)

        Way_line_left_font = pygame.font.Font(".\\resources\\SuperDream-ax3vE.ttf", 28)
        Way_line_left_text = Press_space_font.render("<<<", True, Colors.WAY_TOO_DARK_GRAY)

        Press_space_text.set_alpha(236)

        if Press_space_sem:
            screen.blit(Press_space_text, (W_WIDTH // 2 - Press_space_text.get_width() // 2, W_HEIGHT // 5))

        if ball.x_vel < 0:
            WAY_ARROW_SEM = False  # Ball is moving left
        else:
            WAY_ARROW_SEM = True

        if print_arrows:
            if WAY_ARROW_SEM:
                screen.blit(Way_line_right_text, (W_WIDTH // 2 + 40 * W_PERC, W_HEIGHT // 2 - 30 * W_PERC))
            elif not WAY_ARROW_SEM:
                screen.blit(Way_line_left_text, (W_WIDTH // 2 - 115 * W_PERC, W_HEIGHT // 2 - 30 * W_PERC))



    # Controls
    KEYS_PRESSED = pygame.key.get_pressed()
    if KEYS_PRESSED[pygame.K_UP]:
        if DEBUG_MODE:
            # print_debug("Keydown: UP")
            print_debug(int(time() * 1000))
        if right_paddle.y > 0:
            right_paddle.y -= PADDLE_SPEED * RIGHT_PADDLE_SPEED_MULT / TPS
    if KEYS_PRESSED[pygame.K_DOWN]:
        if DEBUG_MODE: print_debug("Keydown: DOWN")
        if right_paddle.y < W_HEIGHT - PADDLE_HEIGHT:
            right_paddle.y += PADDLE_SPEED * RIGHT_PADDLE_SPEED_MULT / TPS

    if KEYS_PRESSED[pygame.K_w]:
        if DEBUG_MODE: print_debug("Keydown: W")
        if left_paddle.y > 0:
            left_paddle.y -= PADDLE_SPEED * LEFT_PADDLE_SPEED_MULT / TPS
    if KEYS_PRESSED[pygame.K_s]:
        if DEBUG_MODE: print_debug("Keydown: S")
        if left_paddle.y < W_HEIGHT - PADDLE_HEIGHT:
            left_paddle.y += PADDLE_SPEED * LEFT_PADDLE_SPEED_MULT / TPS

    if DEBUG_MODE:
        fps = clock.get_fps()
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {fps:.2f}", True, (170, 170, 170))
        screen.blit(fps_text, (10, 10))

    pygame.display.update()
    clock.tick(TPS)






