from os import path

# Estabelece a pasta que contem as figuras e sons.
IMG_DIR = path.join(path.dirname(__file__), 'assets', 'img')
SND_DIR = path.join(path.dirname(__file__), 'assets', 'snd')
FNT_DIR = path.join(path.dirname(__file__), 'assets', 'font')

# Dados gerais do jogo.
WIDTH = 1500 # Largura da tela
HEIGHT = 750 # Altura da tela
MINION_WIDTH = 210
MINION_HEIGHT = 120
FPS = 60 # Frames por segundo]
BANANA_WIDTH = 110
BANANA_HEIGHT = 60
ROBOT_WIDTH = 210
ROBOT_HEIGHT = 120
SORO_WIDTH = 130
SORO_HEIGHT = 130

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