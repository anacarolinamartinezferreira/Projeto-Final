import pygame
import random 
from os import path

from config import IMG_DIR, BLACK, FPS, INIT , QUIT, INFO

def game_over_screen(screen): 
    # Variável para ajuste de velocidade 
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial 
    background = pygame.image.load(path.join(IMG_DIR, 'game_over_screen')).convert()
    background = pygame.transform.scale(background,(600, 300))
    background_rect = background.get_rect()

    running = True 
    while running: 

        # Ajusta a velocidade do jogo. 
        clock.tick(FPS)

        # Processa os enventos
        for event in pygame.event.get():
            # Verifica se foi fechado 
            if event.type == pygame.QUIT:
                state = QUIT
                running = False 
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    state = INIT
                    running = False
        
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()

    return state