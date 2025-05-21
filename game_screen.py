import pygame
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
    


    for i in range(10):
        # Criando as bananas
        b = Banana(assets, HEIGHT-25, 100+50*i)
        all_sprites.add(b)
        all_bananas.add(b)
    for i in range(3):
        # Criando os robôs
        r = Robot(assets)
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

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != QUIT and state != GAME_OVER:
        clock.tick(FPS)

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
                        all_sprites.update()
                        # A cada loop, redesenha o fundo e os sprites
                        window.fill(BLACK)
                        # Atualiza a posição da imagem de fundo.
                        background_rect.x += world_speed
                        # Se o fundo saiu da janela, faz ele voltar para dentro.
                        if background_rect.right < 0:
                            background_rect.x += background_rect.width
                            # Desenha o fundo e uma cópia para a direita.
                            # Assumimos que a imagem selecionada ocupa pelo menos o tamanho da janela.
                            # Além disso, ela deve ser cíclica, ou seja, o lado esquerdo deve ser continuação do direito.
                            window.blit(background, background_rect)
                            # Desenhamos a imagem novamente, mas deslocada da largura da imagem em x.
                            background_rect2 = background_rect.copy()
                            background_rect2.x += background_rect2.width
                            window.blit(background, background_rect2)

                        all_sprites.draw(window)
                    # Depois de desenhar tudo, inverte o display.
                    pygame.display.flip()                        
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_RIGHT:
                            player.image = assets[MINION_STILL_IMG]

        if state == PLAYING:
            hits = pygame.sprite.spritecollide(player, all_soros, True, pygame.sprite.collide_mask)
            for soro in hits:
                player.image = assets[PURPLE_MINION_IMG] 
                s = Soro(assets)
                all_sprites.add(s)
                all_soros.add(s)
            # Verifica se houve colisão entre tiro e meteoro
            hits = pygame.sprite.spritecollide(player, all_bananas, True, pygame.sprite.collide_mask)
            for banana in hits: # As chaves são os elementos do primeiro grupo (meteoros) que colidiram com alguma bala
                # O meteoro e destruido e precisa ser recriado
                b = Banana(assets, HEIGHT-25, banana.rect.centerx+100)
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