from BitDogLib import *
from utime import ticks_us

# Para não quebrar caso dê um erro todo o jogo está num bloco try
try:
    # Variaveis que serão para indicar se o navio esta na horizontal ou vertical
    HORIZONTAL = 0
    VERTICAL = 1

    # Cores no formato RGB
    VERDE = [0,10,0]
    VERMELHO = [10,0,0]
    AZUL = [0,0,10]
    BRANCO = [10,10,10]
    APAGADO = [0,0,0]

    # Essa classe representa um navio
    class Navio:
        # O navio inicializa na posição 0 0, na horizontal e ainda não colocado
        def __init__(self, tamanho) -> None:
            self.x = 0
            self.y = 0
            self.orientacao = HORIZONTAL
            self.tamanho = tamanho
            self.colocado = False

        # adiciona o navio a uma matriz e retorna a nova matriz
        def adicionar_a_matriz(self, matriz):
            b = 0
            x = round(self.x)
            y = round(self.y)
            while b < self.tamanho:
                if self.orientacao == HORIZONTAL:
                    matriz[y][x + b] = VERDE
                else:
                    matriz[y + b][x] = VERDE
                b = b + 1
            return matriz

    # Essa lista guarda todos os navios que serão usados, cada um com seu tamanho
    navios = [Navio(3),
            Navio(3),
            Navio(2),
            Navio(2),
            Navio(1),
            Navio(1)]

    # Essa função verifica se o navio novo pode ser posicionado na posição escolhida
    # e também desenha a matriz nos leds
    def posicionando_navio(novo_navio:Navio, navios:list[Navio]):
        matriz = criar_matriz_navios(navios)
        # representa quantos leds do navio já foram posicionados
        leds_do_navio = 0
        # representa se a posição do navio é aceitavel
        aceitavel = True
        while leds_do_navio < novo_navio.tamanho:
            # verificamos se o barco esta na orientação horizontal ou vertical
            if novo_navio.orientacao == HORIZONTAL:
                x = novo_navio.x + leds_do_navio
                y = novo_navio.y
            else:
                x = novo_navio.x
                y = novo_navio.y + leds_do_navio
            # arredondamos para ter números inteiros
            x = round(x)
            y = round(y)
            # se a posição já está ocupada pintamos o led de vermelho
            if matriz[y][x] == VERDE:
                matriz[y][x] = VERMELHO
                aceitavel = False
            # caso contrário pintamos de branco
            else:
                matriz[y][x] = BRANCO
            leds_do_navio = leds_do_navio + 1
        ligar_matriz(matriz)
        return aceitavel

    # Cria uma matriz e adiciona todos os barcos à ela
    def criar_matriz_navios(navios:list[Navio]):
        matriz = criar_matriz()
        for navio in navios:
            # verificamos se o navio já foi colocado ou não
            # navios não colocados ainda não tem uma posição confirmada
            if navio.colocado:
                matriz = navio.adicionar_a_matriz(matriz)
        return matriz

    # cria a matriz com todos os navios e liga os leds
    def criar_matriz_todos_os_navios(navios:list[Navio]):
        matriz = criar_matriz_navios(navios)
        ligar_matriz(matriz)
        return matriz

    # calcula quanto tempo passou desde o último ciclo em micro segundos
    def tempo_de_jogo(old):
        new = ticks_us()
        delta = abs(new - old)
        old = new
        return (delta, old)

    # controla o posicionamento do navio
    def fase_posicionamento():
        navios_restantes = len(navios)
        for navio in navios:
            limpar_tela()
            escrever_tela("FASE DE ", 0, 0)
            escrever_tela("POSICIONAMENTO", 0, 10)
            escrever_tela(f'{navios_restantes} navios', 0, 20)
            escrever_tela('Restantes', 0, 30)
            mostrar_tela()
            old = ticks_us()
            # loop para ler inputs
            while True:
                delta, old = tempo_de_jogo(old)
                # variaveis do tamanho do navio para controlar o posicionamento do navio
                x_end = 1
                y_end = 1
                # botão para trocar a orientação
                if botao_A_pressionado():
                    if navio.orientacao == VERTICAL:
                        if round(navio.x) + navio.tamanho <= 5:
                            navio.orientacao = HORIZONTAL
                    else:
                        if round(navio.y) + navio.tamanho <= 5:
                            navio.orientacao = VERTICAL

                # definimos qual eixo do navio é maior
                if navio.orientacao == VERTICAL:
                    y_end = navio.tamanho
                else:
                    x_end = navio.tamanho

                # controle do joystick no eixo x
                jx = joystick_x()
                # verificamos se podemos mover mais para a direita
                if jx > 0 and navio.x <= 5-x_end:
                    # 1/250000 representa a velocidade em leds por microsegundo
                    # somamos a quantidade movida a posição do navio
                    navio.x = navio.x + 1/250000*delta
                # verificamos se podemos mover mais para a esquerda
                if jx < 0 and navio.x >= 0:
                    # subtraimos a quantidade movida a posição do navio
                    navio.x = navio.x - 1/250000*delta

                # controle do joystick no eixo y
                jy = joystick_y()
                # verificamos se podemos mover mais para cima
                if jy > 0 and navio.y <= 5-y_end:
                    # 1/250000 representa a velocidade em leds por microsegundo
                    # somamos a quantidade movida a posição do navio
                    navio.y = navio.y + 1/250000*delta
                # verificamos se podemos mover mais para baixo
                if jy < 0 and navio.y >= 0:
                    # subtraimos a quantidade movida a posição do navio
                    navio.y = navio.y - 1/250000*delta

                # verificamos se podemos posicionar e também desenhamos os navios na tela
                pode = posicionando_navio(navio, navios)
                # botão para confirmar o posicionamento do navio
                if botao_B_pressionado() and pode:
                    navio.colocado = True
                    break
            # atualizamos a quantidade de navios
            navios_restantes = navios_restantes - 1
        # criamos a matriz final dos barcos
        matriz = criar_matriz_todos_os_navios(navios)
        return matriz
    
    # Essa função é a fase de ataque em si
    # posiciona o tiro
    # envia uma msg ao inimigo com as informações sobre o tiro
    # e verifica se acertou e acabou
    def dar_tiro(matriz_tiros):
        # valores iniciais
        old = ticks_us()
        tiro_x = 2
        tiro_y = 2
        acabou = False
        # loop enquanto não acabou ou ganhou
        while True:
            # Limpa a tela e indica que está em fase de ataque
            limpar_tela()
            escrever_tela("FASE DE ATAQUE", 0, 0)
            mostrar_tela()
            
            # Atualiza o tempo jogo
            delta, old = tempo_de_jogo(old)
            
            #obtem os valores de x e y do joystick
            jx = joystick_x()
            jy = joystick_y()
            
            # JX e jy somente podem ter valores de 0 a 4
            # Esses if fazem essas limitações
            
            if jx > 0 and tiro_x <= 4:
                # v = v0 + at
                tiro_x = tiro_x + 1/250000*delta
            if jx < 0 and tiro_x >= 0:
                # v = v0 + at
                tiro_x = tiro_x - 1/250000*delta

            if jy > 0 and tiro_y <= 4:
                # v = v0 + at
                tiro_y = tiro_y  + 1/250000*delta
            if jy < 0 and tiro_y >= 0:
                # v = v0 + at
                tiro_y = tiro_y - 1/250000*delta

            # por padrão pode é True
            pode = True
            # Só pode atirar nas posições as quais estão Apagadas
            if matriz_tiros[round(tiro_y)][round(tiro_x)] != APAGADO:
                # A cor do indicador de tiro ficará em vermelho
                cor_ponteiro = VERMELHO
                # Pode muda para false
                pode = False
            else:
                # Se pode o indicador de tiro fica branco
                cor_ponteiro = BRANCO

            # Se o jogador pressionar o botão B e poder dar o tiro então:
            if botao_B_pressionado() and pode:
                # Verifica se acertou e se acabou
                acertou, acabou = checar_acertou_ganhou(tiro_x, tiro_y)
                # Atualiza o tempo atual
                old = ticks_us()
                # Se acertou, a posição onde o indicador está fica em verde
                if acertou:
                    matriz_tiros[round(tiro_y)][round(tiro_x)] = VERDE
                # Se errou, a posição onde o indicador está fica em azulacertou
                # além disso sai da fase de dar tiro
                else:
                    matriz_tiros[round(tiro_y)][round(tiro_x)] = AZUL
                    break

                # Se acabou sai da fase de dar tiro
                if(acabou):
                    break
            # Printa a situação do jogo atual
            desenhar_tiros(matriz_tiros, tiro_x, tiro_y, cor_ponteiro)
        # retorna se o jogo acabou
        return acabou

    # Essa função envia o tiro e verifica se ganhou
    def checar_acertou_ganhou(x, y):
        # arredonda os valores de x e y
        x = round(x)
        y = round(y)

        # envia a msg com as informações sobre o tiro por WiFi
        enviar_via_wifi([x,y])
        # Espera resposta do inimigo
        dado = esperar_receber()
        # Decompõe o dado em acertou e acabou
        acertou = dado[0]
        acabou = dado[1]
        # Se não acertou
        if acertou == 0:
            # Toca animação de agua no OLED
            agua_oled()
            # Toca o som de agua
            som_agua()
        elif acertou == 1:
            # Toca animação de explosão no OLED
            explosao_oled()
            # Toca o som de explosão
            som_explosao()
        #retorna acertou e acabou
        return acertou, acabou

    # Essa função atualiza o elemento X, Y do mapa do atacante após um tiro
    def desenhar_tiros(matriz_tiros, tiro_x, tiro_y, cor_ponteiro):
        matriz = copiar_matriz(matriz_tiros)
        matriz[round(tiro_y)][round(tiro_x)] = cor_ponteiro
        ligar_matriz(matriz)
    
    # Essa função checa se o jogador perdeu
    # Caso haja algum elemento na matriz da cor verde
    # quer dizer que não acabou ainda
    # A função retorna se acabou ou não
    def checar_perdeu(matriz_navios):
        y = 0
        while y < 5:
            x = 0
            while x < 5:
                if matriz_navios[y][x] == VERDE:
                    return False
                x = x + 1
            y = y + 1

        return True

    # Essa função é a fase de defesa em si
    # Nela o jogador vê como ele posicionou seus barcos e onde o inimigo atacou
    def receber_tiro(matriz_navios):
        # Por padrão o acabou é 0 (Falso)
        acabou = 0
        
        # Indica na tela a situação atual do mapa do jogador
        # Com onde recebeu tiros e os seus navios
        ligar_matriz(matriz_navios)
        
        # Defende/Recebe tro até o inimigo errar ou jogo acabar
        while True:
            # Limpa a tela e indica que está em fase de defesa
            limpar_tela()
            escrever_tela("FASE DE DEFESA", 0, 0)
            mostrar_tela()
            # Por padrão acertou é falso
            acertou = 0
            # O jogador fica aguardando receber uma mensagem com o ataque inimigo
            dado = esperar_receber()
            # Decompõe a msg em tiro X e tiro Y
            tiro_x = dado[0]
            tiro_y = dado[1]
            # Caso o elemento que está na posição X Y da matriz for verde
            # Quer dizer que acertou um navio
            if matriz_navios[tiro_y][tiro_x] == VERDE:
                # Acertou vira 1 (Verdadeiro)
                acertou = 1
                # O Elemento XY muda sua cor para vermelho
                matriz_navios[tiro_y][tiro_x] = VERMELHO
                # Toca animação de explosão no OLED
                explosao_oled()
                # Toca som de explosão
                som_explosao()
            # Caso o elemento na posição XY não for verde
            # Quer dizer que não acertou um navio
            else:
                # O Elemento XY muda sua cor para azul
                matriz_navios[tiro_y][tiro_x] = AZUL
                # Toca animação de agua no OLED
                agua_oled()
                # Toca som de agua
                som_agua()

            # Checa se perdeu
            if checar_perdeu(matriz_navios):
                acabou = 1
            # Envia ao inimigo indicando se ele acertou e se o jogo acabou
            enviar_via_wifi([acertou, acabou])

            # Atualiza a matriz de LED com a situação atual do jogo
            ligar_matriz(matriz_navios)
            # Caso inimigo não acertou, ou acabou, sai do loop
            if acertou == 0 or acabou == 1:
                break
                
        # retorna valor de acabou
        return acabou

    # Essa função representa a fase de ataque
    # Caso acabar no ataque, o jogador ganha
    def atacar(matriz_tiros):
        acabou = dar_tiro(matriz_tiros)
        if acabou:
            limpar_tela()
            escrever_tela("GANHOU",0,0)
            mostrar_tela()
            carinha_feliz(AZUL)
            return True
        return False

    # Essa função representa a fase de defesa
    # Caso acabar na fase de defesa, o jogador perdeu
    def defender():
        acabou = receber_tiro(matriz_navios)
        if acabou:
            limpar_tela()
            escrever_tela("PERDEU",0,0)
            mostrar_tela()
            carinha_triste(VERMELHO)
            return True
        return False


    # Essa função é a batalha do Time A
    # primeiro ataca, depois defente
    # Enquanto não acabar o jogo
    def time_A_batalha(matriz_tiros):
        while True:
            acabou = atacar(matriz_tiros)
            if acabou:
                break
            acabou = defender()
            if acabou:
                break

    # Essa função é a batalha do Time B
    # primeiro defende, depois ataca
    # Enquanto não acabar o jogo
    def time_B_batalha(matriz_tiros):
        while True:
            acabou = defender()
            if acabou:
                break
            acabou = atacar(matriz_tiros)
            if acabou:
                break
    
    # Aqui começa a fase de batalha
    # Se o jogador for um servidor ele joga como time A
    # senão como time B
    def fase_batalha(time):
        matriz_tiros = criar_matriz()
        if is_servidor:
            time_A_batalha(matriz_tiros)
        else:
            time_B_batalha(matriz_tiros)

    # Aqui o jogador escolherá o lado
    def escolher_lado():
        # Imprimi no OLED as instruções para o jogador
        limpar_tela()
        escrever_tela("Escolha seu lado", 0, 0)
        escrever_tela("A<-Time A", 0, 10)
        escrever_tela("Time B->B", 0, 20)
        mostrar_tela()
        
        # Espera o jogador pressionar botão A ou B
        while True:
            if botao_A_pressionado():
                return True
            if botao_B_pressionado():
                return False

    # Aqui o jogador escolherá qual grupo deseja jogar
    # Apenas 2 jogadores de mesmo grupo poderão jogar entre si
    def escolher_grupo():
        
        # variavel para controlar o tempo, com o tempo atual
        old = ticks_us()
        # o grupo inicial é 0
        numero = 0
        
        # Enquanto não escolher ficará em loop
        while True:
            
            # Limpa telam e informa o usuário qual grupo está selecionado
            # e para apertar A para confirmar
            limpar_tela()
            escrever_tela("Escolha o grupo", 0, 0)
            escrever_tela(str(round(numero)), 0, 10)
            escrever_tela("A para confirmar", 0, 20)
            mostrar_tela()

            # Caso o botão A for pressionado, o grupo atualmente selecionado
            # é escolhido e é retornado
            if botao_A_pressionado():
                # retorna o valor arredondado
                return round(numero)
            
            # Pega a quantida de tempo passado desde a ultima iteração 
            # e atualiza old com o tempo atual
            delta,old = tempo_de_jogo(old)
            # Pega o valor do joystick em X
            jx = joystick_x()
            # Os 2 ifs limitam numero para apenas ter valor entre 0 e 255
            if jx > 0 and numero <= 255:
                # v = v0 + at
                numero = numero + 1/250000*delta
            if jx < 0 and numero >= 0:
                # v = v0 + at
                numero = numero - 1/250000*delta

    # Essa função manda uma mensagem simples, apenas um [1]
    # para checar se a outra placa já está pronta
    def mandar_pronto():
        apagar_leds()
        limpar_tela()
        escrever_tela('Aguardando',0,0)
        escrever_tela('Inimigo',0,10)
        mostrar_tela()

        enviar_via_wifi([1])
        esperar_receber()

    # Essa função finaliza o jogo de corretamentes
    def finalizar_jogo():
        # Primeiro a BitDog dorme por 2s
        dormir(2)
        # Desliga o WiFi
        desligar_wifi()
        # Limpa a tela e indica o jogador para reiniciar a BitDog
        limpar_tela()
        escrever_tela('Reinicie',0,0)
        escrever_tela('para jogar',0,20)
        escrever_tela('novamente',0,30)
        mostrar_tela()
        # Apaga a matriz de leds
        apagar_leds()

    # Primeiramente desliga-se o WiFi
    desligar_wifi()
    # Então o jogador escolherá entre time A e B
    # Dependendo da escolha ele agirá como servidor ou cliente
    # O servidor sempre ataca primeiro
    is_servidor = escolher_lado()
    # Para que se possa ocorrer varias batalhas simulatanementes
    # Isso é varias duplas jogando
    # Precisa definir um grupo de 0 à 255 para não ter conflito
    numero = escolher_grupo()
    # Aqui o Wifi é inicializado, podendo ser como servidor ou cliente
    definir_servidor_ou_cliente(numero, is_servidor)
    # Fase onde jogador posicionará os navios
    matriz_navios = fase_posicionamento()
    # A função abaixo faz com que o jogo só comece qnd ambos estão prontos
    mandar_pronto()
    # Aqui o jogo em si começa
    fase_batalha(is_servidor)
    # Finaliza o jogo corretamente
    finalizar_jogo()
except Exception as e:
    # Se der algum erro, salva o erro em error.log
    import sys
    with open('error.log', 'w') as f:
        sys.print_exception(e, f)
    # Printa o erro no serial
    print(e)
    # Apaga os Leds
    apagar_leds()
    limpar_tela()
    # Indica ao jogador que ocorreu um erro
    escrever_tela('Ocorreu',0,0)
    escrever_tela('um erro',0,10)
    mostrar_tela()
