import pygame

pygame.mixer.init()
sfx = pygame.mixer.Sound

HIGHPITCHED_HIT = sfx(".\\resources\\sounds\\pong_sound2.wav")
MIDPITCHED_HIT = sfx(".\\resources\\sounds\\pong_sound1.wav")
LOWPITCHED_HIT = sfx(".\\resources\\sounds\\pickupCoin2.wav")