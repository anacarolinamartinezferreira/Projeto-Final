from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
WIDTH = 600 # Largura da tela
HEIGHT = 300 # Altura da tela
MINION_WIDTH = 100
MINION_HEIGHT = 50
FPS = 60 # Frames por segundo]
BANANA_WIDTH = 50
BANANA_HEIGHT = 25
ROBOT_WIDTH = 90
ROBOT_HEIGHT = 45

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
EXPLODING = 2
QUIT = 3
INFO = 4
GAME_OVER = 5