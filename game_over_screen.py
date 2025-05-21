import pygame
pygame.display.init()
import random 
import os
from os import path
from assets import load_assets,GAME_OVER_SOUND
from config import IMG_DIR, BLACK, FPS, INIT , QUIT, INFO, SND_DIR

def game_over_screen(screen): 
    # Variável para ajuste de velocidade 
    clock = pygame.time.Clock()
    assets = load_assets()

    # Carrega o fundo da tela inicial 
    background = pygame.image.load(path.join(IMG_DIR, 'game_over_screen.png')).convert()
    background = pygame.transform.scale(background,(600, 300))
    background_rect = background.get_rect()

    running = True 
    while running: 
        assets[GAME_OVER_SOUND].play()
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