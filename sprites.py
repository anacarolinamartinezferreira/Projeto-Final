import random
import pygame
from config import WIDTH, HEIGHT
from assets import MINION_STILL_IMG, MINION_RUN_IMG, ROBOT_IMG, BANANA_IMG, PURPLE_MINION_IMG, SORO_IMG, DYING_ANIMATION


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

        # Atributos para controle do poder do minion roxo
        self.is_purple = False
        self.purple_start_time = 0
        self.purple_duration = 7000  # 7 segundos de duração
        
        # Controle de movimento
        self.moving = False

        # Controle da animação de morte
        self.dying = False
        self.dying_start = 0
        self.dying_duration = 700  # 0.7 segundos de animação

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def update(self):
        self.rect.y += self.speedy
        
        tempo_atual = pygame.time.get_ticks()

        # Atualiza animação de morte
        if self.dying:
            if tempo_atual - self.dying_start > self.dying_duration:
                self.dying = False
            return  # Não atualiza outros estados durante a animação de morte
        
        # Atualiza invencibilidade
        if self.invencivel:
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

        # Atualiza estado do minion roxo
        if self.is_purple:
            if tempo_atual - self.purple_start_time > self.purple_duration:
                self.is_purple = False
                if not self.moving:  # Se não estiver se movendo
                    self.image = self.assets[MINION_STILL_IMG]
                else:  # Se estiver se movendo
                    self.image = self.assets[MINION_RUN_IMG]
                self.image.set_alpha(self.alpha)

    def tomar_dano(self):
        if not self.invencivel:
            self.invencivel = True
            self.ultimo_dano = pygame.time.get_ticks()
            self.dying = True
            self.dying_start = pygame.time.get_ticks()
            return True
        return False
    
    def turn_purple(self):
        self.is_purple = True
        self.purple_start_time = pygame.time.get_ticks()
        self.image = self.assets[PURPLE_MINION_IMG]
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
    # Construtor da classe.
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
        self.speedy = 0

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

