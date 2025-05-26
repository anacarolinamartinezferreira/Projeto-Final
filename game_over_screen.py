import pygame
pygame.display.init()
import random 
import os
from os import path
from assets import load_assets, GAME_OVER_SOUND, SCORE_FONT
from config import IMG_DIR, BLACK, FPS, INIT, QUIT, INFO, SND_DIR, WIDTH, HEIGHT, RED

def game_over_screen(screen, score, high_score): 
    # Variável para ajuste de velocidade 
    clock = pygame.time.Clock()
    assets = load_assets()

    # Carrega o fundo da tela inicial 
    background = pygame.image.load(path.join(IMG_DIR, 'game_over_screen.png')).convert()
    background = pygame.transform.scale(background,(WIDTH, HEIGHT))
    background_rect = background.get_rect()

    running = True 
    while running: 
        assets[GAME_OVER_SOUND].play()
        # Ajusta a velocidade do jogo. 
        clock.tick(FPS)

        # Processa os eventos
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

        # Desenha a pontuação atual
        score_text = assets[SCORE_FONT].render(f"Score: {score}", True, BLACK)
        score_rect = score_text.get_rect()
        score_rect.centerx = WIDTH / 2
        score_rect.centery = HEIGHT - 20
        screen.blit(score_text, score_rect)

        # Desenha o recorde
        high_score_text = assets[SCORE_FONT].render(f"High Score: {high_score}", True, BLACK)
        high_score_rect = high_score_text.get_rect()
        high_score_rect.centerx = WIDTH / 2
        high_score_rect.centery = HEIGHT - 80
        screen.blit(high_score_text, high_score_rect)

        # Depois de desenhar tudo, inverte o display
        pygame.display.flip()

    return state