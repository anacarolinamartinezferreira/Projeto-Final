import random
import pygame
from config import WIDTH, HEIGHT
from assets import MINION_STILL_IMG, MINION_RUN_IMG, ROBOT_IMG, BANANA_IMG, PURPLE_MINION_IMG, SORO_IMG


class Minion(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[MINION_STILL_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100  
        self.rect.bottom = HEIGHT
        self.speedy = 0 
        self.groups = groups
        self.assets = assets
        
        # Atributos para controle de invencibilidade
        self.invencivel = False
        self.ultimo_dano = 0
        self.tempo_invencivel = 2000  # 2 segundos de invencibilidade
        self.alpha = 255  # Controle de transparência

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def update(self):
        self.rect.y += self.speedy
        
        # Atualiza invencibilidade
        if self.invencivel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.ultimo_dano > self.tempo_invencivel:
                self.invencivel = False
                self.alpha = 255
                self.image.set_alpha(self.alpha)
            else:
                # Faz o Minion piscar
                self.alpha = 255 if (tempo_atual // 100) % 2 == 0 else 128
                self.image.set_alpha(self.alpha)
        else:
            # Garante que a opacidade seja 255 quando não estiver invencível
            self.alpha = 255
            self.image.set_alpha(self.alpha)

    def tomar_dano(self):
        if not self.invencivel:
            self.invencivel = True
            self.ultimo_dano = pygame.time.get_ticks()
            return True
        return False
    
    def purple(self):
        self.image = self.assets[PURPLE_MINION_IMG]
        # Mantém a opacidade atual ao trocar de imagem
        self.image.set_alpha(self.alpha)

class Robot(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[ROBOT_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 0  
        self.speedy = 0  

        # Se o robô passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()
            
    def update(self):
        # Atualiza a posição do robô
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Banana(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[BANANA_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 0
        self.speedy = 0

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Soro(pygame.sprite.Sprite):
    def __init__(self, assets, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[SORO_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 0 

        # Se o soro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()