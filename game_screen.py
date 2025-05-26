import pygame
import random
from config import FPS, WIDTH, HEIGHT, BLACK, YELLOW, RED, QUIT, GAME_OVER, INFO, INIT, GAME
from assets import load_assets, BACKGROUND, SCORE_FONT,MINION_STILL_IMG,MINION_RUN_IMG,PURPLE_MINION_IMG, GAME_OVER_SOUND
from sprites import Minion,Robot,Banana,Soro

world_speed=-10

# Variável global para armazenar o recorde
high_score = 0

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
    
    # Posição inicial para a primeira banana e robôs (começando bem depois do Minion)
    current_x = WIDTH + 200  # Começa uma tela depois do início
    
    # Lista para guardar posições ocupadas
    posicoes_ocupadas = []

    # Primeiro criamos os robôs para que apareçam antes das bananas
    for i in range(2):  # Reduzindo para apenas 2 robôs
        # Criando os robôs com espaçamento menor
        r = Robot(assets, HEIGHT-25, current_x)
        all_sprites.add(r)
        all_robots.add(r)
        # Guarda a região ocupada pelo robô (considerando sua largura)
        posicoes_ocupadas.append((current_x - 100, current_x + 100))  # 100 pixels de margem para cada lado
        # Adiciona um espaçamento aleatório entre 500 e 800 pixels para o próximo robô
        current_x += random.randint(500, 800)

    # Agora criamos as bananas depois dos robôs
    for i in range(10):
        # Tenta encontrar uma posição válida para a banana
        posicao_valida = False
        while not posicao_valida:
            # Verifica se a posição atual não está muito próxima de nenhum robô
            posicao_valida = True
            for inicio, fim in posicoes_ocupadas:
                if inicio - 50 <= current_x <= fim + 50:  # 50 pixels de margem de segurança
                    posicao_valida = False
                    current_x += 100  # Move um pouco para frente e tenta de novo
                    break
        
        # Escolhe aleatoriamente se a banana vai estar no chão ou no alto
        altura_banana = random.choice([HEIGHT-25, HEIGHT-150])
        # Criando as bananas com espaçamento aleatório
        b = Banana(assets, altura_banana, current_x)
        all_sprites.add(b)
        all_bananas.add(b)
        # Guarda a posição da banana
        posicoes_ocupadas.append((current_x - 30, current_x + 30))  # 30 pixels de margem para cada lado
        # Adiciona um espaçamento aleatório entre 50 e 150 pixels para a próxima banana
        current_x += random.randint(50, 150)

    PLAYING = 0
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
                        moving = True
                        # Faz todas as bananas se moverem em direção ao Minion
                        for banana in all_bananas:
                            banana.speedx = world_speed  # Inverte a direção para ir ao encontro do Minion
                        for robos in all_robots:
                            robos.speedx = world_speed
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
                            player.image = assets[MINION_STILL_IMG]
                            player.image.set_alpha(player.alpha)  # Mantém a opacidade atual
                            # Para o movimento das bananas quando o jogador para
                            for banana in all_bananas:
                                banana.speedx = 0
                            for robos in all_robots: 
                                robos.speedx = 0

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
            player.image.set_alpha(player.alpha)  # Mantém a opacidade atual
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
                altura_banana = random.choice([HEIGHT-25, HEIGHT-150])
                # Encontra a posição x mais distante entre todas as bananas existentes
                novo_x = max([b.rect.centerx for b in all_bananas]) + random.randint(200, 400) if all_bananas else player.rect.centerx + WIDTH
                # Cria uma nova banana
                b = Banana(assets, altura_banana, novo_x)
                if moving:
                    b.speedx = world_speed
                all_sprites.add(b)
                all_bananas.add(b)

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
                if player.image == assets[MINION_STILL_IMG] or player.image == assets[MINION_RUN_IMG]:
                    score += 1
                elif player.image == assets[PURPLE_MINION_IMG]:
                    score += 2

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
                if moving:
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