from BitDogLib import * # está linha nos da acesso a funções para interagir com o BitDogLab

AZUL = [0, 0, 1]
jogador_x = 2
jogador_y = 0
ligar_led(jogador_x, jogador_y, AZUL) 

# como vamos usar o número total de colunas varias muitas vezes vamos criar uma variável.
TOTAL_COLUNAS = 5

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
def apagar_linha(y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para desligar cada led da linha
        apagar_led(coluna, y)
        coluna = coluna + 1


VERDE = [0, 1, 0]
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
    apagar_linha(int(arvore_y))
    # calculamos a nova posição da arvore
    # subtraindo a posição atual da distância movida
    arvore_y = arvore_y - dist
    # verificamos se a arvore ainda está nos leds
    if arvore_y < 0:
        # novo número aleatório para o buraco
        buraco = numero_aleatorio(0,4)
        # se a arvore já saiu dos leds vamos voltar o valor de arvore_y para o início
        arvore_y = 4.999999
        return
    # se a arvore não saiu dos leds ligamos os leds na nova posição
    ligar_linha(buraco, int(arvore_y))

def jogo(delta):
    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()


# passamos a função jogo que criamos como variavel da função loop
loop(jogo)
