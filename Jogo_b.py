import pygame
import random

# -----------------------------
# INICIALIZA O PYGAME
# -----------------------------
pygame.init()

#Fonte
fonte = pygame.font.SysFont("Arial", 30)
fonte_gameover = pygame.font.SysFont("Arial", 30)

# -----------------------------
# TAMANHO DA JANELA DO JOGO
# -----------------------------
LARGURA, ALTURA = (1100, 800)
tela = pygame.display.set_mode((LARGURA, ALTURA))

# Título da janela
pygame.display.set_caption("A Lapada")

# -----------------------------
# CORES (PODEM SER USADAS DEPOIS)
# -----------------------------
BRANCO    = (255, 255, 255)
PRETO     = (0, 0, 0)
CINZA     = (220, 220, 220)
HOVER     = (173, 216, 230)
VERDE     = (50, 200, 50)
AZUL      = (50, 50, 200)
VERMELHO  = (200, 50, 50)

# -----------------------------
# CARREGANDO O FUNDO DO JOGO
# -----------------------------
fundo = pygame.image.load("imagens/fundo.gif")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# -----------------------------
# CARREGANDO O PERSONAGEM (HERÓI)
# -----------------------------
heroi = pygame.image.load("imagens/hero.png")
heroi = pygame.transform.scale(heroi, (64, 64))

# -----------------------------
# CARREGANDO O INIMIGO
# -----------------------------
imagem_inimigo = pygame.image.load("imagens/gaspar.png")
imagem_inimigo = pygame.transform.scale(imagem_inimigo, (32, 32))

# -----------------------------
# CARREGANDO O TIRO
# -----------------------------
tiro = pygame.image.load("imagens/tiro.png")
bala = pygame.transform.scale(tiro, (64, 64))

# -----------------------------
# POSIÇÃO DO HERÓI
# -----------------------------
heroi_x = 100
heroi_y = 200

# Velocidade do herói
velocidade = 3

# -----------------------------
# TIROS
# -----------------------------
projeteis = []

limite_tiros = 5
tempo_entre_tiros = 350
ultimo_tiro = 0

# -----------------------------
# CLASSE DO INIMIGO
# -----------------------------
class Inimigo:

    def __init__(self):

        self.x = random.randint(150, LARGURA - 32)
        self.y = random.randint(0, ALTURA - 32)

        self.velocidade = 1

        self.direcao_x = random.choice([-1, 0, 1])
        self.direcao_y = random.choice([-1, 0, 1])

        while self.direcao_x == 0 and self.direcao_y == 0:
            self.direcao_x = random.choice([-1, 0, 1])
            self.direcao_y = random.choice([-1, 0, 1])

        self.tempo_troca = 1000
        self.ultima_troca = pygame.time.get_ticks()

    def mover(self):

        agora = pygame.time.get_ticks()

        # Troca de direção
        if agora - self.ultima_troca > self.tempo_troca:

            self.direcao_x = random.choice([-1, 0, 1])
            self.direcao_y = random.choice([-1, 0, 1])

            while self.direcao_x == 0 and self.direcao_y == 0:
                self.direcao_x = random.choice([-1, 0, 1])
                self.direcao_y = random.choice([-1, 0, 1])

            self.ultima_troca = agora

        # Movimento
        self.x += self.direcao_x * self.velocidade
        self.y += self.direcao_y * self.velocidade

        # Limites da tela
        if self.x < 0:
            self.x = 0
            self.direcao_x *= -1

        if self.x > LARGURA - 32:
            self.x = LARGURA - 32
            self.direcao_x *= -1

        if self.y < 0:
            self.y = 0
            self.direcao_y *= -1

        if self.y > ALTURA - 32:
            self.y = ALTURA - 32
            self.direcao_y *= -1

    def desenhar(self):
        tela.blit(imagem_inimigo, (self.x, self.y))

# -----------------------------
# CRIANDO OS INIMIGOS
# -----------------------------
quantidade = random.randint(3, 4)

inimigos = []

for i in range(quantidade):
    inimigos.append(Inimigo())

#Pontuação
pontuacao = 0
ultimo_ponto = pygame.time.get_ticks()

# -----------------------------
# LOOP PRINCIPAL DO JOGO
# -----------------------------
rodando = True
game_over = False
while rodando:

    # -------------------------
    # VERIFICA EVENTOS
    # -------------------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    agora = pygame.time.get_ticks()

    # -------------------------
    # VERIFICA TECLAS
    # -------------------------
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        heroi_x -= velocidade

    if teclas[pygame.K_RIGHT]:
        heroi_x += velocidade

    if teclas[pygame.K_UP]:
        heroi_y -= velocidade

    if teclas[pygame.K_DOWN]:
        heroi_y += velocidade

        # -------------------------
    # LIMITANDO O MOVIMENTO DO HERÓI
    # -------------------------
    if heroi_x < 0:
        heroi_x = 0

    if heroi_x > LARGURA - 64:
        heroi_x = LARGURA - 64

    if heroi_y < 0:
        heroi_y = 0

    if heroi_y > ALTURA - 64:
        heroi_y = ALTURA - 64

    # -------------------------
    # DISPARO DOS TIROS
    # -------------------------
    if teclas[pygame.K_SPACE]:

        if len(projeteis) < limite_tiros:

            if agora - ultimo_tiro > tempo_entre_tiros:

                projeteis.append([heroi_x + 60, heroi_y + 24])

                ultimo_tiro = agora

    # -------------------------
    # MOVIMENTO DOS TIROS
    # -------------------------
    for p in projeteis:
        p[0] += 5

    projeteis = [p for p in projeteis if p[0] < LARGURA]

    # -------------------------
    # MOVIMENTO DOS INIMIGOS
    # -------------------------
    for inimigo in inimigos:
        inimigo.mover()

    # -------------------------
    # GERA NOVOS INIMIGOS
    # -------------------------
    if len(inimigos) < 3:

        # pequena chance de nascer um novo inimigo
        if random.randint(1, 300) == 10:

            inimigos.append(Inimigo())

    # -------------------------
    # COLISÃO ENTRE TIROS E INIMIGOS
    # -------------------------
    for tiro in projeteis[:]:

        for inimigo in inimigos[:]:

          if (tiro[0] < inimigo.x + 32 and
            tiro[0] + 64 > inimigo.x and
            tiro[1] < inimigo.y + 32 and
            tiro[1] + 64 > inimigo.y):

            projeteis.remove(tiro)
            inimigos.remove(inimigo)
        break

    # -------------------------
    # COLISÃO HERÓI X INIMIGO
    # -------------------------

    heroi_rect = pygame.Rect(heroi_x, heroi_y, 64, 64)

    for inimigo in inimigos:

        inimigo_rect = pygame.Rect(inimigo.x, inimigo.y, 32, 32)

        if heroi_rect.colliderect(inimigo_rect):
            game_over = True            


    agora = pygame.time.get_ticks()
    # -----------------------------
    # PONTUAÇÃO POR TEMPO
    # -----------------------------
    if agora - ultimo_ponto >= 2000:
        pontuacao += 10
        ultimo_ponto = agora

    # -------------------------
    # DESENHO NA TELA
    # -------------------------
    tela.blit(fundo, (0, 0))
    #Adicionando placa na tela
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (20, 20))

    # Desenha o herói
    tela.blit(heroi, (heroi_x, heroi_y))

    # Desenha todos os inimigos
    for inimigo in inimigos:
        inimigo.desenhar()

    # Desenha os tiros
    for p in projeteis:
        tela.blit(bala, (p[0], p[1]))
    
        # -------------------------
    # CONTADOR DE FPS
    # -------------------------
    pygame.display.set_caption(
        f"A Lapada - Inimigos: {len(inimigos)}"
    )



       # -------------------------
    # DESENHO NA TELA
    # -------------------------
    tela.blit(fundo, (0, 0))

    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (20, 20))

    tela.blit(heroi, (heroi_x, heroi_y))

    for inimigo in inimigos:
        inimigo.desenhar()

    for p in projeteis:
        tela.blit(bala, (p[0], p[1]))

    pygame.display.set_caption(
        f"A Lapada - Inimigos: {len(inimigos)}"
    )

    # -------------------------
    # GAME OVER CORRETO
    # -------------------------
    if not game_over:

        pygame.display.flip()

    else:

        tela.fill(PRETO)

        texto = fonte_gameover.render("GAME OVER", True, VERMELHO)
        tela.blit(texto, (300, 250))

        texto2 = fonte.render(f"Pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto2, (350, 360))

        pygame.display.flip()

        pygame.time.delay(3000)

        rodando = False

# -----------------------------
# FINALIZA O JOGO
# -----------------------------
pygame.quit()