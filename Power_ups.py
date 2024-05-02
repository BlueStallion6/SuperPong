import pygame
import json
import time
from keywords import *

try:
    open("config.json")
except FileNotFoundError:
    print_error("Config file not found.")

with open("config.json", "r") as file:
    CONFIG = json.load(file)
    # print_debug(str(config["settings"]))
    file.close()

RIGHT_SCORE_INCREASE_MULT = CONFIG["powerups"]["score_mult"]


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