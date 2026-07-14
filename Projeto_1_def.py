import pygame
# Importa a biblioteca Pygame, que fornece as ferramentas pra criar jogos:
# janelas, desenho, controle de teclado, tempo, etc.

pygame.init()
# Inicializa todos os módulos internos do Pygame.
# Sem isso, várias funções (como criar janela) não funcionam direito.

largura = 600
altura = 600
# Variáveis que definem o tamanho da janela do jogo, em pixels.

tela = pygame.display.set_mode((largura, altura))
# Cria a janela do jogo com o tamanho definido acima.
# set_mode() espera uma TUPLA (largura, altura) — por isso os parênteses duplos.
# 'tela' guarda a "superfície" onde tudo será desenhado.

pygame.display.set_caption("Projeto_1",)
# Define o texto que aparece na barra de título da janela.

# posição inicial do personagem
x = 100
y = 100
# Coordenadas do canto SUPERIOR ESQUERDO do quadrado.
# Em telas de computador, x cresce pra direita e y cresce PRA BAIXO
# (diferente do gráfico de matemática que você já conhece).

tamanho = 50
# Tamanho do lado do quadrado (ele é desenhado como um quadrado 50x50).

velocidade = 5
# Quantos pixels o quadrado se move a cada frame (quadro) do jogo.


def travar_evento():
    """Verifica os eventos (como fechar a janela) e retorna se o jogo deve continuar."""
    # 'eventos' são coisas que acontecem: teclas pressionadas, cliques,
    # fechar a janela, etc. O Pygame acumula tudo isso numa lista a cada frame.

    for evento in pygame.event.get():
        # pygame.event.get() devolve a lista de eventos que ocorreram
        # desde a última vez que verificamos. O 'for' percorre essa lista,
        # um evento de cada vez, guardando cada um na variável 'evento'.

        if evento.type == pygame.QUIT:
            # Verifica se ESSE evento específico é do tipo "QUIT"
            # (que o Pygame gera automaticamente quando você clica no X da janela).

            return False
            # Se for QUIT, a função "sai" imediatamente e devolve False,
            # sinalizando pro loop principal: "pode parar de rodar".

    return True
    # IMPORTANTE: esta linha está FORA do 'for' (mesma indentação dele, não do 'if').
    # Ou seja: só é executada depois que TODOS os eventos da lista foram checados
    # e nenhum deles era QUIT. Devolve True: "pode continuar rodando o jogo".


def mover_jogador(x, y):
    """Lê o teclado e retorna a nova posição x, y do jogador."""
    # Repare que x e y aqui são PARÂMETROS: cópias locais das variáveis
    # de fora. Mudar eles aqui dentro não muda automaticamente o x e y
    # do restante do programa — por isso, no final, usamos 'return'
    # pra devolver os novos valores.

    teclas = pygame.key.get_pressed()
    # Devolve uma lista enorme com o estado de TODAS as teclas do teclado
    # nesse exato frame: True se está pressionada, False se não está.

    if teclas[pygame.K_RIGHT]:
        # Verifica especificamente a posição da seta DIREITA nessa lista.
        x += velocidade
        # Equivale a "x = x + velocidade". Move o quadrado pra direita.

    if teclas[pygame.K_LEFT]:
        x -= velocidade
        # Move pra esquerda.

    if teclas[pygame.K_UP]:
        y -= velocidade
        # Diminui y = sobe na tela (lembre: y cresce pra baixo).

    if teclas[pygame.K_DOWN]:
        y += velocidade
        # Aumenta y = desce na tela.

    x = max(0, min(x, largura - tamanho))
    # Trava o valor de x dentro dos limites da tela:
    # - min(x, largura - tamanho): garante que x nunca passe do limite direito
    #   (largura - tamanho, pra sobrar espaço pro quadrado inteiro caber).
    # - max(0, ...): garante que o resultado não fique negativo (fora à esquerda).
    # Essa linha está FORA de todos os 'if' acima, então roda sempre,
    # independente de qual tecla foi apertada.

    y = max(0, min(y, altura - tamanho))
    # Mesma lógica, só que pro eixo vertical.

    return x, y
    # Devolve os dois valores atualizados juntos (como uma tupla),
    # pra quem chamou a função poder atualizar suas próprias variáveis.


def desenhar(x, y):
    """Limpa a tela e desenha o jogador na posição atual."""

    tela.fill((30, 20, 80))
    # Pinta TODA a tela com essa cor (formato RGB: vermelho, verde, azul,
    # cada um de 0 a 255). Isso "apaga" o frame anterior — sem isso,
    # o desenho antigo ficaria borrado/acumulado na tela.

    pygame.draw.rect(tela, (255, 255, 255), (x, y, tamanho, tamanho))
    # Desenha um retângulo:
    # - 'tela': onde desenhar
    # - (255,255,255): cor branca
    # - (x, y, tamanho, tamanho): posição (canto sup. esquerdo) + largura/altura

    pygame.display.flip()
    # Atualiza a JANELA de verdade com tudo que foi desenhado até aqui.
    # Sem essa linha, os comandos acima só existem "internamente",
    # nada aparece de fato na tela pro usuário ver.


relogio = pygame.time.Clock()
# Cria um "relógio" que vamos usar pra controlar a velocidade do loop
# (quantas vezes por segundo ele roda), garantindo que o jogo tenha
# velocidade parecida em qualquer computador.

rodando = True
# Variável que controla se o loop principal deve continuar. Começa em True.

while rodando:
    # Esse é o "game loop": o coração do jogo. Repete infinitamente
    # (várias vezes por segundo) tudo que estiver dentro dele, até
    # 'rodando' virar False.

    rodando = travar_evento()
    # Chama a função, e guarda o resultado (True ou False) de volta
    # na variável 'rodando'. Se o usuário fechou a janela, isso vira False,
    # e o 'while' vai parar na PRÓXIMA verificação (não instantaneamente).

    x, y = mover_jogador(x, y)
    # Chama a função passando a posição atual, e recebe de volta
    # a posição atualizada, sobrescrevendo x e y.

    desenhar(x, y)
    # Redesenha a tela inteira com a posição mais recente do quadrado.

    relogio.tick(165)
    # Pausa o loop o suficiente pra não ultrapassar 165 "voltas" por segundo
    # (ajustado à taxa de atualização do seu monitor). Isso evita que o jogo
    # rode rápido demais em PCs potentes.

pygame.quit()
# Quando o loop termina (rodando virou False), encerra o Pygame
# de forma organizada, liberando os recursos usados pela janela.