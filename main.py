#Dupa ce instalezi importurile baga in consola "pip freeze > requirements.txt"
try:
    import os
    import pygame
    import colored
    from keywords import *
    import sys
    #import resources.pygameResources as assets
    import screeninfo
    from screeninfo import get_monitors
except ImportError:
    print("ImportError >> Please run 'pip install -r requirements.txt' in this folder's directory.")
    exit()

pygame.init()

monitors = get_monitors()
primary_monitor = monitors[0]

flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

if primary_monitor.width >= 2560 and primary_monitor.height >= 1440:
    # If monitor resolution is at least 2560x1440, use 2K
    width, height = 2560, 1440
    background_image_path = "pxfuel_2k.jpg"
elif primary_monitor.width >= 3840 and primary_monitor.height >= 2160:
    width, height = 3840, 2160
    background_image_path = "pxfuel_4k.jpg"
else:
    # Otherwise, default to 1080p
    width, height = 1920, 1080
    background_image_path = "pxfuel_fhd.jpg.jpg"

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height), flags)

background_image = pygame.image.load(background_image_path)

pygame.display.set_caption('SuperPong')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print_success("Closing the game...")
            exit()
    pygame.display.flip()
    screen.blit(background_image, (-240, 0))
    pygame.display.update()

    clock.tick(100)






