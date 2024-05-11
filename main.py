#  MAIN FILE
try:
    import os
    import time
    import pygame
    import colored
    import sys
    import screeninfo
    import json
    import resources.pygameResources as assets
    import threading
    from screeninfo import get_monitors
    from resources.pygameResources import sfx
    from keywords import *
    from Constants import *

except ImportError:
    print("ImportError >> Please run 'pip install -r requirements.txt' in this project's directory.")
    exit()

#######################################################################################################################

#~WINDOW INIT~
pygame.init()
pygame.display.set_caption('SuperPong')
clock = pygame.time.Clock()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT), FLAGS)
score_font = pygame.font.Font(".\\resources\\pong-score.ttf", size=CONFIG["settings"]["font_size"])
running = True
leftPowerupList = ["Score Multiplier", "Enlarge Paddle", "Paddle Speed Boost"]
rightPowerupList = ["Score Multiplier", "Enlarge Paddle", "Paddle Speed Boost"]

######################################################################################################################

class Paddle:
    def __init__(self, x, y, width, height, side, speed):
        self.x = x
        self.y = y
        self.side = side
        self.width = width
        self.height = height
        self.speed = speed

    def draw_right(self, win):
        pygame.draw.rect(win, Colors.MEGA_LIGHT_BLUE, (self.x, self.y, self.width, self.height))

    def draw_left(self, win):
        pygame.draw.rect(win, Colors.MEGA_LIGHT_RED, (self.x, self.y, self.width, self.height))

left_paddle = Paddle(LEFT_PADDLE_SPACING, W_HEIGHT/2 - (PADDLE_HEIGHT * LEFT_PADDLE_HEIGHT_MULT)/2, PADDLE_WIDTH, PADDLE_HEIGHT * LEFT_PADDLE_HEIGHT_MULT, "LEFT", PADDLE_SPEED)
right_paddle = Paddle(W_WIDTH - RIGHT_PADDLE_SPACING - PADDLE_WIDTH, W_HEIGHT/2 - (PADDLE_HEIGHT * RIGHT_PADDLE_HEIGHT_MULT)/2, PADDLE_WIDTH, PADDLE_HEIGHT * RIGHT_PADDLE_HEIGHT_MULT, "RIGHT", PADDLE_SPEED)

#######################################################################################################################

ball_velocity_x = 1340 * W_PERC / TPS
ball_velocity_y = -100 * W_PERC / TPS
velocity_inc_rate = 1.8
velocity_inc_flat = 32 * W_PERC / TPS
right_score_increment = 0
left_score_increment = 0

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
            RIGHT_SCORE.inc(1 + right_score_increment)
            ball.reset()
            ball.moving = False
            ball.x_vel = - ball_velocity_x
            ball.y_vel = ball_velocity_y
            sfx.play(assets.WIN_LOSE_ROUND_SOUND)

        #RIGHT PADDLE COLLISION
        if right_paddle.x + PADDLE_WIDTH >= ball.x + ball.radius >= right_paddle.x and right_paddle.y - ball.radius < ball.y < right_paddle.y + right_paddle.height + ball.radius:

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
            LEFT_SCORE.inc(1 + left_score_increment)
            ball.reset()
            ball.moving = False
            ball.x_vel = ball_velocity_x
            ball.y_vel = ball_velocity_y
            sfx.play(assets.WIN_LOSE_ROUND_SOUND)

    def draw(self, screen):
        pygame.draw.circle(screen, Colors.BALL_COLOR, (self.x, self.y), self.radius, width = 0)

ball = Ball(W_WIDTH // 2, W_HEIGHT // 2, BALL_RADIUS)

#######################################################################################################################

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

#######################################################################################################################

# Variable initializing
midlines_draw = True
ball.moving = False
player_won = False
WAY_ARROW_SEM = 0

right_score_powerup_usage = 0
left_score_powerup_usage = 0
right_paddle_enlarge_usage = 0
left_paddle_enlarge_usage = 0
right_paddle_speed_boost_usage = 0
left_paddle_speed_boost_usage = 0

right_score_mult_interdicted = False
left_score_mult_interdicted = False
right_enlarge_paddle_interdicted = False
left_enlarge_paddle_interdicted = False
right_paddle_speed_boost_interdicted = False
left_paddle_speed_boost_interdicted = False

right_score_start_time = None
left_score_start_time = None
enlarge_paddle_left_start_time = None
enlarge_paddle_right_start_time = None
left_speed_boost_start_time = None
right_speed_boost_start_time = None

SCORE_MULT_LIFESPAN = 42 * TPS
ENLARGE_PADDLE_LIFESPAN = 40 * TPS
SPEED_BOOST_LIFESPAN = 40 * TPS

left_paddle_height_aux = left_paddle.height
right_paddle_height_aux = right_paddle.height
left_paddle_height_aux2 = left_paddle.height
right_paddle_height_aux2 = right_paddle.height
PADDLE_SPEED_AUX = PADDLE_SPEED


right_score_mult_active = False
left_score_mult_active = False
right_paddle_enlarge_active = False
left_paddle_enlarge_active = False
right_paddle_speed_boost_active = False
left_paddle_speed_boost_active = False

ball_velocity_x_aux = None
ball_velocity_y_aux = None
ball_freeze_sem = False
ball_freeze_usage = 0
ball_unfreeze_usage = 0

                                                    ##################################################################
while running:                                      #####################---- WHILE RUNNING ----######################
    screen.fill(Colors.SCREEN_FILL_COLOR)           ##################################################################
    current_frame = pygame.time.get_ticks()

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #POWERUP - SCORE MULTIPLIER EVENT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and right_score_powerup_usage == 0 and right_score_mult_interdicted is False:  #start_time =~ 640
                if ball.moving:
                    right_score_increment = 1
                    right_score_powerup_usage = 1
                right_score_start_time = pygame.time.get_ticks()
                sfx.play(assets.POWERUP_SOUND)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and left_score_powerup_usage == 0 and left_score_mult_interdicted is False:
                if ball.moving:
                    left_score_increment = 1
                    left_score_powerup_usage = 1
                left_score_start_time = pygame.time.get_ticks()
                sfx.play(assets.POWERUP_SOUND)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #POWERUP - PADDLE ENLARGE EVENT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and right_paddle_enlarge_usage == 0 and right_enlarge_paddle_interdicted is False:
                if ball.moving:
                    right_paddle.height += THE_PADDLE_HEIGHT_INCREASE
                    right_paddle.y -= (THE_PADDLE_HEIGHT_INCREASE / 2)
                    right_paddle_enlarge_usage = 1
                    enlarge_paddle_right_start_time = pygame.time.get_ticks()
                    right_paddle_enlarge_active = True
                    sfx.play(assets.POWERUP_SOUND2)
            paddle_height_increase = left_paddle.y


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and left_paddle_enlarge_usage == 0 and left_enlarge_paddle_interdicted is False:
                if ball.moving:
                    left_paddle.height += THE_PADDLE_HEIGHT_INCREASE
                    left_paddle.y -= (THE_PADDLE_HEIGHT_INCREASE / 2)
                    left_paddle_enlarge_usage = 1
                    enlarge_paddle_left_start_time = pygame.time.get_ticks()
                    left_paddle_enlarge_active = True
                    sfx.play(assets.POWERUP_SOUND2)
            paddle_height_increase = left_paddle.y

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # POWERUP - PADDLE SPEED BOOST EVENT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and right_paddle_speed_boost_usage == 0 and right_paddle_speed_boost_interdicted is False:
                if ball.moving:
                    right_paddle.speed += PADDLE_SPEED_INCREASE
                    right_paddle_speed_boost_usage = 1
                    right_paddle_speed_boost_active = True
                    right_speed_boost_start_time = pygame.time.get_ticks()
                    sfx.play(assets.POWERUP_SOUND3)


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and left_paddle_speed_boost_usage == 0 and left_paddle_speed_boost_interdicted is False:
                if ball.moving:
                    left_paddle.speed += PADDLE_SPEED_INCREASE
                    left_paddle_speed_boost_usage = 1
                    left_paddle_speed_boost_active = True
                    left_speed_boost_start_time = pygame.time.get_ticks()
                    sfx.play(assets.POWERUP_SOUND3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # POWERUP - FREEZE BALL EVENT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RSHIFT:
                if ball.moving and ball_freeze_usage == 0 and left_paddle.x + 2 * PADDLE_WIDTH <= ball.x:

                    ball_freeze_sem = True
                    ball_freeze_usage = 1

                    ball_velocity_x_aux = ball.x_vel
                    ball_velocity_y_aux = ball.y_vel
                    Colors.BALL_COLOR = Colors.DARKER_BLUE
                    sfx.play(assets.ICE_SOUND)

                    ball.x_vel = 0
                    ball.y_vel = 0



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                if ball.moving and ball_freeze_sem is True and ball_unfreeze_usage == 0:

                    ball_unfreeze_usage = 1

                    ball.x_vel = ball_velocity_x_aux
                    ball.y_vel = ball_velocity_y_aux
                    Colors.BALL_COLOR = Colors.BALL_COLOR_AUX
                    sfx.play(assets.UNFREEZE_SOUND)













#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #POWERUP - SCORE MULTIPLIER

    if right_score_start_time is not None and current_frame - right_score_start_time >= SCORE_MULT_LIFESPAN:
        right_score_increment = 0
        right_score_start_time = None

    if left_score_start_time is not None and current_frame - left_score_start_time >= SCORE_MULT_LIFESPAN:
        left_score_increment = 0
        left_score_start_time = None

    if right_score_increment == 1:
        right_enlarge_paddle_interdicted = True
        right_paddle_speed_boost_interdicted = True
        right_score_powerup_text = SuperDreamFont.render("SCORE MULTIPLIER ACTIVE", True, Colors.MEGA_LIGHT_BLUE_AUX)
        screen.blit(right_score_powerup_text, (W_WIDTH // 1.14 - right_score_powerup_text.get_width() // 2, W_HEIGHT - (W_HEIGHT - 12 * W_PERC)))
        Colors.SCREEN_FILL_COLOR = (0, 0, 9)

    elif right_score_increment == 0 and left_score_increment == 0:
        Colors.SCREEN_FILL_COLOR = Colors.SCREEN_FILL_COLOR_AUX
        right_enlarge_paddle_interdicted = False
        right_paddle_speed_boost_interdicted = False

    if left_score_increment == 1:
        left_enlarge_paddle_interdicted = True
        left_paddle_speed_boost_interdicted = True
        left_score_powerup_text = SuperDreamFont.render("SCORE MULTIPLIER ACTIVE", True, Colors.MEGA_LIGHT_RED_AUX)
        screen.blit(left_score_powerup_text, (W_WIDTH // 10 - left_score_powerup_text.get_width() // 2, W_HEIGHT - (W_HEIGHT - 12 * W_PERC)))
        Colors.SCREEN_FILL_COLOR = (9, 0, 0)

    elif left_score_increment == 0 and right_score_increment == 0:
        Colors.SCREEN_FILL_COLOR = Colors.SCREEN_FILL_COLOR_AUX
        left_enlarge_paddle_interdicted = False
        left_paddle_speed_boost_interdicted = False

    if left_score_increment == 1 and right_score_increment == 1:
        Colors.SCREEN_FILL_COLOR = (10, 0, 14)

    if right_score_increment == 1:
        Colors.MEGA_LIGHT_BLUE = (0, 50, 245)
    elif right_score_increment == 0:
        Colors.MEGA_LIGHT_BLUE = Colors.MEGA_LIGHT_BLUE_AUX

    if left_score_increment == 1:
        Colors.MEGA_LIGHT_RED = (240, 100, 0)
    elif left_score_increment == 0:
        Colors.MEGA_LIGHT_RED = Colors.MEGA_LIGHT_RED_AUX

 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # POWERUP - ENLARGE PADDLE

    if enlarge_paddle_right_start_time is not None and current_frame - enlarge_paddle_right_start_time >= (ENLARGE_PADDLE_LIFESPAN / 1.1) and right_paddle_enlarge_active is True:
        Colors.MEGA_LIGHT_BLUE = (0, 0, 120)
    elif right_paddle_enlarge_active is True:
        Colors.MEGA_LIGHT_BLUE = Colors.MEGA_LIGHT_BLUE_AUX

    if enlarge_paddle_left_start_time is not None and current_frame - enlarge_paddle_left_start_time >= (ENLARGE_PADDLE_LIFESPAN / 1.1) and left_paddle_enlarge_active is True:
        Colors.MEGA_LIGHT_RED = (120, 0, 0)
    elif left_paddle_enlarge_active is True:
        Colors.MEGA_LIGHT_RED = Colors.MEGA_LIGHT_RED_AUX

    if enlarge_paddle_right_start_time is not None and current_frame - enlarge_paddle_right_start_time >= ENLARGE_PADDLE_LIFESPAN and right_paddle_enlarge_active is True:
        enlarge_paddle_right_start_time = None
        right_paddle_enlarge_usage += 1
        right_paddle.height = left_paddle_height_aux
        right_paddle.y += (THE_PADDLE_HEIGHT_INCREASE // 2)
        right_paddle_enlarge_active = False
        right_score_mult_interdicted = False
        right_paddle_speed_boost_interdicted = False

    if enlarge_paddle_left_start_time is not None and current_frame - enlarge_paddle_left_start_time >= ENLARGE_PADDLE_LIFESPAN and left_paddle_enlarge_active is True:
        enlarge_paddle_left_start_time = None
        left_paddle_enlarge_usage += 1
        left_paddle.height = left_paddle_height_aux
        left_paddle.y += (THE_PADDLE_HEIGHT_INCREASE // 2)
        left_paddle_enlarge_active = False
        left_score_mult_interdicted = False
        left_paddle_speed_boost_interdicted = False

    if right_paddle_enlarge_active == 1:
        right_enlarge_paddle_text = SuperDreamFont.render("ENLARGE PADDLE ACTIVE", True, Colors.MEGA_LIGHT_BLUE_AUX)
        screen.blit(right_enlarge_paddle_text, (W_WIDTH // 1.14 - right_enlarge_paddle_text.get_width() // 2, W_HEIGHT - (W_HEIGHT - 12 * W_PERC)))

    if left_paddle_enlarge_active == 1:
        left_enlarge_paddle_text = SuperDreamFont.render("ENLARGE PADDLE ACTIVE", True, Colors.MEGA_LIGHT_RED_AUX)
        screen.blit(left_enlarge_paddle_text, (W_WIDTH // 10 - left_enlarge_paddle_text.get_width() // 2, W_HEIGHT - (W_HEIGHT - 12 * W_PERC)))

    if left_paddle_enlarge_active:
        left_score_mult_interdicted = True
        left_paddle_speed_boost_interdicted = True

    if right_paddle_enlarge_active:
        right_score_mult_interdicted = True
        right_paddle_speed_boost_interdicted = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # POWERUP - PADDLE SPEED BOOST

    if right_speed_boost_start_time is not None and current_frame - right_speed_boost_start_time >= (SPEED_BOOST_LIFESPAN / 1.1) and right_paddle_speed_boost_active is True:
        Colors.MEGA_LIGHT_BLUE = (0, 0, 120)
    elif right_paddle_speed_boost_active is True:
        Colors.MEGA_LIGHT_BLUE = Colors.MEGA_LIGHT_BLUE_AUX

    if left_speed_boost_start_time is not None and current_frame - left_speed_boost_start_time >= (SPEED_BOOST_LIFESPAN / 1.1) and left_paddle_speed_boost_active is True:
        Colors.MEGA_LIGHT_RED = (120, 0, 0)
    elif left_paddle_speed_boost_active is True:
        Colors.MEGA_LIGHT_RED = Colors.MEGA_LIGHT_RED_AUX


    if right_speed_boost_start_time is not None and current_frame - right_speed_boost_start_time >= SPEED_BOOST_LIFESPAN:
        right_speed_boost_start_time = None
        right_paddle_speed_boost_active = False
        right_paddle.speed = PADDLE_SPEED_AUX
        right_score_mult_interdicted = False
        right_enlarge_paddle_interdicted = False


    if left_speed_boost_start_time is not None and current_frame - left_speed_boost_start_time >= SPEED_BOOST_LIFESPAN:
        left_speed_boost_start_time = None
        left_paddle_speed_boost_active = False
        left_paddle.speed = PADDLE_SPEED_AUX
        left_score_mult_interdicted = False
        left_enlarge_paddle_interdicted = False


    if right_paddle_speed_boost_active == 1:
        right_speed_boost_text = SuperDreamFont.render("SPEED BOOST ACTIVE", True, Colors.MEGA_LIGHT_BLUE_AUX)
        screen.blit(right_speed_boost_text, (W_WIDTH // 1.14 - right_speed_boost_text.get_width() // 2, W_HEIGHT - (W_HEIGHT - 12 * W_PERC)))

    if left_paddle_speed_boost_active == 1:
        left_speed_boost_text = SuperDreamFont.render("SPEED BOOST ACTIVE", True, Colors.MEGA_LIGHT_RED_AUX)
        screen.blit(left_speed_boost_text, (W_WIDTH // 10 - left_speed_boost_text.get_width() // 2, W_HEIGHT - (W_HEIGHT - 12 * W_PERC)))


    if left_paddle_speed_boost_active:
        left_score_mult_interdicted = True
        left_enlarge_paddle_interdicted = True

    if right_paddle_speed_boost_active:
        right_score_mult_interdicted = True
        right_enlarge_paddle_interdicted = True


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       ###### DRAWS #######

    if midlines_draw:
        for i in range(0, MID_LINES_COUNT):
            LINE_START = i * 2 * W_HEIGHT / (MID_LINES_COUNT * 2)
            LINE_END = (i * 2 + 1) * W_HEIGHT / (MID_LINES_COUNT * 2)
            pygame.draw.line(screen, Colors.WAY_TOO_DARK_GRAY, (W_WIDTH / 2, LINE_START), (W_WIDTH / 2, LINE_END),2)

    left_paddle.draw_left(screen)
    right_paddle.draw_right(screen)
    ball.draw(screen)
    LEFT_SCORE.draw()
    RIGHT_SCORE.draw()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Press_space_sem = True
    print_arrows = True

    #########   WINNING SITUATION   #########

    if LEFT_SCORE.get() >= WINNING_SCORE or RIGHT_SCORE.get() >= WINNING_SCORE:
        right_score_increment = 0
        left_score_increment = 0
        left_score_powerup_usage = 0
        right_score_powerup_usage = 0
        right_paddle_enlarge_usage = 0
        left_paddle_enlarge_usage = 0
        right_paddle_speed_boost_usage = 0
        left_paddle_speed_boost_usage = 0

        right_paddle.height = left_paddle_height_aux2
        right_paddle_enlarge_active = False

        left_paddle.height = left_paddle_height_aux2
        left_paddle_enlarge_active = False

        if right_paddle_speed_boost_active:
            right_paddle.speed = PADDLE_SPEED_AUX
            right_paddle_speed_boost_active = False

        if left_paddle_speed_boost_active:
            left_paddle.speed = PADDLE_SPEED_AUX
            left_paddle_speed_boost_active = False


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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #######  PRESS SPACE TO START SITUATION  #######

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
            right_score_increment = 0
            left_score_increment = 0
            right_score_mult_interdicted = False
            left_score_mult_interdicted = False
            right_paddle_speed_boost_interdicted = False
            left_paddle_speed_boost_interdicted = False

            left_paddle.height = left_paddle_height_aux2
            left_paddle_enlarge_active = False
            right_paddle.height = left_paddle_height_aux2
            right_paddle_enlarge_active = False


            if right_paddle_speed_boost_active:
                right_paddle.speed = PADDLE_SPEED_AUX
                right_paddle_speed_boost_active = False


            if left_paddle_speed_boost_active:
                left_paddle.speed = PADDLE_SPEED_AUX
                left_paddle_speed_boost_active = False


        if ball.x_vel < 0:
            WAY_ARROW_SEM = False  # Ball is moving left
        else:
            WAY_ARROW_SEM = True

        if print_arrows:
            if WAY_ARROW_SEM:
                screen.blit(Way_line_right_text, (W_WIDTH // 2 + 40 * W_PERC, W_HEIGHT // 2 - 30 * W_PERC))
            elif not WAY_ARROW_SEM:
                screen.blit(Way_line_left_text, (W_WIDTH // 2 - 115 * W_PERC, W_HEIGHT // 2 - 30 * W_PERC))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #########  Controls  #########

    KEYS_PRESSED = pygame.key.get_pressed()
    if KEYS_PRESSED[pygame.K_UP]:
        if DEBUG_MODE: print_debug("Keydown: UP")
        if right_paddle.y > 0:
            right_paddle.y -= right_paddle.speed * RIGHT_PADDLE_SPEED_MULT / TPS

    if KEYS_PRESSED[pygame.K_DOWN]:
        if DEBUG_MODE: print_debug("Keydown: DOWN")
        if right_paddle.y < W_HEIGHT - right_paddle.height:
            right_paddle.y += right_paddle.speed * RIGHT_PADDLE_SPEED_MULT / TPS

    if KEYS_PRESSED[pygame.K_w]:
        if DEBUG_MODE: print_debug("Keydown: W")
        if left_paddle.y > 0:
            left_paddle.y -= left_paddle.speed * LEFT_PADDLE_SPEED_MULT / TPS

    if KEYS_PRESSED[pygame.K_s]:
        if DEBUG_MODE: print_debug("Keydown: S")
        if left_paddle.y < W_HEIGHT - left_paddle.height:
            left_paddle.y += left_paddle.speed * LEFT_PADDLE_SPEED_MULT / TPS

    ################################
    ######### Clip Bug Fix #########
    ################################

    if left_paddle.y > W_HEIGHT - left_paddle.height:
        left_paddle.y = W_HEIGHT - left_paddle.height
    if left_paddle.y < 0:
        left_paddle.y = 0
    if right_paddle.y > W_HEIGHT - right_paddle.height:
        right_paddle.y = W_HEIGHT - right_paddle.height
    if right_paddle.y < 0:
        right_paddle.y = 0

    if DEBUG_MODE:
        fps = clock.get_fps()
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {fps:.2f}", True, (170, 170, 170))
        screen.blit(fps_text, (10, 10))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    pygame.display.update()
    clock.tick(TPS)