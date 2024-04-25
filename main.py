#Dupa ce instalezi importurile baga in consola "pip freeze > requirements.txt"

try:
    import pygame
    import colored
    from keywords import *
    from sys import exit
    import resources.pygameResources as assets
except ImportError:
    print("Error >> Please run 'pip install -r requirements.txt' in this folder's directory.")


pygame.init()
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('SuperPong')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print_success("Closing the game...")
            exit()
    screen.blit(assets.bg,(-240,0))
    pygame.display.update()
    clock.tick(75)






