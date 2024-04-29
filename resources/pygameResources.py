import pygame

pygame.mixer.init()
sfx = pygame.mixer.Sound

MARGIN_HIT_SOUND = sfx(".\\resources\\sounds\\pong_sound2.wav")
PADDLE_HIT_SOUND = sfx(".\\resources\\sounds\\pong_sound1.wav")
WIN_LOSE_SOUND = sfx(".\\resources\\sounds\\pickupCoin2.wav")