from BitDogLib import *

# cores
AZUL = [0, 0, 1]
VERMELHO = [1, 0, 0]
VERDE = [0, 1, 0]

# como vamos usar o número total de colunas varias muitas vezes vamos criar uma variável.
TOTAL_COLUNAS = 5

jogador_x = 2
jogador_y = 0
ligar_led(jogador_x, jogador_y, AZUL) 

# função para ligar uma linha inteira no tela led
def ligar_linha(buraco, arvore_y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para ligar cada led da linha
        # usamos essa verificação para pular o led do buraco
        if coluna != buraco:
            ligar_led(coluna, arvore_y, VERDE)
        # aumentamos o i para 
        coluna = coluna + 1

# função para desligar uma linha inteira no tela led
def apagar_linha(buraco, y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para desligar cada led da linha
        if coluna != buraco:
        # usamos essa verificação para pular o led do buraco pois o jogador pode estar nele
            apagar_led(coluna, y)
        coluna = coluna + 1

buraco = numero_aleatorio(0,4)
arvore_y = 4.999999
ligar_linha(buraco, int(arvore_y))

# função para mover o jogador para a direita
def jogador_direita():
    global jogador_x
    # primeiro verificamos se o jogador não está no canto direito
    if jogador_x >= TOTAL_COLUNAS - 1:
        return
    # apagamos o led da posição atual do jogador
    apagar_led(jogador_x, jogador_y)
    # mudamos a posição para a direita
    jogador_x = jogador_x + 1
    # ligamos o led da nova posição do jogador
    ligar_led(jogador_x,jogador_y, AZUL)

def jogador_esq():
    # declaramos que vamos fazer alterações na variável global
    global jogador_x
    # primeiro verificamos se o jogador não está no canto esquerdo
    if jogador_x <= 0:
        return
    # apagamos o led da posição atual do jogador
    apagar_led(jogador_x, jogador_y)
    # mudamos a posição para a esquerda
    jogador_x = jogador_x - 1
    # ligamos o led da nova posição do jogador
    ligar_led(jogador_x, jogador_y, AZUL)

# reseta os valores da arvore
def resetar_arvore():
    global buraco
    global arvore_y
    # escolhemos um novo buraco aleatório
    buraco = numero_aleatorio(0,4)
    # retornamos as arvores para a parte de baixo da tela
    arvore_y = 4.999999

# reseta os valores do jogador quando ele morrer
def resetar_jogador():
    global jogador_x
    global jogador_y
    # redefinimos a posição do jogador
    jogador_x = 2
    jogador_y = 0
    # ligamos o led na posição inicial
    ligar_led(jogador_x, jogador_y, AZUL)

def mover_arvore(tempo):
    global arvore_y
    global buraco
    # calculamos a distancia que as arvores vão mover
    # velocidade = distância / tempo
    # então podemos calcular a distância movida em certo tempo fazendo
    # tempo * velocidade = distância
    dist = tempo/250_000
    # apagamos a linha atual
    # usamos a função int para transformar o número quebrado da arvore_y em um inteiro
    apagar_linha(buraco, int(arvore_y))
    # calculamos a nova posição da arvore
    # subtraindo a posição atual da distância movida
    arvore_y = arvore_y - dist
    # verificamos se a arvore ainda está nos leds
    if arvore_y < 0:
        resetar_arvore()
        return
    # se a arvore não saiu dos leds ligamos os leds na nova posição
    ligar_linha(buraco, int(arvore_y))

# verifica se o jogador está morto
def morto():
    # se o jogador estiver na mesma linha das arvores e não estiver na coluna do burco ele morreu
    if jogador_x != buraco and jogador_y == int(arvore_y):
        return True
    # caso contrario ele sobreviveu
    else:
        return False

def jogo(delta):
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
        # verificamos se é a primeira vez para tocar o som
        # tocamos o som
        som_morreu()
        # verificamos se o jogador pressionou um botão para voltar ao jogo
        if botao_A_pressionado() or botao_B_pressionado():
            # primeiro apagamos todos os leds
            apagar_leds()
            # resetamos o jogador
            resetar_jogador()
            # resetamos a árvore
            resetar_arvore()
        return

    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()


# passamos a função jogo que criamos como variavel da função loop
loop(jogo)