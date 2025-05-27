import pygame
pygame.display.init()
import os 
from config import IMG_DIR, SND_DIR,FNT_DIR, WIDTH, HEIGHT, MINION_WIDTH, MINION_HEIGHT, BANANA_WIDTH, BANANA_HEIGHT, ROBOT_WIDTH, ROBOT_HEIGHT, SORO_WIDTH, SORO_HEIGHT

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
DYING_ANIMATION = 'perde_vida.anim'
SCORE_ANIMATION = 'score_anim'
SCORE_2_ANIMATION = 'score_2_anim'
BANANA_SOUND = 'banana_sound'
PURPLE_TRANSFORM_SOUND = 'purple_transform_sound'
PURPLE_EXPLOSION = 'purple_explosion'
FAIL_SOUND = 'fail_sound'


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
    assets['soro_img'] = pygame.image.load(os.path.join(IMG_DIR,'soro.png')).convert_alpha()
    assets['soro_img'] = pygame.transform.scale(assets['soro_img'],(SORO_WIDTH, SORO_HEIGHT))
    assets['banana_img'] = pygame.image.load(os.path.join(IMG_DIR,'banana.png')).convert_alpha()
    assets['banana_img'] = pygame.transform.scale(assets['banana_img'],(BANANA_WIDTH, BANANA_HEIGHT))
    assets[SCORE_FONT] = pygame.font.Font(os.path.join(FNT_DIR, 'PressStart2P-Regular.ttf'), 28)
    
    # Animação de perda de vida com transparência
    assets[DYING_ANIMATION] = pygame.image.load(os.path.join(IMG_DIR,'perde_vida.anim.png')).convert_alpha()
    assets[DYING_ANIMATION] = pygame.transform.scale(assets[DYING_ANIMATION], (100, 100))  # Diminue

    # Animação de mais um ponto com transparência
    score_img = pygame.image.load(os.path.join(IMG_DIR,'ganha_ponto.png')).convert_alpha()
    alpha_img = pygame.Surface(score_img.get_size(), pygame.SRCALPHA)
    # Se o pixel for perto de branco, vira transparente
    for x in range(score_img.get_width()):
        for y in range(score_img.get_height()):
            color = score_img.get_at((x, y))
            if color[0] > 200 and color[1] > 200 and color[2] > 200:  # Se for perto de branco
                alpha_img.set_at((x, y), (0, 0, 0, 0))  # Deixar transparente
            else:
                alpha_img.set_at((x, y), color)  # Manter a cor 
    assets[SCORE_ANIMATION] = pygame.transform.scale(alpha_img, (100, 100))  # Escala depois de processar

    # Animação de mais dois pontos com transparência
    score_2_img = pygame.image.load(os.path.join(IMG_DIR,'ganha_2pontos.png')).convert_alpha()
    alpha_img_2 = pygame.Surface(score_2_img.get_size(), pygame.SRCALPHA)
    # Se o pixel for branco, claro ou preto, deixe transparente
    for x in range(score_2_img.get_width()):
        for y in range(score_2_img.get_height()):
            color = score_2_img.get_at((x, y))
            # Se for próximo do branco ou preto, torna transparente
            if (color[0] > 200 and color[1] > 200 and color[2] > 200) or (color[0] < 30 and color[1] < 30 and color[2] < 30):
                alpha_img_2.set_at((x, y), (0, 0, 0, 0))  # Fully transparent
            else:
                alpha_img_2.set_at((x, y), color)  # Manter cor original
    assets[SCORE_2_ANIMATION] = pygame.transform.scale(alpha_img_2, (100, 100))  # Mesmo tamanho da animação +1

    # Explosão roxa com transparência
    explosion_img = pygame.image.load(os.path.join(IMG_DIR,'explosão_roxa.png')).convert_alpha()
    alpha_explosion = pygame.Surface(explosion_img.get_size(), pygame.SRCALPHA)
    # Se o pixel for branco, claro ou preto, deixe transparente
    for x in range(explosion_img.get_width()):
        for y in range(explosion_img.get_height()):
            color = explosion_img.get_at((x, y))
            if (color[0] > 200 and color[1] > 200 and color[2] > 200) or (color[0] < 30 and color[1] < 30 and color[2] < 30):
                alpha_explosion.set_at((x, y), (0, 0, 0, 0))  # Deixar transparente
            else:
                alpha_explosion.set_at((x, y), color)  # Manter cor original
    assets[PURPLE_EXPLOSION] = pygame.transform.scale(alpha_explosion, (200, 200))  # Tamanho maior para a explosão

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR,'relaxing-guitar-loop-v5-245859.mp3'))
    assets[GAME_OVER_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'gameover_snd.mp3'))
    assets[BANANA_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'bana_snd.mp3'))
    assets[PURPLE_TRANSFORM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'purple_minion.mp3'))
    assets[FAIL_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'fail-144746.mp3'))
    pygame.mixer.music.set_volume(0.4)
    return assets