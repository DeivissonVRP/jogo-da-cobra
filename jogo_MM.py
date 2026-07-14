import pygame  # Importa a biblioteca do Pygame para criar o jogo
import random  # Importa a biblioteca para gerar posições aleatórias (comida)

# Inicialização do Pygame
pygame.init()  # Ativa todos os módulos internos do Pygame
pygame.mixer.init()

# Configurações da janela
LARGURA = 1000  # Define a largura máxima da janela do jogo em pixels
ALTURA = 600  # Define a altura máxima da janela do jogo em pixels
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # Cria a janela do jogo com as dimensions acima
pygame.display.set_caption("Snake Game")  # Define o título que aparece na barra da janela

# Configuração dos tamanhos
TAMANHO = 25
TAMANHO_G =25
  # Tamanho de cada quadrado do grid (tamanho da cobra e do rato)

# Carregamento e ajuste das imagens
fundo = pygame.image.load("imagens/jg.jpg")  # Carrega o arquivo da imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta o tamanho do fundo para caber na tela toda

rato = pygame.image.load("imagens/rato.png")  # Carrega o arquivo da imagem do rato
rato = pygame.transform.scale(rato, (TAMANHO, TAMANHO))  # Ajusta o tamanho do rato para o tamanho do bloco (25x25)

gato = pygame.image.load("imagens/gato.png")
gato = pygame.transform.scale(gato, (TAMANHO_G,TAMANHO_G))

cachorro = pygame.image.load("imagens/dog.png")
cachorro = pygame.transform.scale(cachorro, (TAMANHO, TAMANHO))

# CONFIGURAÇÃO DE ÁUDIO CORRIGIDA (Utilizando .ogg para eliminar chiados crônicos)
som_comer = pygame.mixer.Sound("sons/comer.wav")  # Carrega o efeito de mordida em formato wav estável
musica = pygame.mixer.music.load("sons/Chillin-with-My-Friends.mp3") #musica de fundo
# Paleta de cores (no formato RGB: Vermelho, Verde, Azul)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)

#travando clock
tempo = pygame.time.Clock()


# Configuração de texto e tempo
fonte = pygame.font.SysFont("Arial", 25)  # Define a fonte e o tamanho do texto do jogo
clock = pygame.time.Clock()  # Cria um objeto para controlar a velocidade do jogo (FPS)

def desenhar_cobra(lista_cobra):
    # Passa por cada segmento guardado na lista do corpo da cobra
      for bloco in lista_cobra:
        # Desenha um retângulo verde na tela para cada parte do corpo
          TELA.blit(gato, (bloco[0], bloco[1]))
  #      pygame.draw.rect(TELA, VERDE, [bloco[0], bloco[1], TAMANHO, TAMANHO]) 

def mostrar_pontuacao(pontos): 
    texto = fonte.render(f"Pontos: {pontos}", True, BRANCO)  # Transforma o texto dos pontos em uma imagem
    TELA.blit(texto, [10, 10])  # Desenha a imagem do texto na posição superior esquerda da tela

def mover_em_direcao(origem_x, origem_y, alvo_x, alvo_y):
    # Calcula a distância entre a origem e o alvo em cada eixo
    diferenca_x = alvo_x - origem_x
    diferenca_y = alvo_y - origem_y

    # Move um passo de grade, priorizando o eixo com maior distância
    if abs(diferenca_x) > abs(diferenca_y):
        origem_x += TAMANHO if diferenca_x > 0 else -TAMANHO
    elif diferenca_y != 0:
        origem_y += TAMANHO if diferenca_y > 0 else -TAMANHO
    elif diferenca_x != 0:
        origem_x += TAMANHO if diferenca_x > 0 else -TAMANHO

    # Mantém a posição dentro dos limites da tela
    origem_x = max(0, min(origem_x, LARGURA - TAMANHO))
    origem_y = max(0, min(origem_y, ALTURA - TAMANHO))

    return origem_x, origem_y

def jogo():
    # Posicionamento inicial alinhado ao grid (divide pelo tamanho e multiplica de volta)
    x = (LARGURA // 2) // TAMANHO * TAMANHO
    y = (ALTURA // 2) // TAMANHO * TAMANHO

    # Variáveis de deslocamento (velocidade da direção atual)
    dx = 0
    dy = 0

    cobra = []  # Lista que vai guardar as posições X e Y de cada bloco do corpo
    comprimento = 1  # Tamanho inicial da cobra
    velocidade = 6    # Velocidade de quadros por segundo inicial
    velocidade_maxima = 25       # velocidade maxima
    # Sorteia uma posição inicial para o rato que esteja dentro dos limites do grid
    rato_x = random.randrange(0, LARGURA - TAMANHO, TAMANHO)
    rato_y = random.randrange(0, ALTURA - TAMANHO, TAMANHO)

    cachorro1_x = 0
    cachorro1_y = 0
    cachorro2_x = LARGURA - TAMANHO
    cachorro2_y = ALTURA - TAMANHO

    rodando = True  # Variável que mantém o loop principal funcionando
    game_over = False  # Variável que controla o estado de derrota

    ultimo_movimento = pygame.time.get_ticks()
    # TRAVA DE DIREÇÃO: Reseta a cada novo movimento físico da cobra
    direcao_alterada = False
    velocidade_cachorro = 3  # Cachorros começam mais lentos que o gato
    ultimo_movimento_cachorro = pygame.time.get_ticks()
    pygame.mixer.music.play(-1)

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
                        # Recarrega e reinicia a música antes de reiniciar a partida
                        pygame.mixer.music.load("sons/Chillin-with-My-Friends.mp3")
                        pygame.mixer.music.play(-1)
                        return True  # Se apertar "C", reinicia o jogo enviando um sinal positivo

        

        # Captura de eventos do jogo em andamento (Teclado, mouses, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Se fechar no "X" durante a partida, encerra o programa
         
            if event.type == pygame.KEYDOWN:
                # Só aceita mudar de comando se ainda não mudou de direção neste frame 
                if not direcao_alterada:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx = -TAMANHO
                        dy = 0
                        direcao_alterada = True
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx = TAMANHO
                        dy = 0
                        direcao_alterada = True
                    elif event.key == pygame.K_UP and dy == 0:
                        dy = -TAMANHO
                        dx = 0
                        direcao_alterada = True
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dy = TAMANHO
                        dx = 0
                        direcao_alterada = True
                
        intervalo_movimento = 1000 // velocidade
        agora = pygame.time.get_ticks()
        if agora - ultimo_movimento >= intervalo_movimento:

            # Atualização da posição da cabeça somando o deslocamento
            x += dx
            y += dy

        # Verificação se a cabeça saiu dos limites da tela (colisão com a parede)
            if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
               game_over = True  # Ativa o estado de Game Over
               pygame.mixer.music.stop()
                # Atualização do corpo da cobra
            cabeca = [x, y]  # Cria uma lista com a coordenada atual da cabeça
            cobra.append(cabeca)  # Adiciona a cabeça na lista do corpo da cobra
            # Garante que o corpo não fique maior do que a pontuação/comprimento atual permite
            if len(cobra) > comprimento:
               del cobra[0]  # Remove o pedaço mais antigo da cauda para simular o movimento de andar
            # Verificação se a cabeça bateu em qualquer outra parte do próprio corpo
            for bloco in cobra[:-1]:
                if bloco == cabeca:
                    # Ignora a colisão se a cobra ainda estiver parada no início do jogo
                    if dx != 0 or dy != 0:
                        game_over = True
                        
             # Mecânica de comer o rato
            if x == rato_x and y == rato_y:
                som_comer.play()  # Ativa a reprodução instantânea do efeito sonoro de mordida
            # Sorteia uma nova posição para o próximo rato aparecer
                rato_x = random.randrange(0, LARGURA - TAMANHO, TAMANHO)
                rato_y = random.randrange(0, ALTURA - TAMANHO, TAMANHO)
                
                comprimento += 1  # Aumenta o tamanho do corpo da cobra
                velocidade = min(velocidade + 1, velocidade_maxima)  # Aumenta o FPS atual para o jogo acelerar e ficar mais difícil
            

         #Variavel para localização do cachoro 
            ultimo_movimento = agora
            direcao_alterada = False
        
        # Movimento dos cachorros, num ritmo próprio (metade da velocidade do gato)
        intervalo_movimento_cachorro = 1000 // max(1, velocidade // 2)
        if agora - ultimo_movimento_cachorro >= intervalo_movimento_cachorro:
           # Cachorro 1 segue a cauda
            if cobra:
                cachorro1_x, cachorro1_y = mover_em_direcao(
                cachorro1_x,
                cachorro1_y,
                cobra[0][0],
                cobra[0][1]
                               )

            # Cachorro 2 tenta interceptar a cabeça
            alvo2_x = max(0, min(x + dx * 3, LARGURA - TAMANHO))
            alvo2_y = max(0, min(y + dy * 3, ALTURA - TAMANHO))

            cachorro2_x, cachorro2_y = mover_em_direcao(
            cachorro2_x,
                cachorro2_y,
                    alvo2_x,
                        alvo2_y
                                )



            ultimo_movimento_cachorro = agora        
            # Colisão do gato com os cachorros
            if (x == cachorro1_x and y == cachorro1_y) or \
                (x == cachorro2_x and y == cachorro2_y):
                    game_over = True  
                    pygame.mixer.music.stop()
          





    
        # Renderização do cenário (Desenha de trás para frente)
        TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na posição inicial (0,0)
        TELA.blit(rato, (rato_x, rato_y))  # Desenha a imagem do rato na sua respectiva coordenada
        TELA.blit(cachorro, (cachorro1_x, cachorro1_y))
        TELA.blit(cachorro, (cachorro2_x, cachorro2_y))


        # Desenha a cobra e updates o placar por cima do fundo
        desenhar_cobra(cobra)
        mostrar_pontuacao(comprimento - 1)

        pygame.display.update()  # Mostra na janela tudo o que foi desenho neste frame

       
        # Trava a taxa de atualização do jogo de acordo com o valor da velocidade
        clock.tick(60) 
         
# Loop externo principal que gerencia o reinício limpo sem estourar a memória RAM
continuar_jogando = True
while continuar_jogando:
    continuar_jogando = jogo()  # A variável recebe o True ou False retornado pela função 'jogo'

pygame.quit()  # Fecha os módulos do Pygame com segurança e desliga a janela
