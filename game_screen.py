import pygame
import random
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, QUIT, GAME_OVER, INFO, INIT, GAME
from assets import load_assets, BACKGROUND, SCORE_FONT,MINION_STILL_IMG,MINION_RUN_IMG,PURPLE_MINION_IMG, GAME_OVER_SOUND
from sprites import Minion,Robot,Banana,Soro

world_speed=-10 # Velocidade que a tela moverá

high_score = 0 # Variável para armazenar o recorde

def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # Criando grupos
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
    
    # Posição inicial para a primeira banana e robôs (depois do Minion)
    current_x = WIDTH + 200  # Começa uma tela depois do início
    
    # Lista para guardar posições ocupadas
    posicoes_ocupadas = []

    # Criando bananas primeiro
    for i in range(10):
        posicao_valida = False
        while not posicao_valida:
            posicao_valida = True
            for inicio, fim in posicoes_ocupadas:
                if inicio - 50 <= current_x <= fim + 50:
                    posicao_valida = False
                    current_x += 100
                    break
        
        altura_banana = random.choice([HEIGHT-25,HEIGHT-150])
        b = Banana(assets, altura_banana, current_x)
        all_sprites.add(b)
        all_bananas.add(b)
        current_x += random.randint(50, 150)

    # Criando robôs depois das bananas
    for i in range(2):
        r = Robot(assets, HEIGHT-25, current_x)
        all_sprites.add(r)
        all_robots.add(r)
        current_x += random.randint(500, 800)

    # Criando soro por último e bem mais longe
    for i in range(1):  # Apenas 1 soro
        altura_soro = random.choice([HEIGHT-25, HEIGHT-150])
        s = Soro(assets, altura_soro, current_x + 2000)  # Começa muito mais à frente, após bananas e robôs
        all_sprites.add(s)
        all_soros.add(s)

    PLAYING = 0
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3
 
    # Carrega o fundo do jogo
    background = assets['background']
    # Redimensiona o fundo
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

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
            # Verifica o teclado se está no estado de jogo
            if state == PLAYING:

                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera o estado de movimento
                    keys_down[event.key] = True
                    if event.key == pygame.K_RIGHT:
                        moving = True
                        player.moving = True
                        # Faz todas as bananas se moverem 
                        for banana in all_bananas:
                            banana.speedx = world_speed 
                        # Faz todos os robôs se moverem
                        for robos in all_robots:
                            robos.speedx = world_speed
                        # Faz todos os soros se moverem 
                        for soro in all_soros:
                            soro.speedx = world_speed
                    if event.key == pygame.K_UP and not pulo and not desce:
                        delta_ms = pygame.time.get_ticks() + 400
                        pulo = True # Incia o pulo
                        player.speedy -= 8

                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera o estado de movimento
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_RIGHT:
                            moving = False
                            player.moving = False
                            if player.is_purple:
                                player.image = assets[PURPLE_MINION_IMG]
                            else:
                                player.image = assets[MINION_STILL_IMG]
                            player.image.set_alpha(player.alpha)
                            # Para o movimento das bananas quando o jogador para
                            for banana in all_bananas:
                                banana.speedx = 0
                            # Para o movimento dos robôs quando o jogador para
                            for robos in all_robots: 
                                robos.speedx = 0
                            # Para o movimento dos soros quando o jogador para 
                            for soro in all_soros:
                                soro.speedx = 0
        
        # Fazendo o minion pular e, em seguida, descer
        if pygame.time.get_ticks() >  delta_ms and pulo:
            pulo = False
            desce = True # Incia descida
            delta_ms_down = pygame.time.get_ticks() + 400
            player.speedy += 16
    
        if pygame.time.get_ticks() > delta_ms_down and desce:
            desce = False
            player.speedy = 0


        if player.moving:
            if player.is_purple:
                player.image = assets[PURPLE_MINION_IMG]
            else:
                player.image = assets[MINION_RUN_IMG]
            player.image.set_alpha(player.alpha)  # Mantém a opacidade atual
            background_rect.x += world_speed
            
        window.blit(background, background_rect)
        # Cria e desenha uma cópia do fundo logo após o primeiro
        background_rect2 = background_rect.copy()
        background_rect2.x = background_rect.right
        window.blit(background, background_rect2)
        # Se o fundo principal saiu completamente da tela, reseta sua posição
        if background_rect.right <= 0:
            background_rect.x = 0

        all_sprites.update()
    
        # Verifica se há robôs que ficaram para trás e os recria à frente
        for robo in all_robots:
            if robo.rect.right < 0:  # Se o robô saiu completamente da tela pela esquerda
                # Remove o robô antigo
                robo.kill()
                # Encontra a posição x mais distante entre todos os robôs existentes
                novo_x = max([r.rect.centerx for r in all_robots]) + random.randint(500, 800) if all_robots else player.rect.centerx + WIDTH
                # Cria um novo robô
                r = Robot(assets, HEIGHT-25, novo_x)
                if moving:
                    r.speedx = world_speed
                all_sprites.add(r)
                all_robots.add(r)

        # Verifica se há bananas que ficaram para trás e as recria à frente
        for banana in all_bananas:
            if banana.rect.right < 0:  # Se a banana saiu completamente da tela pela esquerda
                # Remove a banana antiga
                banana.kill()
                # Escolhe uma altura aleatória para a nova banana
                altura_banana = random.choice([HEIGHT-25,HEIGHT-150])
                # Encontra a posição x mais distante entre todas as bananas existentes
                novo_x = max([b.rect.centerx for b in all_bananas]) + random.randint(200, 400) if all_bananas else player.rect.centerx + WIDTH
                # Cria uma nova banana
                b = Banana(assets, altura_banana, novo_x)
                # Se o jogador estiver se movendo, a nova banana também deve se mover
                if moving:
                    b.speedx = world_speed
                all_sprites.add(b)
                all_bananas.add(b)

        # Verifica se há soros que ficaram para trás e os recria à frente
        for soro in all_soros:
            if soro.rect.right < 0:  # Se o soro saiu completamente da tela pela esquerda
                soro.kill()
                # Encontra a posição x mais distante entre todos os soros existentes e adiciona uma distância muito maior
                novo_x = max([s.rect.centerx for s in all_soros]) + random.randint(6000, 8000) if all_soros else player.rect.centerx + WIDTH + 6000
                altura_soro = random.choice([HEIGHT-25, HEIGHT-150])
                s = Soro(assets, altura_soro, novo_x)
                if player.moving:
                    s.speedx = world_speed
                all_sprites.add(s)
                all_soros.add(s)

        if state == PLAYING:
            # Verifica colisão com soro
            hits = pygame.sprite.spritecollide(player, all_soros, True, pygame.sprite.collide_mask)
            for soro in hits:
                player.turn_purple()
                
                # Cria um novo soro muito mais à frente
                novo_x = max([s.rect.centerx for s in all_soros]) + random.randint(6000, 8000) if all_soros else player.rect.centerx + WIDTH + 6000
                altura_soro = random.choice([HEIGHT-25, HEIGHT-150])
                s = Soro(assets, altura_soro, novo_x)
                if player.moving:
                    s.speedx = world_speed
                all_sprites.add(s)
                all_soros.add(s)
            
            # Verifica se houve colisão entre minion e banana
            hits = pygame.sprite.spritecollide(player, all_bananas, True, pygame.sprite.collide_mask)
            for banana in hits:
                # Encontra uma posição válida para a nova banana
                posicao_valida = False
                novo_x = max([b.rect.centerx for b in all_bananas]) + random.randint(200, 400) if all_bananas else player.rect.centerx + WIDTH
                while not posicao_valida:
                    posicao_valida = True
                    # Verifica se há robôs próximos
                    for robo in all_robots:
                        if abs(robo.rect.centerx - novo_x) < 150:  # 150 pixels de distância mínima
                            posicao_valida = False
                            novo_x += 100
                            break
                # Escolhe uma altura aleatória para a nova banana
                altura_banana = random.choice([HEIGHT-25, HEIGHT-150])
                # Cria a nova banana bem mais longe
                b = Banana(assets, altura_banana, novo_x)
                # Se o jogador estiver se movendo, a nova banana também deve se mover
                if moving:
                    b.speedx = world_speed
                all_sprites.add(b)
                all_bananas.add(b)

                # Ganhou pontos!
                if player.is_purple:  # Se estiver com o poder do minion roxo
                    score += 2
                else:  # Se estiver normal
                    score += 1

            # Verifica se houve colisão entre minion e robô
            hits = pygame.sprite.spritecollide(player, all_robots, True, pygame.sprite.collide_mask)
            for robos in hits:
                # Encontra uma posição válida para o novo robô
                posicao_valida = False
                novo_x = max([r.rect.centerx for r in all_robots]) + random.randint(500, 800) if all_robots else player.rect.centerx + WIDTH
                while not posicao_valida:
                    posicao_valida = True
                    # Verifica se há bananas próximas
                    for banana in all_bananas:
                        if abs(banana.rect.centerx - novo_x) < 150:  # 150 pixels de distância mínima
                            posicao_valida = False
                            novo_x += 100
                            break
                
                # O robô é destruido e precisa ser recriado bem mais à frente
                r = Robot(assets, HEIGHT-25, novo_x)
                # Se o jogador estiver se movendo, o novo robô também deve se mover
                if player.moving:
                    r.speedx = world_speed
                all_sprites.add(r)
                all_robots.add(r)
                
                # Só toma dano se não estiver invencível
                if player.tomar_dano():
                    lives -= 1
                    if lives == 0:
                        state = GAME_OVER
                        # Atualiza o recorde se necessário
                        global high_score
                        if score > high_score:
                            high_score = score
                        return state, score, high_score

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
    
    # Se o jogo terminar por outro motivo, também retorna as pontuações
    return state, score, high_score 