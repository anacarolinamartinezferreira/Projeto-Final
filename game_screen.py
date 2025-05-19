import pygame
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED
from assets import load_assets, BACKGROUND, SCORE_FONT,MINION_STILL_IMG,MINION_RUN_IMG,PURPLE_MINION_IMG
from sprites import Minion,Robot,Banana,Soro


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
    

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    keys_down[event.key] = True
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_UP:
                        player.speedy += 8
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 8
                        if event.key == pygame.K_UP:
                            player.speedy += 8

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos meteoros
        all_sprites.update()

        if state == PLAYING:
            hits = pygame.sprite.groupcollide(all_soros, True, True, pygame.sprite.collide_mask)
            for soro in hits:
                Minion.image = assets[PURPLE_MINION_IMG] 
                s = Soro(assets)
                all_sprites.add(s)
                all_soros.add(s)
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.groupcollide(all_bananas, True, True, pygame.sprite.collide_mask)
            for banana in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                b = Banana(assets)
                all_sprites.add(b)
                all_robots.add(b)

                # Ganhou pontos!
                if Minion.image == assets[MINION_STILL_IMG] or Minion.image == assets[MINION_RUN_IMG]:
                    score += 1
                elif Minion.image == assets[PURPLE_MINION_IMG]:
                    score += 2

            # Verifica se houve colisão entre nave e meteoro
            hits = pygame.sprite.spritecollide(player, all_robots, True, pygame.sprite.collide_mask)
            if len(hits) > 0:
                # Toca o som da colisão
                player.kill()
                lives -= 1
                state = EXPLODING
                keys_down = {}
        elif state == EXPLODING:
            if lives == 0:
                state = DONE
            else:
                state = PLAYING
                player = Minion(groups, assets)
                all_sprites.add(player)

        # ----- Gera saídas
        window.fill(BLACK)  # Preenche com a cor branca
        window.blit(assets[BACKGROUND], (0, 0))
        # Desenhando meteoros
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