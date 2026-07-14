# ==============================================================
# JOGO: DESVIE DOS INIMIGOS
# Controle uma nave e desvie dos inimigos que caem do topo da tela
# ==============================================================

import pygame   # biblioteca principal para criar jogos 2D em Python
import random   # usada para gerar posições e escolhas aleatórias
import sys      # usada para encerrar o programa corretamente

# --------------------------------------------------------------
# 1. INICIALIZAÇÃO DO PYGAME E DA JANELA
# --------------------------------------------------------------

pygame.init()  # inicializa todos os módulos internos do pygame (vídeo, fontes, etc.)
pygame.mixer.init()  # inicializa o módulo de áudio separadamente (mais seguro)

LARGURA = 800   # largura da janela em pixels (requisito do jogo)
ALTURA = 600    # altura da janela em pixels (requisito do jogo)

# cria a janela do jogo com o tamanho definido acima
tela = pygame.display.set_mode((LARGURA, ALTURA))

# define o título que aparece na barra da janela
pygame.display.set_caption("Desvie dos Inimigos - Nave Espacial")

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
VERDE_CLARO = (0, 230, 90)
AMARELO  = (255, 220, 0)
CINZA    = (60, 60, 60)

# --------------------------------------------------------------
# 3. CONTROLE DE TEMPO (FPS) E FONTES DE TEXTO
# --------------------------------------------------------------

relogio = pygame.time.Clock()  # objeto usado para controlar a velocidade do jogo
FPS = 60                        # quantidade de quadros por segundo desejada

# fontes usadas para escrever textos na tela (tamanho em pixels)
fonte_hud     = pygame.font.SysFont("Arial", 26)   # fonte para vidas/pontuação
fonte_titulo  = pygame.font.SysFont("Arial", 60, bold=True)  # fonte para "GAME OVER"
fonte_botao   = pygame.font.SysFont("Arial", 24, bold=True)  # fonte do botão reiniciar

# --------------------------------------------------------------
# 4. MÚSICA DE FUNDO (Desafio extra ✅)
# --------------------------------------------------------------
# Coloque um arquivo chamado "musica_fundo.mp3" na mesma pasta deste
# script para que a música toque. Se o arquivo não existir, o jogo
# simplesmente continua sem som (não trava).

try:
    pygame.mixer.music.load("musica_fundo.mp3")  # carrega o arquivo de música
    pygame.mixer.music.set_volume(0.4)            # define volume de 0.0 a 1.0
    pygame.mixer.music.play(-1)                   # -1 = tocar em loop infinito
except pygame.error:
    print("Aviso: 'musica_fundo.mp3' não encontrado. O jogo seguirá sem música.")


# --------------------------------------------------------------
# 5. CLASSE DO JOGADOR (a nave)
# --------------------------------------------------------------

class Jogador:
    def __init__(self):
        self.largura = 50       # largura da nave em pixels
        self.altura = 40        # altura da nave em pixels
        # posiciona a nave centralizada horizontalmente, perto da base da tela
        self.x = LARGURA // 2 - self.largura // 2
        self.y = ALTURA - 80
        self.velocidade_normal = 7   # velocidade padrão (sem boost)
        self.velocidade_boost = 13   # velocidade quando o boost está ativo (SPACE pressionado)
        self.velocidade = self.velocidade_normal  # velocidade usada no momento
        self.vidas = 3                # requisito: começa com 3 vidas
        self.usando_boost = False     # guarda se o boost está ativo neste quadro (usado no desenho)

    def mover(self, teclas):
        # verifica se a barra de espaço está pressionada para ativar o boost
        self.usando_boost = teclas[pygame.K_SPACE]
        # escolhe a velocidade deste quadro: mais rápida se o boost estiver ativo
        self.velocidade = self.velocidade_boost if self.usando_boost else self.velocidade_normal

        # se a seta esquerda estiver pressionada e a nave não estiver na borda esquerda
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade  # move para a esquerda (mais rápido se boost ativo)
        # se a seta direita estiver pressionada e a nave não estiver na borda direita
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - self.largura:
            self.x += self.velocidade  # move para a direita (mais rápido se boost ativo)

    def desenhar(self, tela):
        # desenha a nave como um triângulo apontando para cima (visual simples e leve)
        ponta = (self.x + self.largura // 2, self.y)               # topo da nave
        base_esq = (self.x, self.y + self.altura)                  # canto inferior esquerdo
        base_dir = (self.x + self.largura, self.y + self.altura)   # canto inferior direito
        cor_nave = AMARELO if self.usando_boost else AZUL  # muda de cor quando o boost está ativo
        pygame.draw.polygon(tela, cor_nave, [ponta, base_esq, base_dir])
        # pequeno detalhe no centro da nave (cabine), só estética
        pygame.draw.circle(tela, BRANCO, (self.x + self.largura // 2, self.y + 25), 6)

        # se o boost estiver ativo, desenha um "rastro" de fogo atrás da nave (efeito visual)
        if self.usando_boost:
            chama1 = (self.x + self.largura // 2 - 8, self.y + self.altura)      # ponto esquerdo da chama
            chama2 = (self.x + self.largura // 2 + 8, self.y + self.altura)      # ponto direito da chama
            chama_ponta = (self.x + self.largura // 2, self.y + self.altura + 20)  # ponta da chama, mais embaixo
            pygame.draw.polygon(tela, LARANJA, [chama1, chama2, chama_ponta])

    def get_rect(self):
        # retorna o retângulo (hitbox) usado para checar colisão com os inimigos
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def resetar(self):
        # usada ao reiniciar o jogo: volta a nave para a posição inicial e 3 vidas
        self.x = LARGURA // 2 - self.largura // 2
        self.y = ALTURA - 80
        self.vidas = 3


# --------------------------------------------------------------
# 6. CLASSE DO INIMIGO
# --------------------------------------------------------------
# Desafio extra ✅: diferentes tipos de inimigo, cada um com
# tamanho, velocidade e cor próprios.

class Inimigo:
    def __init__(self, velocidade_base):
        # escolhe aleatoriamente um tipo de inimigo
        self.tipo = random.choice(["normal", "rapido", "grande"])
        self.definir_tipo(velocidade_base)  # define tamanho/velocidade/cor conforme o tipo
        self.reposicionar()                 # define a posição inicial (fora da tela, no topo)

    def definir_tipo(self, velocidade_base):
        if self.tipo == "normal":
            self.tamanho = 30                     # tamanho médio
            self.velocidade = velocidade_base      # velocidade padrão
            self.cor = VERMELHO                    # cor padrão (requisito: inimigos vermelhos)
        elif self.tipo == "rapido":
            self.tamanho = 20                      # menor
            self.velocidade = velocidade_base + 4  # mais rápido, porém menor (mais difícil de ver)
            self.cor = LARANJA                     # cor diferenciada para identificar o tipo
        elif self.tipo == "grande":
            self.tamanho = 45                      # maior
            self.velocidade = max(2, velocidade_base - 2)  # mais lento, porém ocupa mais espaço
            self.cor = VERMELHO_ESCURO             # tom mais escuro de vermelho

    def reposicionar(self):
        # sorteia uma posição X dentro dos limites da tela
        self.x = random.randint(0, LARGURA - self.tamanho)
        # sorteia uma posição Y negativa, para o inimigo "nascer" acima da tela
        self.y = random.randint(-200, -40)

    def mover(self):
        self.y += self.velocidade  # move o inimigo continuamente para baixo

    def desenhar(self, tela):
        # desenha o inimigo como um quadrado (formato simples e de fácil colisão)
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.tamanho, self.tamanho))

    def get_rect(self):
        # retorna o retângulo (hitbox) do inimigo, usado na checagem de colisão
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)


# --------------------------------------------------------------
# 7. FUNÇÕES AUXILIARES DE DESENHO (HUD, GAME OVER, BOTÃO)
# --------------------------------------------------------------

def desenhar_hud(pontos, vidas):
    # desenha o placar de pontos no canto superior esquerdo
    texto_pontos = fonte_hud.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (15, 15))
    # desenha o número de vidas no canto superior direito
    texto_vidas = fonte_hud.render(f"Vidas: {vidas}", True, VERMELHO)
    tela.blit(texto_vidas, (LARGURA - 150, 15))


def desenhar_botao_reiniciar():
    # define a área (retângulo) clicável do botão
    botao_rect = pygame.Rect(LARGURA // 2 - 100, ALTURA // 2 + 70, 200, 50)
    pygame.draw.rect(tela, VERDE, botao_rect, border_radius=8)         # fundo do botão
    pygame.draw.rect(tela, BRANCO, botao_rect, width=3, border_radius=8)  # borda do botão
    texto = fonte_botao.render("REINICIAR", True, BRANCO)
    texto_rect = texto.get_rect(center=botao_rect.center)  # centraliza o texto no botão
    tela.blit(texto, texto_rect)
    return botao_rect  # devolve o retângulo para podermos checar o clique do mouse


def tela_game_over(pontos_finais):
    # preenche a tela toda de preto antes de escrever a mensagem
    tela.fill(PRETO)
    # requisito: exibir a mensagem "GAME OVER"
    texto_go = fonte_titulo.render("GAME OVER", True, VERMELHO)
    rect_go = texto_go.get_rect(center=(LARGURA // 2, ALTURA // 2 - 60))
    tela.blit(texto_go, rect_go)
    # mostra também a pontuação final, como informação extra ao jogador
    texto_pontos = fonte_hud.render(f"Pontuação final: {pontos_finais}", True, BRANCO)
    rect_pontos = texto_pontos.get_rect(center=(LARGURA // 2, ALTURA // 2))
    tela.blit(texto_pontos, rect_pontos)
    # desenha o botão de reiniciar (desafio extra ✅) e devolve seu retângulo
    botao_rect = desenhar_botao_reiniciar()
    pygame.display.flip()  # atualiza a tela para mostrar tudo que foi desenhado
    return botao_rect


# --------------------------------------------------------------
# 8. FUNÇÃO PRINCIPAL DO JOGO
# --------------------------------------------------------------

def rodar_jogo():
    jogador = Jogador()  # cria a nave do jogador

    velocidade_base_inimigo = 3  # velocidade inicial dos inimigos (antes de multiplicar por tipo)
    PONTOS_MAXIMO_AUMENTO = 200   # a partir dessa pontuação, a velocidade para de aumentar
    numero_inimigos = 3          # quantidade de inimigos caindo ao mesmo tempo
    # cria a lista inicial de inimigos usando list comprehension
    inimigos = [Inimigo(velocidade_base_inimigo) for _ in range(numero_inimigos)]

    pontos = 0        # pontuação começa zerada
    rodando = True     # controla o loop principal do jogo
    jogo_ativo = True  # True = jogando; False = tela de game over

    # ---------------- LOOP PRINCIPAL DO JOGO ----------------
    while rodando:
        relogio.tick(FPS)  # limita o jogo a rodar no máximo FPS vezes por segundo

        # -------- 8.1 TRATAMENTO DE EVENTOS --------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # se o usuário clicar no "X" da janela
                rodando = False
            # captura clique do mouse, usado apenas na tela de game over (botão reiniciar)
            if evento.type == pygame.MOUSEBUTTONDOWN and not jogo_ativo:
                if botao_reiniciar_rect.collidepoint(evento.pos):
                    return "reiniciar"  # sinaliza para a função main() reiniciar o jogo

        if jogo_ativo:
            # -------- 8.2 MOVIMENTAÇÃO DO JOGADOR --------
            teclas = pygame.key.get_pressed()  # lê todas as teclas pressionadas no momento
            jogador.mover(teclas)              # move a nave conforme as setas

            # -------- 8.3 MOVIMENTAÇÃO E LÓGICA DOS INIMIGOS --------
            for inimigo in inimigos:
                inimigo.mover()  # desce o inimigo um pouco a cada quadro

                # checa colisão entre o inimigo e o jogador
                if inimigo.get_rect().colliderect(jogador.get_rect()):
                    jogador.vidas -= 1        # requisito: perde 1 vida ao ser atingido
                    inimigo.reposicionar()    # requisito: inimigo volta para o topo

                # checa se o inimigo passou da parte inferior da tela sem atingir o jogador
                elif inimigo.y > ALTURA:
                    pontos += 1               # requisito: +1 ponto por inimigo desviado
                    inimigo.reposicionar()    # o inimigo volta ao topo para continuar o jogo

                    # desafio extra ✅: aumenta a velocidade a cada 10 pontos,
                    # mas só até a pontuação máxima definida (PONTOS_MAXIMO_AUMENTO)
                    if pontos % 10 == 0 and pontos <= PONTOS_MAXIMO_AUMENTO:
                        velocidade_base_inimigo += 1
                        for i in inimigos:
                            i.definir_tipo(velocidade_base_inimigo)  # atualiza velocidade de todos

            # -------- 8.4 CHECAGEM DE GAME OVER --------
            if jogador.vidas <= 0:
                jogo_ativo = False              # muda para o estado de "fim de jogo"
                tempo_game_over = pygame.time.get_ticks()  # marca o momento em que o jogo acabou

            # -------- 8.5 DESENHO NA TELA (fase jogando) --------
            tela.fill(PRETO)                    # limpa a tela pintando o fundo de preto
            jogador.desenhar(tela)              # desenha a nave
            for inimigo in inimigos:
                inimigo.desenhar(tela)          # desenha cada inimigo
            desenhar_hud(pontos, jogador.vidas) # desenha pontuação e vidas na tela
            pygame.display.flip()               # atualiza a janela com tudo que foi desenhado

        else:
            # -------- 8.6 TELA DE GAME OVER --------
            botao_reiniciar_rect = tela_game_over(pontos)  # desenha a tela e pega o botão

            # requisito: fechar o jogo automaticamente após alguns segundos
            if pygame.time.get_ticks() - tempo_game_over > 6000:  # 6000 ms = 6 segundos
                rodando = False

    return "sair"  # sinaliza que o jogador não pediu reinício (fechou ou tempo esgotou)


# --------------------------------------------------------------
# 9. PONTO DE ENTRADA DO PROGRAMA
# --------------------------------------------------------------
# Permite reiniciar o jogo (desafio extra ✅) sem precisar rodar
# o script novamente, chamando rodar_jogo() em loop até o usuário
# realmente sair.

def main():
    resultado = rodar_jogo()   # roda o jogo pela primeira vez
    while resultado == "reiniciar":
        resultado = rodar_jogo()  # se o jogador clicou em reiniciar, roda de novo

    pygame.quit()  # encerra o pygame corretamente
    sys.exit()      # encerra o programa Python


if __name__ == "__main__":
    main()  # só executa o jogo se este arquivo for rodado diretamente