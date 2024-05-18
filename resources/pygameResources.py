import pygame

pygame.mixer.init()
sfx = pygame.mixer.Sound

MARGIN_HIT_SOUND = sfx(".\\resources\\sounds\\pong_sound2.wav")
MARGIN_HIT_SOUND_2 = sfx(".\\resources\\sounds\\pong_sound2.wav")
PADDLE_HIT_SOUND = sfx(".\\resources\\sounds\\pong_sound1.wav")
WIN_LOSE_ROUND_SOUND = sfx(".\\resources\\sounds\\pickupCoin2.wav")
WIN_SOUND = sfx(".\\resources\\sounds\\Win_sound.wav")
POWERUP_SOUND = sfx(".\\resources\\sounds\\powerUp4.wav")
POWERUP_SOUND2 = sfx(".\\resources\\sounds\\powerUp2.wav")
POWERUP_SOUND3 = sfx(".\\resources\\sounds\\powerUp5.wav")
ICE_SOUND = sfx(".\\resources\\sounds\\ice_sfx.wav")
UNFREEZE_SOUND = sfx(".\\resources\\sounds\\unfreeze1.wav")
SABOTAGE_SOUND = sfx(".\\resources\\sounds\\powerUp_sabotage.wav")

MARGIN_HIT_SOUND.set_volume(0.3)
PADDLE_HIT_SOUND.set_volume(0.35)
WIN_LOSE_ROUND_SOUND.set_volume(0.35)
WIN_SOUND.set_volume(0.35)
POWERUP_SOUND.set_volume(0.20)
POWERUP_SOUND2.set_volume(0.20)
POWERUP_SOUND3.set_volume(0.18)
ICE_SOUND.set_volume(0.26)
UNFREEZE_SOUND.set_volume(0.20)
SABOTAGE_SOUND.set_volume(0.20)
MARGIN_HIT_SOUND_2.set_volume(0.10)