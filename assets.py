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
    
    # Load death animation with transparency and scale it down
    assets[DYING_ANIMATION] = pygame.image.load(os.path.join(IMG_DIR,'perde_vida.anim.png')).convert_alpha()
    assets[DYING_ANIMATION] = pygame.transform.scale(assets[DYING_ANIMATION], (100, 100))  # Make it smaller, adjust size as needed

    # Load score animation with transparency
    score_img = pygame.image.load(os.path.join(IMG_DIR,'ganha_ponto.png')).convert_alpha()
    # Create a copy with per-pixel alpha
    alpha_img = pygame.Surface(score_img.get_size(), pygame.SRCALPHA)
    # For each pixel, if it's light colored (close to white), make it transparent
    for x in range(score_img.get_width()):
        for y in range(score_img.get_height()):
            color = score_img.get_at((x, y))
            if color[0] > 200 and color[1] > 200 and color[2] > 200:  # If it's close to white
                alpha_img.set_at((x, y), (0, 0, 0, 0))  # Fully transparent
            else:
                alpha_img.set_at((x, y), color)  # Keep original color
    assets[SCORE_ANIMATION] = pygame.transform.scale(alpha_img, (100, 100))  # Scale after processing

    # Load score 2 animation with transparency
    score_2_img = pygame.image.load(os.path.join(IMG_DIR,'ganha_2pontos.png')).convert_alpha()
    # Create a copy with per-pixel alpha
    alpha_img_2 = pygame.Surface(score_2_img.get_size(), pygame.SRCALPHA)
    # For each pixel, if it's light colored (close to white) or black, make it transparent
    for x in range(score_2_img.get_width()):
        for y in range(score_2_img.get_height()):
            color = score_2_img.get_at((x, y))
            # Se for próximo do branco ou preto, torna transparente
            if (color[0] > 200 and color[1] > 200 and color[2] > 200) or (color[0] < 30 and color[1] < 30 and color[2] < 30):
                alpha_img_2.set_at((x, y), (0, 0, 0, 0))  # Fully transparent
            else:
                alpha_img_2.set_at((x, y), color)  # Keep original color
    assets[SCORE_2_ANIMATION] = pygame.transform.scale(alpha_img_2, (100, 100))  # Mesmo tamanho da animação +1

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(SND_DIR,'relaxing-guitar-loop-v5-245859.mp3'))
    assets[GAME_OVER_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'gameover_snd.mp3'))
    assets[BANANA_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'bana_snd.mp3'))
    assets[PURPLE_TRANSFORM_SOUND] = pygame.mixer.Sound(os.path.join(SND_DIR, 'purple_minion.mp3'))
    pygame.mixer.music.set_volume(0.4)
    return assets