import pygame
import random
import math

pygame.init()

# Dimensões da janela do jogo
LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pinguim no Gelo")

clock = pygame.time.Clock()

# Paleta de cores usada no jogo
AZUL = (70, 220, 255)
BRANCO = (255,255,255)
PRETO = (20,20,20)
CINZA = (210,210,210)
AZUL_GELO = (120,180,255)
LARANJA = (255,160,0)

fonte = pygame.font.SysFont(None,36)

# -----------------------
# Jogador
# -----------------------

# Posição inicial do pinguim (centralizado horizontalmente, perto da base da tela)
jogador_x = LARGURA//2
jogador_y = ALTURA-70
velocidade = 8  # velocidade de movimento lateral do jogador

# -----------------------
# Buracos
# -----------------------

# Lista que guarda todos os buracos ativos na tela
buracos = []

spawn = 0            # contador usado para controlar o intervalo entre criação de buracos
pontos = 0            # pontuação do jogador
velocidade_jogo = 6   # velocidade com que os buracos se movem em direção ao jogador

rodando = True
def desenhar_pista():
    # Desenha o fundo (céu) e a pista com efeito de perspectiva

    # Céu
    tela.fill((60, 215, 255))

    # Pista (formato de trapézio para simular profundidade/distância)
    pygame.draw.polygon(
        tela,
        (250,250,250),
        [
            (170,80),
            (630,80),
            (800,600),
            (0,600)
        ]
    )

    # Barranco esquerdo
    # Desenha várias elipses ao longo do eixo Y para simular a borda de neve
    # ficando mais larga conforme se aproxima da câmera (efeito de perspectiva)
    for y in range(85, 600, 18):

        t = (y-80)/(600-80)  # fator de interpolação de 0 (topo/longe) a 1 (base/perto)

        x = 170*(1-t)  # posição X do barranco convergindo para o ponto de fuga

        largura = 8 + t*35  # a largura aumenta conforme t cresce (mais perto = mais largo)

        # camada clara (base da borda)
        pygame.draw.ellipse(
            tela,
            (245,245,245),
            (x-largura/2, y, largura, 10+t*6)
        )

        # camada um pouco mais escura por cima, dando volume
        pygame.draw.ellipse(
            tela,
            (200,200,200),
            (x-largura/2, y+5, largura, 5+t*4)
        )

    # Barranco direito
    # Mesma lógica do barranco esquerdo, espelhada para o outro lado da pista
    for y in range(85,600,18):

        t = (y-80)/(600-80)

        x = 630 + (800-630)*t

        largura = 8+t*35

        pygame.draw.ellipse(
            tela,
            (245,245,245),
            (x-largura/2,y,largura,10+t*6)
        )

        pygame.draw.ellipse(
            tela,
            (200,200,200),
            (x-largura/2,y+5,largura,5+t*4)
        ) 
# -----------------------
# Loop principal do jogo
# -----------------------
while rodando:

    clock.tick(60)  # limita o jogo a 60 quadros por segundo

    # Trata os eventos do pygame (fechar janela, etc.)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Captura o estado atual das teclas pressionadas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jogador_x -= velocidade

    if teclas[pygame.K_RIGHT]:
        jogador_x += velocidade

    # limites da pista (impede o jogador de sair da área jogável)
    jogador_x = max(+120, min(LARGURA-120, jogador_x))

    spawn += 1

    # A cada 25 quadros, cria um novo buraco em uma posição X aleatória
    if spawn > 25:
        spawn = 0

        buracos.append({
            "x": random.randint(140,660),
            "y": 90,
            "r": 5
        })

    desenhar_pista()

    # sombras laterais (dão profundidade às bordas da pista)
    pygame.draw.polygon(
        tela,
        CINZA,
        [(0,600),(120,80),(80,80),(0,600)]
    )

    pygame.draw.polygon(
        tela,
        CINZA,
        [(800,600),(680,80),(720,80),(800,600)]
    )

    novos = []  # lista auxiliar para manter apenas os buracos ainda visíveis na tela

    for b in buracos:

        b["y"] += velocidade_jogo  # move o buraco em direção ao jogador (para baixo)

        # aumenta o raio do buraco conforme ele se aproxima, reforçando a perspectiva
        escala = (b["y"]/ALTURA)

        raio = max(5, int(35*escala))

        pygame.draw.ellipse(
            tela,
            PRETO,
            (
                b["x"]-raio,
                b["y"]-raio//2,
                raio*2,
                raio
            )
        )

        # colisão: calcula a distância entre o jogador e o centro do buraco
        dx = jogador_x-b["x"]
        dy = jogador_y-b["y"]

        # se a distância for menor que a soma dos raios, houve colisão e o jogo termina
        if math.sqrt(dx*dx+dy*dy) < raio+18:
            rodando = False

        # mantém o buraco na lista enquanto ele não sair da tela;
        # quando sai, soma um ponto (o jogador desviou com sucesso)
        if b["y"] < ALTURA+50:
            novos.append(b)
        else:
            pontos += 1

    buracos = novos

    # -----------------------
    # Desenha pinguim
    # -----------------------

    # Corpo (elipse preta)
    pygame.draw.ellipse(
        tela,
        PRETO,
        (jogador_x-18,jogador_y-28,36,52)
    )

    # Barriga (elipse branca por cima do corpo)
    pygame.draw.ellipse(
        tela,
        BRANCO,
        (jogador_x-10,jogador_y-8,20,22)
    )

    # Bico (triângulo laranja)
    pygame.draw.polygon(
        tela,
        LARANJA,
        [
            (jogador_x,jogador_y),
            (jogador_x+10,jogador_y+4),
            (jogador_x,jogador_y+8)
        ]
    )

    # Exibe a pontuação atual no canto superior esquerdo
    texto = fonte.render(f"Pontos: {pontos}",True,PRETO)
    tela.blit(texto,(20,20))

    pygame.display.flip()  # atualiza a tela com tudo que foi desenhado neste quadro

# -----------------------
# Tela Game Over
# -----------------------

# Ao sair do loop principal (colisão ou fechamento da janela), exibe a tela final
tela.fill((20,20,40))

txt1 = fonte.render("GAME OVER",True,(255,255,255))
txt2 = fonte.render(f"Pontuação: {pontos}",True,(255,255,255))

tela.blit(txt1,(LARGURA//2-90,250))
tela.blit(txt2,(LARGURA//2-90,300))

pygame.display.flip()

pygame.time.wait(3000)  # mantém a tela de game over visível por 3 segundos

pygame.quit()