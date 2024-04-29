import json
import pygame
from keywords import *
from screeninfo import get_monitors


try:
    open("config.json")
except FileNotFoundError:
    print_error("Config file not found.")

with open("config.json", "r") as file:
    CONFIG = json.load(file)
    # print_debug(str(config["settings"]))
    file.close()

if CONFIG["settings"]["window_perc"] is None:
    #FALLBACK VALUE
    W_PERC = 0.5  
else:
    W_PERC = CONFIG["settings"]["window_perc"] / 100

MONITORS = get_monitors()
primary_monitor = MONITORS[0]

DEBUG_MODE = CONFIG["settings"]["debug_mode"]
W_WIDTH = primary_monitor.width * W_PERC
W_HEIGHT = primary_monitor.height * W_PERC
PADDLE_WIDTH, PADDLE_HEIGHT = CONFIG["play_configs"]["paddle_width"] * W_PERC, CONFIG["play_configs"]["paddle_height"] * W_PERC
TPS = CONFIG["settings"]["tps"]
PADDLE_SPEED = CONFIG["play_configs"]["paddle_speed"] * W_PERC

TEXT_UP = CONFIG["play_configs"]["text_up"] * W_PERC
TEXT_SPACING = CONFIG["play_configs"]["text_spacing"] * W_PERC

RP_HEIGHT_MULT = 1
RP_SPEED_MULT = 1

LP_HEIGHT_MULT = 1
LP_SPEED_MULT = 1


MID_LINES_COUNT = CONFIG["play_configs"]["mid_lines_count"]
PADDLE_SPACING = CONFIG["play_configs"]["paddle_spacing"] * W_PERC
BALL_RADIUS = CONFIG["play_configs"]["ball_radius"] * W_PERC

SFX_VOLUME = CONFIG["settings"]["sfx_volume"]

FLAGS = pygame.HWSURFACE | pygame.DOUBLEBUF