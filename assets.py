import pygame
pygame.display.init()
import os 
from config import IMG_DIR, SND_DIR,FNT_DIR, WIDTH, HEIGHT, MINION_WIDTH, MINION_HEIGHT, BANANA_WIDTH, BANANA_HEIGHT, ROBOT_WIDTH, ROBOT_HEIGHT

BACKGROUND = 'background'
ROBOT_IMG = 'robot_img'
MINION_STILL_IMG = 'minion_still_img'
MINION_RUN_IMG = 'minion_run_img'
PURPLE_MINION_IMG = 'purple_minion_img'
DOWN_IMG = 'down_img'
UP_IMG = 'up_img'
UNICORN_IMG = 'unicorn_img'
SORO_IMG = 'soro_img'
RAIO_IMG = 'raio_img'
BANANA_IMG = 'banana_img'
FLOOR_IMG = 'floor_img'
SCORE_FONT = 'score_font'
GAME_OVER_SOUND = 'game_over_sound'

def load_assets():
    assets = {}
    assets['background'] = pygame.image.load(os.path.join(IMG_DIR,'background.png')).convert()
    assets['background'] = pygame.transform.scale(assets['background'],(WIDTH, HEIGHT))
    assets['robot_img'] = pygame.image.load(os.path.join(IMG_DIR,'robo.png')).convert_alpha()
    assets['robot_img'] = pygame.transform.scale(assets['robot_img'],(ROBOT_WIDTH, ROBOT_HEIGHT))
    assets['minion_still_img'] = pygame.image.load(os.path.join(IMG_DIR,'minion_still.png')).convert_alpha()
    assets['minion_still_img'] = pygame.transform.scale(assets['minion_still_img'],(MINION_WIDTH, MINION_HEIGHT))
    assets['minion_run_img'] = pygame.image.load(os.path.join(IMG_DIR,'minion_run.png')).convert_alpha()
    assets['minion_run_img'] = pygame.transform.scale(assets['minion_run_img'],(MINION_WIDTH, MINION_HEIGHT))
    assets['purple_minion_img'] = pygame.image.load(os.path.join(IMG_DIR,'purple_minion.png')).convert_alpha()
    assets['purple_minion_img'] = pygame.transform.scale(assets['purple_minion_img'],(MINION_WIDTH, MINION_HEIGHT))
    assets['down_img'] = pygame.image.load(os.path.join(IMG_DIR,'embaixo.png')).convert_alpha()
    assets['up_img'] = pygame.image.load(os.path.join(IMG_DIR,'cima.png')).convert_alpha()
    assets['unicorn_img'] = pygame.image.load(os.path.join(IMG_DIR,'unicorn.png')).convert_alpha()
    assets['soro_img'] = pygame.image.load(os.path.join(IMG_DIR,'soro.png')).convert_alpha()
    assets['raio_img'] = pygame.image.load(os.path.join(IMG_DIR,'raio.png')).convert_alpha()
    assets['banana_img'] = pygame.image.load(os.path.join(IMG_DIR,'banana.png')).convert_alpha()
    assets['banana_img'] = pygame.transform.scale(assets['banana_img'],(BANANA_WIDTH, BANANA_HEIGHT))
    assets['floor_img'] = pygame.image.load(os.path.join(IMG_DIR,'floor.png')).convert_alpha()
    assets[SCORE_FONT] = pygame.font.Font(os.path.join(FNT_DIR, 'PressStart2P-Regular.ttf'), 28)

    pygame.mixer.music.load(os.path.join(SND_DIR,'relaxing-guitar-loop-v5-245859.mp3'))
    assets[GAME_OVER_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'gameover_snd.mp3'))
    pygame.mixer.music.set_volume(0.4)
    return assets