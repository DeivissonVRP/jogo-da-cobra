import pygame  # Importa a biblioteca do Pygame para criar o jogo
import random  # Importa a biblioteca para gerar posições aleatórias (comida)

# Inicialização do Pygame
pygame.init()  # Ativa todos os módulos internos do Pygame

# Configurações da janela
LARGURA = 1000  # Define a largura máxima da janela do jogo em pixels
ALTURA = 600  # Define a altura máxima da janela do jogo em pixels
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela do jogo com as dimensões acima
pygame.display.set_caption("Snake Game")  # Define o título que aparece na barra da janela

# Configuração dos tamanhos
TAMANHO = 25
  # Tamanho de cada quadrado do grid (tamanho da cobra e do rato)

# Carregamento e ajuste das imagens
fundo = pygame.image.load("imagens/jg.jpg")  # Carrega o arquivo da imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta o tamanho do fundo para caber na tela toda

rato = pygame.image.load("imagens/rato.png")  # Carrega o arquivo da imagem do rato
rato = pygame.transform.scale(rato, (TAMANHO, TAMANHO))  # Ajusta o tamanho do rato para o tamanho do bloco (25x25)

# CONFIGURAÇÃO DE ÁUDIO CORRIGIDA (Utilizando .ogg para eliminar chiados crônicos)
som_comer = pygame.mixer.Sound("sons/comer.wav")  # Carrega o efeito de mordida em formato wav estável

# Paleta de cores (no formato RGB: Vermelho, Verde, Azul)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

# Configuração de texto e tempo
fonte = pygame.font.SysFont("Arial", 25)  # Define a fonte e o tamanho do texto do jogo
clock = pygame.time.Clock()  # Cria um objeto para controlar a velocidade do jogo (FPS)

def desenhar_cobra(lista_cobra):
    # Passa por cada segmento guardado na lista do corpo da cobra
    for bloco in lista_cobra:
        # Desenha um retângulo verde na tela para cada parte do corpo
        pygame.draw.rect(TELA, VERDE, [bloco[0], bloco[1], TAMANHO, TAMANHO])

def mostrar_pontuacao(pontos): 
    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)  # Transforma o texto dos pontos em uma imagem
    TELA.blit(texto, [10, 10])  # Desenha a imagem do texto na posição superior esquerda da tela

def jogo():
    # Posicionamento inicial alinhado ao grid (divide pelo tamanho e multiplica de volta)
    x = (LARGURA // 2) // TAMANHO * TAMANHO
    y = (ALTURA // 2) // TAMANHO * TAMANHO

    # Variáveis de deslocamento (velocidade da direção atual)
    dx = 0
    dy = 0

    cobra = []  # Lista que vai guardar as posições X e Y de cada bloco do corpo
    comprimento = 1  # Tamanho inicial da cobra
    velocidade = 8    # Velocidade de quadros por segundo inicial
    velocidade_maxima = 25       # velocidade maxima
    # Sorteia uma posição inicial para o rato que esteja dentro dos limites do grid
    rato_x = random.randrange(0, LARGURA - TAMANHO, TAMANHO)
    rato_y = random.randrange(0, ALTURA - TAMANHO, TAMANHO)


    rodando = True  # Variável que mantém o loop principal funcionando
    game_over = False  # Variável que controla o estado de derrota

    while rodando:   
        # Tela de Game Over (Loop secundário ativado apenas ao morrer)
        while game_over:
            TELA.fill(PRETO)  # Pinta a tela inteira de preto

            msg = fonte.render("Game Over! Pressione C para continuar", True, BRANCO)
            TELA.blit(msg, [300, ALTURA // 2])  # Desenha o texto de Game Over no centro vertical
            mostrar_pontuacao(comprimento - 1)  # Exibe os pontos finais
            pygame.display.update()  # Atualiza a tela para exibir as mudanças

            # Captura de eventos específicos da tela de Game Over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Se fechar no "X" da janela, encerra o programa por completo
                if event.type == pygame.KEYDOWN:
                   
                    if event.key == pygame.K_c:
                        return True  # Se apertar "C", reinicia o jogo enviando um sinal positivo

        # Captura de eventos do jogo em andamento (Teclado, mouses, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Se fechar no "X" durante a partida, encerra o programa
         
            if event.type == pygame.KEYDOWN:
                # Controles de direção: Só muda o eixo se a cobra não estiver se movendo na direção oposta
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -TAMANHO
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = TAMANHO
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -TAMANHO
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = TAMANHO
                    dx = 0

        # Atualização da posição da cabeça somando o deslocamento
        x += dx
        y += dy

        # Verificação se a cabeça saiu dos limites da tela (colisão com a parede)
        if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
            game_over = True  # Ativa o estado de Game Over

        # Renderização do cenário (Desenha de trás para frente)
        TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na posição inicial (0,0)
        TELA.blit(rato, (rato_x, rato_y))  # Desenha a imagem do rato na sua respectiva coordenada

        # Atualização do corpo da cobra
        cabeca = [x, y]  # Cria uma lista com a coordenada atual da cabeça
        cobra.append(cabeca)  # Adiciona a cabeça na lista do corpo da cobra

        # Garante que o corpo não fique maior do que a pontuação/comprimento atual permite
        if len(cobra) > comprimento:
            del cobra[0]  # Remove o pedaço mais antigo da cauda para simular o movimento de andar

        # Verificação se a cabeça bateu em qualquer outra parte do próprio corpo
        for bloco in cobra[:-1]:
            if bloco == cabeca:
                game_over = True  # Ativa o estado de Game Over

        # Desenha a cobra e updates o placar por cima do fundo
        desenhar_cobra(cobra)
        mostrar_pontuacao(comprimento - 1)

        pygame.display.update()  # Mostra na janela tudo o que foi desenho neste frame

        # Mecânica de comer o rato
        if x == rato_x and y == rato_y:
            som_comer.play()  # Ativa a reprodução instantânea do efeito sonoro de mordida
            # Sorteia uma nova posição para o próximo rato aparecer
            rato_x = random.randrange(0, LARGURA - TAMANHO, TAMANHO)
            rato_y = random.randrange(0, ALTURA - TAMANHO, TAMANHO)
            comprimento += 1  # Aumenta o tamanho do corpo da cobra
            velocidade = min(velocidade + 1, velocidade_maxima)  # Aumenta o FPS atual para o jogo acelerar e ficar mais difícil

        # Trava a taxa de atualização do jogo de acordo com o valor da velocidade
        clock.tick(velocidade) 

# Loop externo principal que gerencia o reinício limpo sem estourar a memória RAM
continuar_jogando = True
while continuar_jogando:
    continuar_jogando = jogo()  # A variável recebe o True ou False retornado pela função 'jogo'

pygame.quit()  # Fecha os módulos do Pygame com segurança e desliga a janela
