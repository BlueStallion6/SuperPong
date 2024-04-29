import pygame

pygame.mixer.init()
sfx = pygame.mixer.Sound

HIGHPITCHED_HIT = sfx(".\\resources\\sounds\\Impact sound high pitch.wav")
MIDPITCHED_HIT = sfx(".\\resources\\sounds\\Impact sound mid pitch.wav")
LOWPITCHED_HIT = sfx(".\\resources\\sounds\\Impact sound low pitch.wav")