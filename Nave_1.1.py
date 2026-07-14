# ==============================================================
# Controle uma nave, desvie dos inimigos e avance pelas 10 fases!
# ==============================================================

import pygame   # biblioteca principal para criar jogos 2D em Python
import random   # usada para gerar posições e escolhas aleatórias
import math     # usada para calcular os pontos de formas geométricas (estrela, hexágono, etc.)
import sys      # usada para encerrar o programa corretamente

# --------------------------------------------------------------
# 1. INICIALIZAÇÃO DO PYGAME E DA JANELA
# --------------------------------------------------------------

pygame.init()          # inicializa todos os módulos internos do pygame
pygame.mixer.init()    # inicializa o módulo de áudio separadamente

LARGURA = 800   # largura da janela em pixels (requisito do jogo)
ALTURA = 600    # altura da janela em pixels (requisito do jogo)






tela = pygame.display.set_mode((LARGURA, ALTURA))          # cria a janela do jogo
pygame.display.set_caption("Desvie dos Inimigos - Nave Espacial")  # título da janela

# --------------------------------------------------------------
# 2. CORES (formato RGB) usadas para desenhar os elementos
# --------------------------------------------------------------

BRANCO   = (255, 255, 255)
PRETO    = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERMELHO_ESCURO = (150, 0, 0)
LARANJA  = (255, 140, 0)
AZUL     = (0, 150, 255)
VERDE    = (0, 180, 0)
VERDE_CLARO = (60, 220, 100)
AMARELO  = (255, 220, 0)
CINZA    = (100, 100, 100)
ROSA     = (255, 105, 180)
CIANO    = (0, 220, 220)
ROXO     = (180, 80, 255)
PRATA    = (220, 220, 230)

# --------------------------------------------------------------
# 3. CONTROLE DE TEMPO (FPS) E FONTES DE TEXTO
# --------------------------------------------------------------

relogio = pygame.time.Clock()  # objeto usado para controlar a velocidade do jogo
FPS = 60                        # quadros por segundo desejados

fonte_hud    = pygame.font.SysFont("Arial", 24)               # fonte para vidas/pontos/fase
fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)    # fonte para "GAME OVER" / "VITÓRIA"
fonte_botao  = pygame.font.SysFont("Arial", 24, bold=True)    # fonte do botão reiniciar
fonte_banner = pygame.font.SysFont("Arial", 46, bold=True)    # fonte do aviso "FASE X!"

# --------------------------------------------------------------
# 4. MÚSICA DE FUNDO (desafio extra ✅)
# --------------------------------------------------------------
# Coloque "musica_fundo.mp3" na mesma pasta deste script para tocar.
# Se não existir, o jogo simplesmente continua sem som.

try:
    pygame.mixer.music.load("sons/musica_fundo.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # -1 = loop infinito
except pygame.error:
    print("Aviso: 'musica_fundo.mp3' não encontrado. O jogo seguirá sem música.")

#--------------------------------------------------------------------
#IMAGEM DE ABERTURA
#-------------------------------------------------------
abertura = pygame.image.load("imagens/abertura.png")
abertura = pygame.transform.scale(abertura, (LARGURA, ALTURA))

# --------------------------------------------------------------
# IMAGENS DA Vitoria
# --------------------------------------------------------------
vitoria = pygame.image.load("imagens/vitoria.png")
vitoria = pygame.transform.scale(vitoria, (LARGURA,ALTURA))



# --------------------------------------------------------------
# IMAGENS DAS FASES
# --------------------------------------------------------------

fundos = []

for i in range(1, 11):
    img = pygame.image.load(f"imagens/nvf_{i}.jpg").convert()
    img = pygame.transform.scale(img, (LARGURA, ALTURA))
    fundos.append(img)
# --------------------------------------------------------------
# 5. CONFIGURAÇÃO DAS FASES E DOS FORMATOS DE INIMIGOS
# --------------------------------------------------------------
# Cada formato só começa a aparecer a partir de uma certa fase.
# Assim, quanto mais fases o jogador avança, mais tipos de inimigo
# diferentes caem na tela ao mesmo tempo (diversidade progressiva).

PONTOS_POR_FASE = 10   # quantos pontos são necessários para passar de fase
FASE_MAXIMA = 10       # última fase do jogo
PONTOS_VITORIA = PONTOS_POR_FASE * FASE_MAXIMA  # 20 x 10 = 200 pontos para vencer o jogo
AUMENTO_VELOCIDADE_POR_FASE = 2  # quanto a velocidade base dos inimigos sobe a cada nova fase

# lista de formatos disponíveis: nome, cor, fase mínima em que aparece,
# tamanho da hitbox (quadrada) e um "extra" de velocidade próprio do formato
FORMATOS = [
    {"nome": "quadrado",  "cor": VERMELHO,        "fase_minima": 1,  "tamanho": 32, "vel_extra": 0},
    {"nome": "circulo",   "cor": LARANJA,         "fase_minima": 2,  "tamanho": 30, "vel_extra": 1},
    {"nome": "triangulo", "cor": AMARELO,         "fase_minima": 3,  "tamanho": 34, "vel_extra": 1},
    {"nome": "losango",   "cor": VERDE_CLARO,     "fase_minima": 4,  "tamanho": 30, "vel_extra": 2},
    {"nome": "estrela",   "cor": ROSA,            "fase_minima": 5,  "tamanho": 36, "vel_extra": 1},
    {"nome": "hexagono",  "cor": CIANO,           "fase_minima": 6,  "tamanho": 34, "vel_extra": 2},
    {"nome": "cruz",      "cor": ROXO,            "fase_minima": 7,  "tamanho": 32, "vel_extra": 2},
    {"nome": "seta",      "cor": PRATA,           "fase_minima": 8,  "tamanho": 28, "vel_extra": 3},
    {"nome": "anel",      "cor": (255, 60, 60),   "fase_minima": 9,  "tamanho": 38, "vel_extra": 2},
    {"nome": "boss",      "cor": VERMELHO_ESCURO, "fase_minima": 10, "tamanho": 50, "vel_extra": 1},
]

def tela_abertura_jogo():
    """Mostra a imagem de abertura e espera o jogador apertar ENTER,
    ESPAÇO ou clicar com o mouse para começar o jogo."""
    esperando = True
    while esperando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                esperando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

        tela.blit(abertura, (0, 0))

        # texto piscando "Pressione ENTER ou clique para começar"
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            texto = fonte_botao.render("Pressione ENTER, ESPAÇO ou clique para começar", True, BRANCO)
            rect_texto = texto.get_rect(center=(LARGURA // 2, ALTURA - 60))
            tela.blit(texto, rect_texto)

        pygame.display.flip()

def formatos_desbloqueados(fase_atual):
    # retorna apenas os formatos cuja fase mínima já foi alcançada
    return [f for f in FORMATOS if f["fase_minima"] <= fase_atual]


# --------------------------------------------------------------
# 6. FUNÇÕES AUXILIARES PARA DESENHAR FORMAS GEOMÉTRICAS
# --------------------------------------------------------------
# Calculam os pontos (vértices) de polígonos regulares e estrelas,
# usados para desenhar hexágono, hexágono do "boss", estrela, etc.

def pontos_poligono_regular(cx, cy, raio, lados, rotacao=-math.pi / 2):
    # cx, cy = centro da forma / raio = distância do centro até a ponta
    # lados = quantidade de lados do polígono (6 = hexágono, 8 = octógono)
    pontos = []
    for i in range(lados):
        # calcula o ângulo de cada vértice, distribuído igualmente em um círculo
        angulo = rotacao + (2 * math.pi * i) / lados
        x = cx + raio * math.cos(angulo)
        y = cy + raio * math.sin(angulo)
        pontos.append((x, y))
    return pontos


def pontos_estrela(cx, cy, raio_externo, raio_interno, pontas=5):
    # gera os vértices de uma estrela alternando entre raio externo (pontas)
    # e raio interno (vales), formando o efeito de estrela
    pontos = []
    for i in range(pontas * 2):
        raio = raio_externo if i % 2 == 0 else raio_interno
        angulo = (math.pi * i / pontas) - math.pi / 2
        x = cx + raio * math.cos(angulo)
        y = cy + raio * math.sin(angulo)
        pontos.append((x, y))
    return pontos


# --------------------------------------------------------------
# 7. CLASSE DO JOGADOR (a nave)
# --------------------------------------------------------------

class Jogador:
    def __init__(self):
        self.largura = 50
        self.altura = 40
        self.x = LARGURA // 2 - self.largura // 2   # centralizado horizontalmente
        self.y = ALTURA - 80                          # perto da base da tela
        self.velocidade_normal = 7   # velocidade padrão (sem boost)
        self.velocidade_boost = 13   # velocidade quando o boost (SPACE) está ativo
        self.velocidade = self.velocidade_normal
        self.vidas = 3                # requisito: começa com 3 vidas
        self.usando_boost = False     # guarda se o boost está ativo neste quadro

    def mover(self, teclas):
        # verifica se a barra de espaço está pressionada para ativar o boost
        self.usando_boost = teclas[pygame.K_SPACE]
        self.velocidade = self.velocidade_boost if self.usando_boost else self.velocidade_normal

        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade  # move para a esquerda
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - self.largura:
            self.x += self.velocidade  # move para a direita

    def desenhar(self, tela):
        # desenha a nave como um triângulo apontando para cima
        ponta = (self.x + self.largura // 2, self.y)
        base_esq = (self.x, self.y + self.altura)
        base_dir = (self.x + self.largura, self.y + self.altura)
        cor_nave = AMARELO if self.usando_boost else AZUL  # muda de cor com o boost ativo
        pygame.draw.polygon(tela, cor_nave, [ponta, base_esq, base_dir])
        pygame.draw.circle(tela, BRANCO, (self.x + self.largura // 2, self.y + 25), 6)  # cabine

        # rastro de chama quando o boost está ativo (efeito visual)
        if self.usando_boost:
            chama1 = (self.x + self.largura // 2 - 8, self.y + self.altura)
            chama2 = (self.x + self.largura // 2 + 8, self.y + self.altura)
            chama_ponta = (self.x + self.largura // 2, self.y + self.altura + 20)
            pygame.draw.polygon(tela, LARANJA, [chama1, chama2, chama_ponta])

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def resetar(self):
        self.x = LARGURA // 2 - self.largura // 2
        self.y = ALTURA - 80
        self.vidas = 3


# --------------------------------------------------------------
# 8. CLASSE DO INIMIGO
# --------------------------------------------------------------
# Cada inimigo tem um "formato" sorteado entre os já desbloqueados
# na fase atual, o que faz o jogo ficar mais variado conforme avança.

class Inimigo:
    def __init__(self, fase_atual, velocidade_base):
        self.trocar_formato(fase_atual, velocidade_base)  # sorteia o formato inicial
        self.reposicionar()                                # define a posição inicial no topo

    def trocar_formato(self, fase_atual, velocidade_base):
        # sorteia um novo formato entre os desbloqueados na fase atual
        self.formato = random.choice(formatos_desbloqueados(fase_atual))
        self.tamanho = self.formato["tamanho"]     # tamanho da hitbox (quadrada) do inimigo
        self.cor = self.formato["cor"]              # cor característica do formato
        # velocidade final = velocidade base da fase + o "extra" próprio do formato
        self.velocidade = velocidade_base + self.formato["vel_extra"]

    def reposicionar(self):
        self.x = random.randint(0, LARGURA - self.tamanho)   # posição X aleatória
        self.y = random.randint(-200, -40)                    # nasce acima da tela

    def mover(self):
        self.y += self.velocidade  # desce continuamente

    def desenhar(self, tela):
        # centro e raio aproximado usados pela maioria das formas
        cx = self.x + self.tamanho / 2
        cy = self.y + self.tamanho / 2
        raio = self.tamanho / 2
        nome = self.formato["nome"]

        if nome == "quadrado":
            pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho, self.tamanho))

        elif nome == "circulo":
            pygame.draw.circle(tela, self.cor, (int(cx), int(cy)), int(raio))

        elif nome == "triangulo":
            # triângulo "de cabeça para baixo", como se estivesse caindo
            p1 = (self.x, self.y)
            p2 = (self.x + self.tamanho, self.y)
            p3 = (cx, self.y + self.tamanho)
            pygame.draw.polygon(tela, self.cor, [p1, p2, p3])

        elif nome == "losango":
            # losango = 4 pontos: topo, direita, base, esquerda
            pontos = [(cx, self.y), (self.x + self.tamanho, cy), (cx, self.y + self.tamanho), (self.x, cy)]
            pygame.draw.polygon(tela, self.cor, pontos)

        elif nome == "estrela":
            pontos = pontos_estrela(cx, cy, raio, raio * 0.45, pontas=5)
            pygame.draw.polygon(tela, self.cor, pontos)

        elif nome == "hexagono":
            pontos = pontos_poligono_regular(cx, cy, raio, lados=6)
            pygame.draw.polygon(tela, self.cor, pontos)

        elif nome == "cruz":
            # desenha uma cruz usando dois retângulos sobrepostos (horizontal e vertical)
            espessura = self.tamanho * 0.35
            barra_h = pygame.Rect(self.x, cy - espessura / 2, self.tamanho, espessura)
            barra_v = pygame.Rect(cx - espessura / 2, self.y, espessura, self.tamanho)
            pygame.draw.rect(tela, self.cor, barra_h)
            pygame.draw.rect(tela, self.cor, barra_v)

        elif nome == "seta":
            # seta apontando para baixo: um triângulo (ponta) + um retângulo (haste)
            largura_haste = self.tamanho * 0.35
            haste = pygame.Rect(cx - largura_haste / 2, self.y, largura_haste, self.tamanho * 0.5)
            pygame.draw.rect(tela, self.cor, haste)
            ponta = [
                (self.x, self.y + self.tamanho * 0.5),
                (self.x + self.tamanho, self.y + self.tamanho * 0.5),
                (cx, self.y + self.tamanho),
            ]
            pygame.draw.polygon(tela, self.cor, ponta)

        elif nome == "anel":
            # anel = círculo "vazado" (desenhado apenas com contorno grosso)
            pygame.draw.circle(tela, self.cor, (int(cx), int(cy)), int(raio), width=6)

        elif nome == "boss":
            # inimigo especial da fase 10: octógono grande com um núcleo menor dentro
            pontos = pontos_poligono_regular(cx, cy, raio, lados=8)
            pygame.draw.polygon(tela, self.cor, pontos)
            pygame.draw.circle(tela, AMARELO, (int(cx), int(cy)), int(raio * 0.35))  # núcleo

    def get_rect(self):
        # hitbox sempre quadrada, independente do formato desenhado (simplifica a colisão)
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)


# --------------------------------------------------------------
# 9. FUNÇÕES DE INTERFACE (HUD, BARRA DE FASE, GAME OVER, VITÓRIA)
# --------------------------------------------------------------

def desenhar_hud(pontos, vidas, fase):
    # placar de pontos (canto superior esquerdo)
    texto_pontos = fonte_hud.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (15, 15))

    # vidas (canto superior direito)
    texto_vidas = fonte_hud.render(f"Vidas: {vidas}", True, VERMELHO)
    tela.blit(texto_vidas, (LARGURA - 150, 15))

    # rótulo da fase atual (centralizado, acima da barra de progresso)
    texto_fase = fonte_hud.render(f"Fase {fase}/{FASE_MAXIMA}", True, AMARELO)
    rect_fase = texto_fase.get_rect(center=(LARGURA // 2, 20))
    tela.blit(texto_fase, rect_fase)


def desenhar_barra_progresso(pontos, fase):
    # dimensões e posição da barra de progresso (desafio extra ✅: barra até 200 pontos)
    largura_barra = 300
    altura_barra = 16
    x_barra = LARGURA // 2 - largura_barra // 2
    y_barra = 40

    # progresso dentro da fase atual (0.0 a 1.0)
    if fase >= FASE_MAXIMA:
        progresso = 1.0 if pontos >= PONTOS_VITORIA else (pontos % PONTOS_POR_FASE) / PONTOS_POR_FASE
    else:
        progresso = (pontos % PONTOS_POR_FASE) / PONTOS_POR_FASE

    pygame.draw.rect(tela, CINZA, (x_barra, y_barra, largura_barra, altura_barra), border_radius=6)  # fundo
    pygame.draw.rect(tela, VERDE_CLARO, (x_barra, y_barra, int(largura_barra * progresso), altura_barra), border_radius=6)  # preenchido
    pygame.draw.rect(tela, BRANCO, (x_barra, y_barra, largura_barra, altura_barra), width=2, border_radius=6)  # borda


def desenhar_banner_fase(fase, tempo_inicio):
    # mostra "FASE X!" grande no centro da tela por um curto período (não bloqueia o jogo)
    if tempo_inicio is None:
        return
    tempo_passado = pygame.time.get_ticks() - tempo_inicio
    if tempo_passado < 1500:  # exibe por 1.5 segundos
        texto = fonte_banner.render(f"FASE {fase}!", True, AMARELO)
        rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 120))
        # desenha um fundo escuro semi-visível atrás do texto para facilitar a leitura
        fundo = pygame.Surface((rect.width + 40, rect.height + 20))
        fundo.set_alpha(160)
        fundo.fill(PRETO)
        tela.blit(fundo, (rect.x - 20, rect.y - 10))
        tela.blit(texto, rect)


def desenhar_botao_reiniciar():
    botao_rect = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 70, 200, 50)
    pygame.draw.rect(tela, VERDE, botao_rect, border_radius=8)
    pygame.draw.rect(tela, BRANCO, botao_rect, width=3, border_radius=8)
    texto = fonte_botao.render("REINICIAR", True, BRANCO)
    texto_rect = texto.get_rect(center=botao_rect.center)
    tela.blit(texto, texto_rect)
    return botao_rect


def tela_game_over(pontos_finais, fase_final):
    tela.fill(PRETO)
    texto_go = fonte_titulo.render("GAME OVER", True, VERMELHO)
    rect_go = texto_go.get_rect(center=(LARGURA // 2, ALTURA // 2 - 70))
    tela.blit(texto_go, rect_go)

    texto_info = fonte_hud.render(f"Pontuação: {pontos_finais}   |   Fase alcançada: {fase_final}", True, BRANCO)
    rect_info = texto_info.get_rect(center=(LARGURA // 2, ALTURA // 2 - 10))
    tela.blit(texto_info, rect_info)

    botao_rect = desenhar_botao_reiniciar()
    pygame.display.flip()
    return botao_rect


def tela_vitoria(pontos_finais):
    tela.blit(vitoria, (0, 0))
    texto_v = fonte_titulo.render("VOCÊ VENCEU!", True, VERDE_CLARO)
    rect_v = texto_v.get_rect(center=(LARGURA // 2, ALTURA // 2 - 70))
    tela.blit(texto_v, rect_v)

    texto_info = fonte_hud.render(f"Todas as {FASE_MAXIMA} fases completas! Pontuação final: {pontos_finais}", True, BRANCO)
    rect_info = texto_info.get_rect(center=(LARGURA // 2, ALTURA // 2 - 10))
    tela.blit(texto_info, rect_info)

    botao_rect = desenhar_botao_reiniciar()
    pygame.display.flip()
    return botao_rect


# --------------------------------------------------------------
# 10. FUNÇÃO PRINCIPAL DO JOGO
# --------------------------------------------------------------

def rodar_jogo():
    jogador = Jogador()

    fase = 1                         # fase inicial
    velocidade_base_inimigo = 3      # velocidade base dos inimigos (cresce a cada fase)
    numero_inimigos = 4             # quantidade de inimigos caindo ao mesmo tempo
    inimigos = [Inimigo(fase, velocidade_base_inimigo) for _ in range(numero_inimigos)]

    pontos = 0
    tempo_banner_fase = pygame.time.get_ticks()  # mostra "FASE 1!" logo no início também

    rodando = True
    jogo_ativo = True     # True = jogando; False = tela final (game over ou vitória)
    vitoria = False        # diferencia se o fim de jogo foi por vitória ou derrota

    while rodando:
        relogio.tick(FPS)

        # -------- 10.1 TRATAMENTO DE EVENTOS --------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and not jogo_ativo:
                if botao_reiniciar_rect.collidepoint(evento.pos):
                    return "reiniciar"

        if jogo_ativo:
            # -------- 10.2 MOVIMENTAÇÃO DO JOGADOR --------
            teclas = pygame.key.get_pressed()
            jogador.mover(teclas)

            # -------- 10.3 MOVIMENTAÇÃO E LÓGICA DOS INIMIGOS --------
            for inimigo in inimigos:
                inimigo.mover()

                if inimigo.get_rect().colliderect(jogador.get_rect()):
                    jogador.vidas -= 1                                  # perde 1 vida
                    inimigo.trocar_formato(fase, velocidade_base_inimigo)  # sorteia novo formato
                    inimigo.reposicionar()                              # volta ao topo

                elif inimigo.y > ALTURA:
                    pontos += 1  # +1 ponto por inimigo desviado
                    inimigo.trocar_formato(fase, velocidade_base_inimigo)
                    inimigo.reposicionar()

                    # -------- 10.4 CONTROLE DE FASES (barra até 200 pontos) --------
                    nova_fase = min(pontos // PONTOS_POR_FASE + 1, FASE_MAXIMA)
                    if nova_fase > fase:
                        fase = nova_fase
                        velocidade_base_inimigo += AUMENTO_VELOCIDADE_POR_FASE  # cada fase deixa os inimigos mais rápidos
                        tempo_banner_fase = pygame.time.get_ticks()  # dispara o aviso "FASE X!"
                        # atualiza a velocidade de todos os inimigos já em tela
                        for i in inimigos:
                            i.velocidade = velocidade_base_inimigo + i.formato["vel_extra"]

            # -------- 10.5 CHECAGEM DE VITÓRIA E GAME OVER --------
            if pontos >= PONTOS_VITORIA:
                jogo_ativo = False
                vitoria = True
                tempo_fim = pygame.time.get_ticks()
            elif jogador.vidas <= 0:
                jogo_ativo = False
                vitoria = False
                tempo_fim = pygame.time.get_ticks()

            # -------- 10.6 DESENHO NA TELA (fase jogando) --------
            tela.blit(fundos[fase-1], (0,0))
            jogador.desenhar(tela)
            for inimigo in inimigos:
                inimigo.desenhar(tela)
            desenhar_hud(pontos, jogador.vidas, fase)
            desenhar_barra_progresso(pontos, fase)
            desenhar_banner_fase(fase, tempo_banner_fase)
            pygame.display.flip()

        else:
            # -------- 10.7 TELA FINAL (game over ou vitória) --------
            if vitoria:
                botao_reiniciar_rect = tela_vitoria(pontos)
            else:
                botao_reiniciar_rect = tela_game_over(pontos, fase)

            # fecha o jogo automaticamente após alguns segundos, se ninguém clicar em reiniciar
            if pygame.time.get_ticks() - tempo_fim > 6000:
                rodando = False

    return "sair"


# --------------------------------------------------------------
# 11. PONTO DE ENTRADA DO PROGRAMA
# --------------------------------------------------------------

def main():
    tela_abertura_jogo()   # <-- mostra a tela de abertura antes de começar

    resultado = rodar_jogo()
    while resultado == "reiniciar":
        resultado = rodar_jogo()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()