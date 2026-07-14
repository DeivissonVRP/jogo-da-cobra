import pygame
import random

# 1. Inicialização do Pygame
pygame.init()

# 2. Configurações da Janela e Cores
LARGURA, ALTURA = 1300, 500
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo: Pedra, Papel ou Tesoura")

BRANCO    = (255, 255, 255)
PRETO     = (0, 0, 0)
CINZA     = (220, 220, 220)
HOVER     = (173, 216, 230) # Cor azul clara quando o mouse passa por cima
VERDE     = (50, 200, 50)
AZUL      = (50, 50, 200)
VERMELHO  = (200, 50, 50)

# 3. Fontes para o Texto
fonte_titulo = pygame.font.SysFont("Arial", 32, bold=True)
fonte_texto = pygame.font.SysFont("Arial", 22)

# 4. Estado Inicial do Jogo
opcoes = {1: "PEDRA", 2: "PAPEL", 3: "TESOURA"}
escolha_jogador = ""
escolha_computador = ""
resultado = "Clique em uma opção abaixo para jogar!"
cor_resultado = PRETO

# Variáveis do Placar
vitorias_jogador = 0
vitorias_computador = 0
empates = 0

# Definição dos Botões (Posição X, Posição Y, Largura, Altura)
botao_pedra = pygame.Rect(430, 350, 130, 50)
botao_papel = pygame.Rect(580, 350, 130, 50)
botao_tesoura = pygame.Rect(730, 350, 130, 50)
 
# 5. Função de Lógica do Vencedor
def verificar_vencedor(jogada, comp):
    if jogada == comp:
        return "RESULTADO: DEU EMPATE!", AZUL, "empate"
    elif (jogada == 1 and comp == 3) or (jogada == 2 and comp == 1) or (jogada == 3 and comp == 2):
        return "RESULTADO: PARABÉNS, VOCÊ VENCEU!!!", VERDE, "jogador"
    else:
        return "RESULTADO: O COMPUTADOR VENCEU!", VERMELHO, "computador"

# 6. Loop Principal do Jogo
rodando = True
while rodando:
    tela.fill(BRANCO)  # Limpa a tela com fundo branco
    pos_mouse = pygame.mouse.get_pos() # Pega a posição X e Y do mouse a cada instante

    # Captura de Eventos (Cliques do mouse e fechar janela)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Detecta o clique do botão esquerdo do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            jogada_feita = 0

            # Verifica qual botão foi clicado com o mouse
            if botao_pedra.collidepoint(pos_mouse):
                jogada_feita = 1
            elif botao_papel.collidepoint(pos_mouse):
                jogada_feita = 2
            elif botao_tesoura.collidepoint(pos_mouse):
                jogada_feita = 3

            # Verifica se uma jogada válida foi clicada
            if jogada_feita in [1, 2, 3]:
                comp_sorteado = random.randint(1, 3)

                escolha_jogador = f"Você escolheu: {opcoes[jogada_feita]}"
                escolha_computador = f"O computador escolheu: {opcoes[comp_sorteado]}"
                
                # Recebe o resultado da rodada atual
                resultado, cor_resultado, ganhador = verificar_vencedor(jogada_feita, comp_sorteado)
                
                # Somando a pontuação
                if ganhador == "jogador":
                    vitorias_jogador += 1
                elif ganhador == "computador":
                    vitorias_computador += 1
                else:
                 empates += 1

                # --- LÓGICA DE LIMITAR ATÉ 3 E ZERAR ---
                if vitorias_jogador == 3:
                    resultado = "FIM DE JOGO: VOCÊ ATINGIU 3 PONTOS E GANHOU O TORNEIO!"
                    cor_resultado = VERDE
                    # Zera o placar para a próxima partida
                    vitorias_jogador = 0
                    vitorias_computador = 0
                    empates = 0

                elif vitorias_computador == 3:
                    resultado = "FIM DE JOGO: O COMPUTADOR ATINGIU 3 PONTOS E GANHOU!"
                    cor_resultado = VERMELHO
                    # Zera o placar para a próxima partida
                    vitorias_jogador = 0
                    vitorias_computador = 0
                    empates = 0

    # 7. Desenhar Elementos na Tela
    txt_titulo = fonte_titulo.render("PEDRA, PAPEL OU TESOURA", True, PRETO)
    tela.blit(txt_titulo, (LARGURA // 2 - txt_titulo.get_width() // 2, 30))

    # Desenhar o placar na tela
    txt_placar = fonte_texto.render(f"Placar: Você {vitorias_jogador} x {vitorias_computador} PC (Empates: {empates})", True, PRETO)
    tela.blit(txt_placar, (LARGURA - txt_placar.get_width() - 100, 100))

    # Mostra as escolhas e o resultado na tela
    txt_jog = fonte_texto.render(escolha_jogador, True, PRETO)
    txt_comp = fonte_texto.render(escolha_computador, True, PRETO)
    txt_res = fonte_titulo.render(resultado, True, cor_resultado)

    tela.blit(txt_jog, (50, 130))
    tela.blit(txt_comp, (50, 180))
    
    # Centraliza o texto de resultado dinamicamente (importante para frases longas de fim de jogo)
    tela.blit(txt_res, (LARGURA // 2 - txt_res.get_width() // 2, 260))

    # Efeito Visual: Mudar a cor do botão se o mouse estiver em cima (Hover)
    cor_pedra = HOVER if botao_pedra.collidepoint(pos_mouse) else CINZA
    cor_papel = HOVER if botao_papel.collidepoint(pos_mouse) else CINZA
    cor_tesoura = HOVER if botao_tesoura.collidepoint(pos_mouse) else CINZA

    # Desenha os retângulos dos Botões
    pygame.draw.rect(tela, cor_pedra, botao_pedra, border_radius=100)
    pygame.draw.rect(tela, cor_papel, botao_papel, border_radius=100)
    pygame.draw.rect(tela, cor_tesoura, botao_tesoura, border_radius=100)

    # Textos centrais dentro dos Botões
    lbl_pedra = fonte_texto.render("PEDRA", True, PRETO)
    lbl_papel = fonte_texto.render("PAPEL", True, PRETO)
    lbl_tesoura = fonte_texto.render("TESOURA", True, PRETO)

    tela.blit(lbl_pedra, (botao_pedra.x + 25, botao_pedra.y + 12))
    tela.blit(lbl_papel, (botao_papel.x + 35, botao_papel.y + 12))
    tela.blit(lbl_tesoura, (botao_tesoura.x + 10, botao_tesoura.y + 12))

    # Atualiza a tela gráfica
    pygame.display.flip()

pygame.quit()