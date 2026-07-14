import pygame
pygame.init()

largura = 600
altura = 600


tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Projeto_1")

#possição inicial dos personagens
x = 100
y = 100
tamanho = 50
velocidade  = 5
 
relogio = pygame.time.Clock()

rodando= True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_RIGHT]:
        x += velocidade

    if teclas[pygame.K_LEFT]:
        x -= velocidade

    if teclas[pygame.K_UP]:
        y -= velocidade

    if teclas[pygame.K_DOWN]:
        y += velocidade

    if x < 0:
        x=0
    if x > largura - tamanho:
        x = largura - tamanho

    if y < 0:
        y = 0
    if y > altura - tamanho:
        y = altura - tamanho

    tela.fill((30,20,80))
    pygame.draw.rect(tela, (255,255,255),(x, y ,tamanho, tamanho))
    pygame.display.flip()

    relogio.tick(165)

pygame.quit()