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
        self.rect.centerx = -WIDTH
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.speedy = 0 
        self.groups = groups
        self.assets = assets

    def update(self):
        # Atualização da posição da nave
        if self.speedx > 0:
            self.image = self.assets[MINION_RUN_IMG]
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def banana(self):
        # A nova bala vai ser criada logo acima e no centro horizontal da nave
        new_banana = Banana(self.assets, self.rect.top, self.rect.centerx)
        self.groups['all_sprites'].add(new_banana)
        self.groups['all_bullets'].add(new_banana)
    
    def purple(self):
        self.image = self.assets[PURPLE_MINION_IMG]

class Robot(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets[ROBOT_IMG]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = 0
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = random.randint(0, 10)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

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

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

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
        self.speedx = 0 # Velocidade fixa para cima

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()