import pygame

pygame.init()

window = pygame.display.set_mode((600, 300))
pygame.display.set_caption('Escape from Vector!')
pygame.mixer.music.load('relaxing-guitar-loop-v5-245859.mp3')
pygame.mixer.music.set_volume(0.4)



assets = {}
assets['background'] = pygame.image.load('background.png').convert()
assets['robot_img'] = pygame.image.load('robo.png').convert_alpha()
assets['minion_still_img'] = pygame.image.load('minion_still.png').convert_alpha()
assets['minion_run_img'] = pygame.image.load('minion_running.png').convert_alpha()
assets['purple_minion_img'] = pygame.image.load('purple_minion.png').convert_alpha()
assets['down_img'] = pygame.image.load('embaixo.png').convert_alpha()
assets['up_img'] = pygame.image.load('cima.png').convert_alpha()
assets['unicorn_img'] = pygame.image.load('unicorn.png').convert_alpha()
assets['soro_img'] = pygame.image.load('soro.png').convert_alpha()
assets['raio_img'] = pygame.image.load('raio.png').convert_alpha()
assets['banana_img'] = pygame.image.load('banana.png').convert_alpha()
assets['floor_img'] = pygame.image.load('floor.png').convert_alpha()

assets['score_font'] = pygame.font.Font('PressStart2P-Regular.ttf',28)



