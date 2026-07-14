# ==============================================================
# JOGO: PINGUIM NO GELO
# O pinguim anda sozinho pelo gelo; você só controla esquerda/direita.
# Desvie dos buracos (matam na hora) e dos blocos de gelo (invertem
# os controles por alguns segundos). Céu com ciclo dia/noite.
# ==============================================================

import pygame   # biblioteca principal para criar jogos 2D em Python
import random   # usada para sortear posições e tipos de obstáculo
import math     # usada para calcular o ciclo suave de dia/noite (seno/cosseno)
import sys      # usada para encerrar o programa corretamente

# --------------------------------------------------------------
# 1. INICIALIZAÇÃO DO PYGAME E DA JANELA
# --------------------------------------------------------------

pygame.init()        # inicializa todos os módulos internos do pygame
pygame.mixer.init()  # inicializa o módulo de áudio separadamente

LARGURA = 800   # largura da janela em pixels
ALTURA = 600    # altura da janela em pixels

tela = pygame.display.set_mode((LARGURA, ALTURA))                 # cria a janela do jogo
pygame.display.set_caption("Pinguim no Gelo - Desvie dos Buracos e Blocos")  # título da janela

# --------------------------------------------------------------
# 2. CORES (formato RGB)
# --------------------------------------------------------------

BRANCO       = (255, 255, 255)
PRETO        = (0, 0, 0)
LARANJA      = (255, 140, 0)
VERMELHO     = (220, 40, 40)
VERDE        = (0, 180, 0)
AMARELO      = (255, 220, 0)

GELO_CLARO   = (210, 240, 250)   # cor principal do chão de gelo
GELO_SOMBRA  = (170, 215, 235)   # linhas de textura do gelo

BURACO_COR   = (20, 20, 30)      # centro escuro do buraco
BURACO_BORDA = (55, 55, 75)      # borda do buraco (efeito de profundidade)

BLOCO_COR    = (190, 235, 250)   # cor do bloco de gelo
BLOCO_BRILHO = (255, 255, 255)   # brilho/contorno do bloco de gelo

DIA_CEU      = (135, 206, 250)   # cor do céu de dia
NOITE_CEU    = (10, 10, 45)      # cor do céu de noite
NUVEM_DIA    = (255, 255, 255)   # cor das nuvens de dia
NUVEM_NOITE  = (90, 90, 115)     # cor das nuvens de noite (mais escuras/discretas)

# --------------------------------------------------------------
# 3. CONTROLE DE TEMPO (FPS) E FONTES DE TEXTO
# --------------------------------------------------------------

relogio = pygame.time.Clock()  # objeto usado para controlar a velocidade do jogo
FPS = 60                        # quadros por segundo desejados

fonte_hud    = pygame.font.SysFont("Arial", 26)             # fonte da pontuação
fonte_aviso  = pygame.font.SysFont("Arial", 30, bold=True)  # fonte do aviso "CONTROLES INVERTIDOS!"
fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)  # fonte de "GAME OVER"
fonte_botao  = pygame.font.SysFont("Arial", 24, bold=True)  # fonte do botão reiniciar

# --------------------------------------------------------------
# 4. MÚSICA DE FUNDO
# --------------------------------------------------------------
# Coloque "musica_fundo.mp3" na mesma pasta deste script para tocar.
# Se o arquivo não existir, o jogo simplesmente continua sem som.

try:
    pygame.mixer.music.load("musica_fundo.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # -1 = toca em loop infinito
except pygame.error:
    print("Aviso: 'musica_fundo.mp3' não encontrado. O jogo seguirá sem música.")


# --------------------------------------------------------------
# 5. CONSTANTES DE CENÁRIO E DE JOGO
# --------------------------------------------------------------

CEU_ALTURA = 200               # altura (em pixels) da faixa de céu no topo da tela
DURACAO_CICLO_MS = 30000       # duração de um ciclo completo de dia -> noite -> dia (30s)
DURACAO_INVERSAO_MS = 3000     # tempo (ms) que os controles ficam invertidos após bater num bloco


# --------------------------------------------------------------
# 6. FUNÇÕES DO CENÁRIO (CÉU, NUVENS, ESTRELAS, CHÃO DE GELO)
# --------------------------------------------------------------

def gerar_nuvens(quantidade=4):
    # cria uma lista de nuvens com posição, tamanho e velocidade aleatórios
    nuvens = []
    for _ in range(quantidade):
        nuvens.append({
            "x": random.randint(0, LARGURA),
            "y": random.randint(20, CEU_ALTURA - 60),
            "raio": random.randint(18, 30),
            # velocidade aleatória: algumas nuvens vão para a direita, outras para a esquerda
            "velocidade": random.choice([-1, 1]) * random.uniform(0.3, 0.8),
        })
    return nuvens


def mover_nuvens(nuvens):
    for nuvem in nuvens:
        nuvem["x"] += nuvem["velocidade"]  # desloca a nuvem horizontalmente
        # quando a nuvem sai por um lado da tela, ela reaparece no lado oposto
        if nuvem["x"] > LARGURA + 60:
            nuvem["x"] = -60
        elif nuvem["x"] < -60:
            nuvem["x"] = LARGURA + 60


def desenhar_nuvem(tela, nuvem, cor):
    # desenha uma "nuvem" simples usando vários círculos sobrepostos
    x, y, r = nuvem["x"], nuvem["y"], nuvem["raio"]
    pygame.draw.circle(tela, cor, (int(x), int(y)), r)
    pygame.draw.circle(tela, cor, (int(x - r * 0.7), int(y + 5)), int(r * 0.7))
    pygame.draw.circle(tela, cor, (int(x + r * 0.7), int(y + 5)), int(r * 0.7))
    pygame.draw.circle(tela, cor, (int(x), int(y - r * 0.4)), int(r * 0.6))


def gerar_estrelas(quantidade=40):
    # gera posições fixas de estrelas dentro da faixa do céu (usadas só à noite)
    return [(random.randint(0, LARGURA), random.randint(0, CEU_ALTURA - 10), random.randint(1, 3))
            for _ in range(quantidade)]


def calcular_fator_noite(tempo_ms):
    # calcula um valor entre 0.0 (dia total) e 1.0 (noite total) que varia suavemente com o tempo
    angulo = (tempo_ms % DURACAO_CICLO_MS) / DURACAO_CICLO_MS * (2 * math.pi)
    return (1 - math.cos(angulo)) / 2  # começa em 0 (dia), sobe até 1 (noite) e volta a 0


def interpolar_cor(cor_a, cor_b, fator):
    # mistura duas cores conforme o "fator" (0 = cor_a pura, 1 = cor_b pura)
    return tuple(int(cor_a[i] + (cor_b[i] - cor_a[i]) * fator) for i in range(3))


def desenhar_ceu(tela, nuvens, estrelas, tempo_ms):
    fator_noite = calcular_fator_noite(tempo_ms)                 # 0 = dia, 1 = noite
    cor_ceu = interpolar_cor(DIA_CEU, NOITE_CEU, fator_noite)     # cor do céu no momento atual
    pygame.draw.rect(tela, cor_ceu, (0, 0, LARGURA, CEU_ALTURA))  # pinta a faixa do céu

    # as estrelas só aparecem (com transparência) quando está escurecendo/está noite
    if fator_noite > 0.05:
        superficie_estrelas = pygame.Surface((LARGURA, CEU_ALTURA), pygame.SRCALPHA)  # superfície com transparência
        for (ex, ey, raio) in estrelas:
            pygame.draw.circle(superficie_estrelas, (255, 255, 255, 255), (ex, ey), raio)
        superficie_estrelas.set_alpha(int(fator_noite * 255))  # quanto mais noite, mais visíveis
        tela.blit(superficie_estrelas, (0, 0))

    cor_nuvem = interpolar_cor(NUVEM_DIA, NUVEM_NOITE, fator_noite)  # nuvens escurecem à noite
    for nuvem in nuvens:
        desenhar_nuvem(tela, nuvem, cor_nuvem)

    return fator_noite


def desenhar_chao(tela):
    # pinta a área de gelo (do fim do céu até o fim da tela)
    pygame.draw.rect(tela, GELO_CLARO, (0, CEU_ALTURA, LARGURA, ALTURA - CEU_ALTURA))
    # linhas horizontais leves, só para dar textura de "placas de gelo"
    for y in range(CEU_ALTURA + 30, ALTURA, 40):
        pygame.draw.line(tela, GELO_SOMBRA, (0, y), (LARGURA, y), 2)


def desenhar_texto_contornado(tela, texto, fonte, x, y, cor_texto=BRANCO, cor_contorno=PRETO):
    # desenha um texto com contorno escuro, para continuar legível tanto de dia quanto de noite
    base = fonte.render(texto, True, cor_contorno)
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # desenha o contorno em 4 direções
        tela.blit(base, (x + dx, y + dy))
    principal = fonte.render(texto, True, cor_texto)
    tela.blit(principal, (x, y))  # por cima, desenha o texto na cor principal


# --------------------------------------------------------------
# 7. CLASSE DO PINGUIM (JOGADOR)
# --------------------------------------------------------------

class Pinguim:
    def __init__(self):
        self.largura = 50
        self.altura = 55
        self.x = LARGURA // 2 - self.largura // 2   # centralizado horizontalmente
        self.y = ALTURA - 90                          # fixo perto da base (andando no gelo)
        self.velocidade = 6
        self.controles_invertidos_ate = 0  # timestamp (ms) até quando os controles ficam invertidos

    def mover(self, teclas, tempo_ms):
        # verifica se ainda estamos dentro do período de inversão de controles
        invertido = tempo_ms < self.controles_invertidos_ate

        # se estiver invertido, troca qual tecla representa "esquerda" e "direita"
        tecla_esquerda = pygame.K_RIGHT if invertido else pygame.K_LEFT
        tecla_direita = pygame.K_LEFT if invertido else pygame.K_RIGHT

        if teclas[tecla_esquerda] and self.x > 0:
            self.x -= self.velocidade
        if teclas[tecla_direita] and self.x < LARGURA - self.largura:
            self.x += self.velocidade

        return invertido  # devolve se está invertido, para o HUD e o desenho usarem

    def ativar_inversao(self, tempo_ms):
        # define até quando (no relógio do jogo) os controles ficam invertidos
        self.controles_invertidos_ate = tempo_ms + DURACAO_INVERSAO_MS

    def desenhar(self, tela, invertido):
        cx = self.x + self.largura // 2  # centro horizontal do pinguim
        cor_corpo = VERMELHO if invertido else PRETO  # fica vermelho como aviso enquanto invertido

        pygame.draw.ellipse(tela, cor_corpo, (self.x, self.y, self.largura, self.altura))          # corpo (tuxedo)
        pygame.draw.ellipse(tela, BRANCO, (self.x + 9, self.y + 16, self.largura - 18, self.altura - 20))  # barriga
        pygame.draw.ellipse(tela, LARANJA, (self.x + 6, self.y + self.altura - 10, 16, 10))          # pé esquerdo
        pygame.draw.ellipse(tela, LARANJA, (self.x + self.largura - 22, self.y + self.altura - 10, 16, 10))  # pé direito
        pygame.draw.polygon(tela, LARANJA, [(cx - 6, self.y + 18), (cx + 6, self.y + 18), (cx, self.y + 28)])  # bico
        pygame.draw.circle(tela, BRANCO, (cx - 8, self.y + 14), 5)   # olho esquerdo (fundo branco)
        pygame.draw.circle(tela, BRANCO, (cx + 8, self.y + 14), 5)   # olho direito (fundo branco)
        pygame.draw.circle(tela, PRETO, (cx - 8, self.y + 14), 2)    # pupila esquerda
        pygame.draw.circle(tela, PRETO, (cx + 8, self.y + 14), 2)    # pupila direita

    def get_rect(self):
        # retorna a hitbox usada para checar colisão com os obstáculos
        return pygame.Rect(self.x, self.y, self.largura, self.altura)


# --------------------------------------------------------------
# 8. CLASSE DO OBSTÁCULO (BURACO OU BLOCO DE GELO)
# --------------------------------------------------------------

class Obstaculo:
    def __init__(self, velocidade_base):
        self.tipo = random.choice(["buraco", "bloco"])  # sorteia o tipo de obstáculo
        self.tamanho = random.randint(38, 52)             # tamanho aleatório
        self.definir_velocidade(velocidade_base)
        self.reposicionar()

    def definir_velocidade(self, velocidade_base):
        # blocos descem um pouco mais rápido que buracos, para variar a dificuldade
        self.velocidade = velocidade_base + (0 if self.tipo == "buraco" else 1)

    def reposicionar(self):
        self.x = random.randint(10, LARGURA - self.tamanho - 10)
        # requisito: obstáculos nascem por volta do meio vertical da tela, não do topo
        self.y = random.randint(ALTURA // 2 - 40, ALTURA // 2)

    def mover(self):
        self.y += self.velocidade  # desce continuamente em direção ao pinguim

    def desenhar(self, tela):
        if self.tipo == "buraco":
            altura_buraco = self.tamanho * 0.6  # buraco fica "achatado", como um furo no chão
            pygame.draw.ellipse(tela, BURACO_BORDA, (self.x - 4, self.y - 2, self.tamanho + 8, altura_buraco + 8))
            pygame.draw.ellipse(tela, BURACO_COR, (self.x, self.y, self.tamanho, altura_buraco))
        else:
            rect = pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)
            pygame.draw.rect(tela, BLOCO_COR, rect, border_radius=6)                 # corpo do bloco
            pygame.draw.rect(tela, BLOCO_BRILHO, rect, width=2, border_radius=6)     # contorno claro
            # linha diagonal simulando brilho/reflexo no gelo
            pygame.draw.line(tela, BLOCO_BRILHO, (self.x + 6, self.y + 6), (self.x + self.tamanho - 14, self.y + 14), 2)

    def get_rect(self):
        # hitbox: buraco usa altura reduzida (é achatado); bloco usa altura cheia
        altura_hitbox = self.tamanho * 0.6 if self.tipo == "buraco" else self.tamanho
        return pygame.Rect(self.x, self.y, self.tamanho, altura_hitbox)


# --------------------------------------------------------------
# 9. INTERFACE (HUD, GAME OVER, BOTÃO DE REINICIAR)
# --------------------------------------------------------------

def desenhar_hud(pontos, invertido):
    desenhar_texto_contornado(tela, f"Pontos: {pontos}", fonte_hud, 15, 15)
    if invertido:
        aviso = fonte_aviso.render("CONTROLES INVERTIDOS!", True, VERMELHO)
        rect = aviso.get_rect(center=(LARGURA // 2, 25))
        # fundo escuro atrás do aviso, para garantir contraste com o céu claro
        fundo = pygame.Surface((rect.width + 20, rect.height + 10))
        fundo.set_alpha(150)
        fundo.fill(PRETO)
        tela.blit(fundo, (rect.x - 10, rect.y - 5))
        tela.blit(aviso, rect)


def desenhar_botao_reiniciar():
    botao_rect = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 70, 200, 50)
    pygame.draw.rect(tela, VERDE, botao_rect, border_radius=8)
    pygame.draw.rect(tela, BRANCO, botao_rect, width=3, border_radius=8)
    texto = fonte_botao.render("REINICIAR", True, BRANCO)
    texto_rect = texto.get_rect(center=botao_rect.center)
    tela.blit(texto, texto_rect)
    return botao_rect


def tela_game_over(pontos_finais):
    tela.fill(PRETO)
    texto_go = fonte_titulo.render("GAME OVER", True, VERMELHO)
    rect_go = texto_go.get_rect(center=(LARGURA // 2, ALTURA // 2 - 70))
    tela.blit(texto_go, rect_go)

    texto_info = fonte_hud.render(f"O pinguim caiu no buraco! Pontuação: {pontos_finais}", True, BRANCO)
    rect_info = texto_info.get_rect(center=(LARGURA // 2, ALTURA // 2 - 10))
    tela.blit(texto_info, rect_info)

    botao_rect = desenhar_botao_reiniciar()
    pygame.display.flip()
    return botao_rect


# --------------------------------------------------------------
# 10. FUNÇÃO PRINCIPAL DO JOGO
# --------------------------------------------------------------

def rodar_jogo():
    pinguim = Pinguim()
    nuvens = gerar_nuvens()
    estrelas = gerar_estrelas()

    velocidade_base = 4          # velocidade inicial dos obstáculos
    numero_obstaculos = 3        # quantidade de obstáculos caindo ao mesmo tempo
    obstaculos = [Obstaculo(velocidade_base) for _ in range(numero_obstaculos)]

    pontos = 0
    rodando = True
    jogo_ativo = True  # True = jogando; False = tela de game over

    while rodando:
        relogio.tick(FPS)
        tempo_ms = pygame.time.get_ticks()  # relógio interno do pygame, em milissegundos

        # -------- 10.1 TRATAMENTO DE EVENTOS --------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and not jogo_ativo:
                if botao_reiniciar_rect.collidepoint(evento.pos):
                    return "reiniciar"

        if jogo_ativo:
            # -------- 10.2 MOVIMENTAÇÃO DO PINGUIM --------
            teclas = pygame.key.get_pressed()
            invertido = pinguim.mover(teclas, tempo_ms)

            # -------- 10.3 MOVIMENTAÇÃO E COLISÃO DOS OBSTÁCULOS --------
            for obstaculo in obstaculos:
                obstaculo.mover()

                if obstaculo.get_rect().colliderect(pinguim.get_rect()):
                    if obstaculo.tipo == "buraco":
                        # requisito: cair no buraco mata na hora
                        jogo_ativo = False
                        tempo_fim = tempo_ms
                    else:
                        # requisito: bater no bloco de gelo inverte os controles por 3 segundos
                        pinguim.ativar_inversao(tempo_ms)
                        obstaculo.reposicionar()

                elif obstaculo.y > ALTURA:
                    # obstáculo atravessou a tela sem atingir o pinguim: ganha ponto
                    pontos += 1
                    obstaculo.reposicionar()

                    # aumenta a velocidade base a cada 10 pontos (dificuldade progressiva)
                    if pontos % 10 == 0:
                        velocidade_base += 1
                        for o in obstaculos:
                            o.definir_velocidade(velocidade_base)

            # -------- 10.4 DESENHO DO CENÁRIO E DOS ELEMENTOS --------
            mover_nuvens(nuvens)
            desenhar_ceu(tela, nuvens, estrelas, tempo_ms)
            desenhar_chao(tela)
            for obstaculo in obstaculos:
                obstaculo.desenhar(tela)
            pinguim.desenhar(tela, invertido)
            desenhar_hud(pontos, invertido)
            pygame.display.flip()

        else:
            # -------- 10.5 TELA DE GAME OVER --------
            botao_reiniciar_rect = tela_game_over(pontos)

            # fecha o jogo automaticamente após alguns segundos, se ninguém clicar em reiniciar
            if tempo_ms - tempo_fim > 6000:
                rodando = False

    return "sair"


# --------------------------------------------------------------
# 11. PONTO DE ENTRADA DO PROGRAMA
# --------------------------------------------------------------

def main():
    resultado = rodar_jogo()
    while resultado == "reiniciar":
        resultado = rodar_jogo()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()