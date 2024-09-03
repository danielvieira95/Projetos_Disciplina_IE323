# Jogo do Esquiador
O BitDog foi esquiar mas sem querer confundiu a pista de inciante com a pista de profissional.
A pista de profissional tem um monte de arvores que o BitDog precisa desviar.

Vamos fazer um jogo dessa história.

A estrutura do jogo vai ser como do diagrama abaixo.
![chart](flowcharts/baixo_nivel.png)

# criar o jogador
## ligar o led
```py
from BitDogLib import * # está linha nos da acesso a funções para interagir com o BitDogLab
ligar_led(2, 0, [0,0,1])
```
como vamos mexer bastante o jogador para deixar mais fácil podemos criar variáveis para salvar os dados.

```py
AZUL = [0, 0, 1]
jogador_x = 2
jogador_y = 0
ligar_led(jogador_x, jogador_y, AZUL) 
```

## mover o jogador
para ficar fácil de mover o jogador vamos criar funções.
### mover para a direita
![função para mover o jogador a direita](flowcharts/jogador_dir.png)
```py
# como vamos usar o número total de colunas varias muitas vezes vamos criar uma variável.
TOTAL_COLUNAS = 5
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
```

### mover para a esquerda
![função para mover o jogador a esquerda](flowcharts/jogador_esq.png)
```py
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
```
## botão
```py
def jogo(delta):
    # verificamos se o jogador pressionou algum botão
    if botao_A_pressionado():
        # se ele pressionou o botão A movemos para a equerda
        jogador_esq()
    if botao_B_pressionado():
        # se ele pressionou o botão B movemos para a direita
        jogador_direita()

# passamos a função jogo que criamos como variavel da função loop
loop(jogo)
```

# criar árvores
O código vai seguir esse diagrama.
![arvores](flowcharts/mover_arvore.png)

## ligar um led
novamente podemos criar variáveis para salvar os dados que vamos usar muitas vezes.
```py
VERDE = [0, 1, 0]
arvore_x = 0
arvore_y = 4
ligar_led(arvore_x, arvore_y, VERDE)
```
## mover um led
agora que acendemos um led podemos criar a função para movê-lo
```py
def mover_arvore(tempo):
    global arvore_y
    # calculamos a distancia que as arvores vão mover
    # velocidade = distância / tempo
    # então podemos calcular a distância movida em certo tempo fazendo
    # tempo * velocidade = distância
    dist = tempo/250_000
    # apagamos a linha atual
    # usamos a função int para transformar o número quebrado da arvore_y em um inteiro
    apagar_led(arvore_x, arvore_y)
    # calculamos a nova posição da arvore
    # subtraindo a posição atual da distância movida
    arvore_y = arvore_y - dist
    # verificamos se a árvore ainda está no led
    if arvore_y < 0:
        # se a árvore já saiu do led vamos 
        arvore_y = 4
        return
    # se a árvore não saiu dos leds ligamos o led na nova posição
    ligar_led(arvore_x, arvore_y, VERDE)
```
```py
def jogo(delta):
    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()

loop(jogo)
```
## bug do .999999
Opá, parece que tem algo errado no código a árvore não parece começar na última linha.
Isso acontece porque o código começa com 4 então na primeira iteração ele já vai para baixo de 4 e muda de linha. Podemos resolver isso começando a linha com 4.999999 se usássemos 5 a função retornaria um erro pois o BitDogLab só tem linhas de 0 até 4.
```py
VERDE = [0, 1, 0]
arvore_x = 0
arvore_y = 4.999999
ligar_led(arvore_x, arvore_y, VERDE)
```
```py
def mover_arvore(tempo):
    global arvore_y
    # calculamos a distancia que as arvores vão mover
    # velocidade = distância / tempo
    # então podemos calcular a distância movida em certo tempo fazendo
    # tempo * velocidade = distância
    dist = tempo/250_000
    # apagamos a linha atual
    # usamos a função int para transformar o número quebrado da arvore_y em um inteiro
    apagar_led(arvore_x, arvore_y)
    # calculamos a nova posição da arvore
    # subtraindo a posição atual da distância movida
    arvore_y = arvore_y - dist
    # verificamos se a árvore ainda está no led
    if arvore_y < 0:
        # se a árvore já saiu do led vamos 
        arvore_y = 4.999999
        return
    # se a árvore não saiu dos leds ligamos o led na nova posição
    ligar_led(arvore_x, arvore_y, VERDE)
```

## criar uma linha de leds
não queremos apenas um led de árvore mas uma linha de árvores.
**função ligar_linha:**
![diagrama para a função](flowcharts/ligar_linha.png)
```py
# função para ligar uma linha inteira no tela led
def ligar_linha(arvore_y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para ligar cada led da linha
        ligar_led(coluna, arvore_y, VERDE)
        # aumentamos o i para 
        coluna = coluna + 1
```
Agora podemos ligar uma linha de leds ao invês de apenas um led, lembre-se de colocar a função ligar_linha antes de usa-lá.
```py
VERDE = [0, 1, 0]
arvore_x = 0
arvore_y = 4.999999
# agora aqui também precisamos mudar arvore_y para int
ligar_linha(int(arvore_y))
```
Uma função para apagar os leds também será útil.
![diagrama para a função](flowcharts/apagar_linha.png)
```py
# função para desligar uma linha inteira no tela led
def apagar_linha(y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para desligar cada led da linha
        apagar_led(coluna, y)
        coluna = coluna + 1
```
## mover uma linha de leds
Agora que temos essa funções podemos mudar o nosso código de mover árvore para mover uma linha de árvores ao invês de uma árvore só. Lembre-se de que a ligar_linha e apagar_linha precisam vir antes de mover_arvore.
```py
def mover_arvore(tempo):
    global arvore_y
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
        # se a arvore já saiu dos leds vamos voltar o valor de arvore_y para o início
        arvore_y = 4.999999
        return
    # se a arvore não saiu dos leds ligamos os leds na nova posição
    ligar_linha(int(arvore_y))
```
## criar um buraco mover o buraco
Agora precisamos de um buraco para o jogador passar, queremos que esse buraco mude aleatoriamente toda vez.
Gere um número aleatório para servir de buraco. Altere a função ligar_linha para aceitar o valor do buraco e não ascender essa linha. Lembre-se de escolher um novo buraco aleatório para cada vez que as arvores voltarem para o começo dos leds.
```py
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
```
```py
# inicializar arvore
# Escolhemos um número aleatório para o buraco
buraco = numero_aleatorio(0,4)
arvore_y = 4.999999
ligar_linha(buraco, int(arvore_y))
```
Não esqueça de mudar em todos os lugares que usamos a função ligar_linha
```py
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
```

## cuidar para o jogador conseguir passar pelo buraco
Opá, parece que encontramos outro problema, mesmo que o jogador passe no buraco ele some temporariamente.
Precisamos tomar cuidado na função apagar_linha para não apagar o led do buraco também.
```py
# função para desligar uma linha inteira no tela led
def apagar_linha(buraco, y):
    coluna = 0
    while coluna < TOTAL_COLUNAS:
    # usamos um loop para desligar cada led da linha
        if coluna != buraco:
        # usamos essa verificação para pular o led do buraco pois o jogador pode estar nele
            apagar_led(coluna, y)
        coluna = coluna + 1
```
Não esqueça de mudar em todos os lugares que usar a função apagar_linha
```py
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
        # novo número aleatório para o buraco
        buraco = numero_aleatorio(0,4)
        # se a arvore já saiu dos leds vamos voltar o valor de arvore_y para o início
        arvore_y = 4.999999
        return
    # se a arvore não saiu dos leds ligamos os leds na nova posição
    ligar_linha(buraco, int(arvore_y))
```

# adicionar morte
Para deixar o jogo mais divertido quando o jogador bate em uma árvore o jogo deve acabar.
## Detectar morte
Vamos criar uma função que consiga descobrir se o jogador morreu ou não.
Dica: o jogador está morto se as árvores estão na mesma linha que o jogador e o jogador não estiver na coluna do buraco.
```py
# verifica se o jogador está morto
def morto():
    # se o jogador estiver na mesma linha das arvores e não estiver na coluna do burco ele morreu
    if jogador_x != buraco and jogador_y == int(arvore_y):
        return True
    # caso contrario ele sobreviveu
    else:
        return False
```
```py
def jogo(delta):
    # verificamos se o jogador morreu
    if morto():
        # por enquanto para verificar que funcionou podemos printar um texto.
        print('morreu')

    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()
```
## parar o jogo
Agora que já sabemos quando o jogador morreu basta parar o jogo nesses momentos.
Dica você pode usar o return para sair da função mais cedo 
```py
    def jogo(delta):
        # verificamos se o jogador morreu
        if morto():
            ligar_led(jogador_x, jogador_y, VERMELHO)
            return

        # passamos o delta que é o tempo desde a última iteração para a nossa nova função
        mover_arvore(delta)

        if botao_A_pressionado():
            jogador_esq()
        if botao_B_pressionado():
            jogador_direita()
```
## reiniciar o jogo
legal mas agora como podemos voltar a jogar?
Vamos mudar a função para que quando o jogador apertar um dos botões o jogo comece de novo do zero.
Para reiniciar o jogo precisamos fazer algumas coisas.
- apagar todos os leds
- voltar a arvore para a posição inicial
- escolher um novo buraco
- voltar o jogador para a posição inicial
como estamos reiniciando a arvore em mais de uma parte do código pode ser útil ter uma função para fazer isso.
```py
# reseta os valores da arvore
def resetar_arvore():
    global buraco
    global arvore_y
    # escolhemos um novo buraco aleatório
    buraco = numero_aleatorio(0,4)
    # retornamos as arvores para a parte de baixo da tela
    arvore_y = 4.999999
```
Agora podemos usar essa função para o mover_arvore e na hora da morte do jogador
```py
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
```
podemos aproveitar e criar uma função para reiniciar os valores do jogador para deixar mais organizado.
```py
# reseta os valores do jogador quando ele morrer
def resetar_jogador():
    global jogador_x
    global jogador_y
    # redefinimos a posição do jogador
    jogador_x = 2
    jogador_y = 0
    # ligamos o led na posição inicial
    ligar_led(jogador_x, jogador_y, AZUL)
```

```py
def jogo(delta):
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
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
```
## adicionar som de morte
Para deixar um pouco mais legal podemos adicionar um som quando o jogador morre
```py
def jogo(delta):
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
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
```
## AaaH está tocando sem parar!
Parece que fizemos um erro bem chato o som era para tocar apenas uma vez mas está tocando sem parar.
O que acontece é que na verdade queremos que o som toque só na primeira vez que o `if` for verdade.
Podemos usar uma variável global para verificar se é a primeira vez que tocamos o som ou não
```py
jogador_x = 2
jogador_y = 0
ligar_led(jogador_x, jogador_y, AZUL) 
morreu = False
```
```py
def jogo(delta):
    global morreu
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
        # verificamos se é a primeira vez para tocar o som
        if not morreu:
            # tocamos o som
            som_morreu()
            # mudamos a variável para não tocar o som de novo
            morreu = True
        # verificamos se o jogador pressionou um botão para voltar ao jogo
        if botao_A_pressionado() or botao_B_pressionado():
            # primeiro apagamos todos os leds
            apagar_leds()
            # resetamos a árvore
            resetar_arvore()
            # resetamos o jogador
            resetar_jogador()
            # agora resetamos a variável para que da próxima vez toque o som de novo
            morreu = False
        return

    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()
```

# adicionar pontuação
Sem saber quão bom fomos a cada vez que jogamos o jogo é meio chato, então vamos adicionar pontuações!
Podemos guardar os pontos de um jogador em uma variável global.
```py
jogador_x = 2
jogador_y = 0
ligar_led(jogador_x, jogador_y, AZUL) 
morreu = False
pontos = 0
```
Queremos subir os pontos toda vez que o jogador passar uma linha de arvores.
Então o melhor lugar para fazer isso é na função resetar_arvore que é chamada toda vez que as árvores chegam no jogador.
![resetar arvore](flowcharts/resetar_arvore_sem_pontos.png)

```py
# reseta os valores da arvore
def resetar_arvore():
    global buraco
    global arvore_y
    global pontos
    # escolhemos um novo buraco aleatório
    buraco = numero_aleatorio(0,4)
    # retornamos as arvores para a parte de baixo da tela
    arvore_y = 4.999999
    # acrescentamos aos pontos
    pontos = pontos + 1
```
Para exibir os pontos podemos usar a telinha do BitDogLab.
Podemos fazer isso na nossa função de jogo.
```py
def jogo(delta):
    global morreu
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
        # verificamos se é a primeira vez para tocar o som
        if not morreu:
            # tocamos o som
            som_morreu()
            # mudamos a variável para não tocar o som de novo
            morreu = True
        # verificamos se o jogador pressionou um botão para voltar ao jogo
        if botao_A_pressionado() or botao_B_pressionado():
            # primeiro apagamos todos os leds
            apagar_leds()
            # resetamos a árvore
            resetar_jogador()
            # agora resetamos a variável para que da próxima vez toque o som de novo
            resetar_arvore()
            # resetamos o jogador
            morreu = False
        return

    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    # escrevemos a pontuação
    limpar_tela()
    escrever_tela("score: " + str(pontos),0,0)
    mostrar_tela()

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()
```

## resetar os pontos
Parece que esquecemos de resetar os pontos para não subir sem parar.
Vamos adicionar isso na função resetar jogador já que queremos limpar os pontos todas as vezes que o jogador resetar o jogo.

![jogador](flowcharts/resetar_jogador.png)

```py
# reseta os valores do jogador quando ele morrer
def resetar_jogador():
    global jogador_x
    global jogador_y
    global pontos
    # redefinimos a posição do jogador
    jogador_x = 2
    jogador_y = 0
    # ligamos o led na posição inicial
    ligar_led(jogador_x, jogador_y, AZUL)
    pontos = 0
```
## HighScore
Pode ser legal se o jogo lembrar qual foi a melhor pontuação.
Para isso podemos adicionar mais uma variável global.
```py
jogador_x = 2
jogador_y = 0
ligar_led(jogador_x, jogador_y, AZUL) 
morreu = False
pontos = 0
highscore = 0
```
agora quando alteramos os pontos vamos verificar se os pontos são maiores que o HighScore.
![resetar arvore](flowcharts/resetar_arvore.png)
```py
# reseta os valores da arvore
def resetar_arvore():
    global buraco
    global arvore_y
    global pontos
    global highscore
    # escolhemos um novo buraco aleatório
    buraco = numero_aleatorio(0,4)
    # retornamos as arvores para a parte de baixo da tela
    arvore_y = 4.999999
    # acrescentamos aos pontos
    pontos = pontos + 1
    # se a nova pontuação for maior que o highscore mudamos o highscore
    if pontos > highscore:
        highscore = pontos
```
vamos também exibir o HighScore na telinha.
```py
def jogo(delta):
    global morreu
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
        # verificamos se é a primeira vez para tocar o som
        if not morreu:
            # tocamos o som
            som_morreu()
            # mudamos a variável para não tocar o som de novo
            morreu = True
        # verificamos se o jogador pressionou um botão para voltar ao jogo
        if botao_A_pressionado() or botao_B_pressionado():
            # primeiro apagamos todos os leds
            apagar_leds()
            # resetamos o jogador
            resetar_jogador()
            # resetamos a árvore
            resetar_arvore()
            # agora resetamos a variável para que da próxima vez toque o som de novo
            morreu = False
        return

    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    # escrevemos a pontuação
    limpar_tela()
    escrever_tela("score: " + str(pontos),0,0)
    # a altura de uma linha de texto é mais ou menos 10 pixels então adicionamos isso na variável para y
    escrever_tela("HighScore: " + str(highscore),0,10)
    mostrar_tela()

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()
```

## Salvar HighScore em arquivo
Seria legal se o HighScore continuasse salvo mesmo depois de desligar o BitDogLab, para isso precisamos salvar e ler um arquivo.
Dá primeira vez que executarmos o código o arquivo ainda não existe, então a função vai retornar vázio, por isso precisamos verificar se está vazio ou não.
Se estiver vázio vamos iniciar com 0, se tiver algum valor vamos transformar o texto (string) em número (int) para podermos fazer calculos
```py
# definimos um nome para o arquivo
HIGHSCORE_FILE = 'highscore.txt'
# lemos o highscore
texto_arquivo = ler_arquivo(HIGHSCORE_FILE)
if texto_arquivo == '':
    highscore = 0
else:
    highscore = int(texto_arquivo)
```
Para a parte de salvar, vamos salvar quando o jogador morrer.
Escrever um arquivo é um pouco demorado para o computador então é melhor evitar fazer muitas vezes.
```py
def jogo(delta):
    global morreu
    # verificamos se o jogador morreu
    if morto():
        ligar_led(jogador_x, jogador_y, VERMELHO)
        # verificamos se é a primeira vez para tocar o som
        if not morreu:
            # tocamos o som
            som_morreu()
            # mudamos a variável para não tocar o som de novo
            morreu = True
            # salvamos o novo highscore transformando o numero inteiro em texto (string)
            escrever_arquivo(HIGHSCORE_FILE, str(highscore))
        # verificamos se o jogador pressionou um botão para voltar ao jogo
        if botao_A_pressionado() or botao_B_pressionado():
            # primeiro apagamos todos os leds
            apagar_leds()
            # resetamos o jogador
            resetar_jogador()
            # resetamos a arvore
            resetar_arvore()
            # agora resetamos a variável para que da próxima vez toque o som de novo
            morreu = False
        return

    # passamos o delta que é o tempo desde a última iteração para a nossa nova função
    mover_arvore(delta)

    # escrevemos a pontuação
    limpar_tela()
    escrever_tela("score: " + str(pontos),0,0)
    # a altura de uma linha de texto é mais ou menos 10 pixels então adicionamos isso na variável para y
    escrever_tela("HighScore: " + str(highscore),0,10)
    mostrar_tela()

    if botao_A_pressionado():
        jogador_esq()
    if botao_B_pressionado():
        jogador_direita()
```
