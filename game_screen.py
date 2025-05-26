import pygame
import random
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, QUIT, GAME_OVER
from assets import load_assets, BACKGROUND, SCORE_FONT,MINION_STILL_IMG,MINION_RUN_IMG,PURPLE_MINION_IMG
from sprites import Minion,Robot,Banana,Soro

world_speed=-10

def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando um grupo de meteoros
    all_sprites = pygame.sprite.Group()
    all_bananas = pygame.sprite.Group()
    all_robots = pygame.sprite.Group()
    all_soros = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_bananas'] = all_bananas
    groups['all_soros'] = all_soros

    # Criando o jogador
    player = Minion(groups, assets)
    all_sprites.add(player)
    
    # Posição inicial para a primeira banana
    current_x = 200

    for i in range(10):
        # Criando as bananas com espaçamento aleatório
        b = Banana(assets, HEIGHT-25, current_x)
        all_sprites.add(b)
        all_bananas.add(b)
        # Adiciona um espaçamento aleatório entre 50 e 150 pixels para a próxima banana
        current_x += random.randint(50, WIDTH)

    for i in range(3):
        # Criando os robôs
        r = Robot(assets, HEIGHT-25, 100+50*i)
        all_sprites.add(r)
        all_robots.add(r)

    PLAYING = 0
    EXPLODING = 1
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3
    # ----- Gera saídas
    # Carrega o fundo do jogo
    background = assets['background']
    # Redimensiona o fundo
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()
    moving=False
    pulo = False
    desce =False
    delta_ms = 0
    delta_ms_down = 0
    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != QUIT and state != GAME_OVER:
        clock.tick(FPS)
        # A cada loop, redesenha o fundo e os sprites
        window.fill(BLACK)
        window.blit(background, background_rect)


        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = QUIT
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_RIGHT:
                        moving=True
                        b.speedx -= 8
                        # Faz todas as bananas se moverem em direção ao Minion
                        for banana in all_bananas:
                            banana.speedx = -world_speed  # Inverte a direção para ir ao encontro do Minion
                    if event.key == pygame.K_UP and not pulo and not desce:
                        delta_ms = pygame.time.get_ticks() + 400
                        pulo = True 
                        player.speedy -= 8
                            # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_RIGHT:
                            moving=False
                            b.speedx += 8
                            player.image = assets[MINION_STILL_IMG]
                            # Para o movimento das bananas quando o jogador para
                            for banana in all_bananas:
                                banana.speedx = 0
        if pygame.time.get_ticks() >  delta_ms and pulo:
            pulo = False
            desce = True
            delta_ms_down = pygame.time.get_ticks() + 400
            player.speedy += 16
    
        if pygame.time.get_ticks() > delta_ms_down and desce:
            desce = False
            player.speedy = 0

        if moving==True:
            player.image = assets[MINION_RUN_IMG]
            background_rect.x += world_speed
            
        # Desenha o fundo principal
        window.blit(background, background_rect)
        
        # Cria e desenha uma cópia do fundo logo após o primeiro
        background_rect2 = background_rect.copy()
        background_rect2.x = background_rect.right
        window.blit(background, background_rect2)
        
        # Se o fundo principal saiu completamente da tela, reseta sua posição
        if background_rect.right <= 0:
            background_rect.x = 0

        all_sprites.update()
    

        if state == PLAYING:
            hits = pygame.sprite.spritecollide(player, all_soros, True, pygame.sprite.collide_mask)
            for soro in hits:
                player.image = assets[PURPLE_MINION_IMG] 
                s = Soro(assets)
                all_sprites.add(s)
                all_soros.add(s)
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.spritecollide(player, all_bananas, True, pygame.sprite.collide_mask)
            for banana in hits:
                # O meteoro e destruido e precisa ser recriado
                b = Banana(assets, HEIGHT-25, banana.rect.centerx+100)
                # Se o jogador estiver se movendo, a nova banana também deve se mover
                if moving:
                    b.speedx = -world_speed  # Inverte a direção para ir ao encontro do Minion
                all_sprites.add(b)
                all_bananas.add(b)

                # Ganhou pontos!
                if player.image == assets[MINION_STILL_IMG] or player.image == assets[MINION_RUN_IMG]:
                    score += 1
                elif player.image == assets[PURPLE_MINION_IMG]:
                    score += 2

            # Verifica se houve colisão entre minion e robô
            hits = pygame.sprite.spritecollide(player, all_robots, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                player.kill()
                lives -= 1
                state = EXPLODING
                keys_down = {}
        elif state == EXPLODING:
            if lives == 0:
                state = GAME_OVER
            else:
                state = PLAYING
                player = Minion(groups, assets)
                all_sprites.add(player)

        all_sprites.draw(window)


        # Desenhando o score
        text_surface = assets[SCORE_FONT].render("{:08d}".format(score), True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_surface, text_rect)

        # Desenhando as vidas
        text_surface = assets[SCORE_FONT].render(chr(9829) * lives, True, RED)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  # Mostra o novo frame para o jogador
    return state 