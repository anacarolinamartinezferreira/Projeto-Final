# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from config import WIDTH, HEIGHT, INIT, GAME, QUIT, INFO, GAME_OVER
from init_screen import init_screen
from game_screen import game_screen
from info_screen import info_screen
from game_over_screen import game_over_screen


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Escape from Vector!')

state = INIT
current_score = 0
high_score = 0

while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state, current_score, high_score = game_screen(window)
    elif state == INFO:
        state = info_screen(window)
    elif state == GAME_OVER:
        state = game_over_screen(window, current_score, high_score)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados