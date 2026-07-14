import pygame
import random
import math

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pinguim no Gelo")

clock = pygame.time.Clock()

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

jogador_x = LARGURA//2
jogador_y = ALTURA-70
velocidade = 8

# -----------------------
# Buracos
# -----------------------

buracos = []

spawn = 0
pontos = 0
velocidade_jogo = 6

rodando = True
def desenhar_pista():

    # Céu
    tela.fill((60, 215, 255))

    # Pista
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
    for y in range(85, 600, 18):

        t = (y-80)/(600-80)

        x = 170*(1-t)

        largura = 8 + t*35

        pygame.draw.ellipse(
            tela,
            (245,245,245),
            (x-largura/2, y, largura, 10+t*6)
        )

        pygame.draw.ellipse(
            tela,
            (200,200,200),
            (x-largura/2, y+5, largura, 5+t*4)
        )

    # Barranco direito
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
while rodando:

    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jogador_x -= velocidade

    if teclas[pygame.K_RIGHT]:
        jogador_x += velocidade

    # limites da pista
    jogador_x = max(200, min(LARGURA-200, jogador_x))

    spawn += 1

    if spawn > 25:
        spawn = 0

        buracos.append({
            "x": random.randint(140,660),
            "y": 90,
            "r": 5
        })

    desenhar_pista()

    # sombras laterais
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

    novos = []

    for b in buracos:

        b["y"] += velocidade_jogo

        # aumenta conforme aproxima
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

        # colisão
        dx = jogador_x-b["x"]
        dy = jogador_y-b["y"]

        if math.sqrt(dx*dx+dy*dy) < raio+18:
            rodando = False

        if b["y"] < ALTURA+50:
            novos.append(b)
        else:
            pontos += 1

    buracos = novos

    # -----------------------
    # Desenha pinguim
    # -----------------------

    pygame.draw.ellipse(
        tela,
        PRETO,
        (jogador_x-18,jogador_y-28,36,52)
    )

    pygame.draw.ellipse(
        tela,
        BRANCO,
        (jogador_x-10,jogador_y-8,20,22)
    )

    pygame.draw.polygon(
        tela,
        LARANJA,
        [
            (jogador_x,jogador_y),
            (jogador_x+10,jogador_y+4),
            (jogador_x,jogador_y+8)
        ]
    )

    texto = fonte.render(f"Pontos: {pontos}",True,PRETO)
    tela.blit(texto,(20,20))

    pygame.display.flip()

# -----------------------
# Tela Game Over
# -----------------------

tela.fill((20,20,40))

txt1 = fonte.render("GAME OVER",True,(255,255,255))
txt2 = fonte.render(f"Pontuação: {pontos}",True,(255,255,255))

tela.blit(txt1,(LARGURA//2-90,250))
tela.blit(txt2,(LARGURA//2-90,300))

pygame.display.flip()

pygame.time.wait(3000)

pygame.quit()