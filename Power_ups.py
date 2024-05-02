import pygame
import time
from keywords import *
from Constants import CONFIG

RIGHT_SCORE_INCREASE_MULT = CONFIG["powerups"]["score_mult"]
LEFT_SCORE_INCREASE_MULT = CONFIG["powerups"]["score_mult"]

LEFT_PADDLE_SPEED_MULT = 1
RIGHT_PADDLE_SPEED_MULT = 1

LEFT_PADDLE_HEIGHT_MULT = 2
RIGHT_PADDLE_HEIGHT_MULT = 2



POWER_UP_DURATION = 5
class PowerUp_Enlarge:
    def __init__(self, paddle):
        self.paddle = paddle
        self.active = False
        self.duration = POWER_UP_DURATION
        self.activation_time = 0

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self):
        if self.active:
            # Check if power-up duration has elapsed
            current_time = pygame.time.get_ticks()
            if current_time - self.activation_time >= self.duration:
                self.deactivate()