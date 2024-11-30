# Importação das bibliotecas necessárias para manipular hardware e funcionalidades adicionais
import machine
import utime
import neopixel
import ssd1306  # Biblioteca para controle de displays OLED
from ST7735 import TFT, TFTColor  # Biblioteca para displays TFT ST7735
from sysfont import sysfont  # Fonte básica para textos no display TFT
from machine import SPI, Pin  # Comunicação SPI e manipulação de GPIOs
import time
import math
# Configuração da interface SPI para o display TFT
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
tft = TFT(spi, 16, 20, 17)  # Inicializa TFT com SPI e pinos de controle (DC, RST, CS)
tft.initr()  # Inicializa o display em modo padrão
tft.rgb(True)  # Define o modo de cores RGB
tft.fill(TFT.BLACK)  # Preenche a tela com a cor preta
# Configuração de um pino GPIO para controlar o backlight do display
pino = Pin(10, Pin.OUT)  # Define GPIO10 como saída
pino.value(1)  # Ativa o backlight ao definir o pino em nível alto

# Parâmetros de hardware para LED, joystick e botões
NUM_LEDS = 25  # Número de LEDs na matriz 5x5
PIN_LED = 7  # Pino GPIO para controle de LEDs WS2812B
VRx_PIN = 27  # Pino GPIO para o eixo X do joystick
VRy_PIN = 26  # Pino GPIO para o eixo Y do joystick
SW_PIN = 22  # Pino GPIO para o botão do joystick
botao_PIN = 5  # Pino GPIO para o Botão A
BOTAO_B_PIN = 6  # Pino GPIO para o Botão B
I2C_SDA_PIN = 14  # Pino GPIO para linha SDA do display OLED
I2C_SCL_PIN = 15  # Pino GPIO para linha SCL do display OLED
OLED_WIDTH = 128  # Largura do display OLED em pixels
OLED_HEIGHT = 64  # Altura do display OLED em pixels



# Variáveis de controle do jogo
jogada = 0  # Contador de jogadas no nível atual
jogadas_total = 0  # Contador total de jogadas em todos os níveis
nr_jogadas = 20  # Número máximo de jogadas por nível
leds_apagados = False  # Estado dos LEDs (apagados ou não)
nivel = 0  # Nível atual do jogo
final_jogo = True  # Controle do estado final do jogo

# Inicialização do controle de LEDs WS2812B
matriz_led = neopixel.NeoPixel(machine.Pin(PIN_LED), NUM_LEDS)

# Configuração de pinos do joystick como entradas analógicas
VRx = machine.ADC(machine.Pin(VRx_PIN))
VRy = machine.ADC(machine.Pin(VRy_PIN))

# Configuração de botões como entradas digitais com resistores pull-up internos
botao = machine.Pin(SW_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
botao_a = machine.Pin(botao_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
botao_b = machine.Pin(BOTAO_B_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Configuração da interface I2C para o display OLED
i2c = machine.SoftI2C(sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)
oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=0x3C)  # Inicializa o display OLED com endereço padrão

# Sensibilidade do movimento do joystick (ajustável)
SENSIBILIDADE = 2000  # Defina um valor de sensibilidade para detectar movimentos

# Padrão zig-zag com LEDs amarelos e apagados
padrao_matriz_leds_invertida = [ # nivel 1
    [1, 1, 0, 1, 1],  # Linha 1
    [1, 0, 1, 0, 1],  # Linha 2
    [0, 1, 1, 1, 0],  # Linha 3
    [1, 0, 1, 0, 1],  # Linha 4
    [1, 1, 0, 1, 1],  # Linha 5
],[ # nivel 2
    [0, 1, 0, 1, 0],  # Linha 1
    [1, 1, 0, 1, 1],  # Linha 2
    [0, 1, 0, 1, 0],  # Linha 3
    [1, 0, 1, 0, 1],  # Linha 4
    [1, 0, 1, 0, 1],  # Linha 5
],[ # nivel 3
    [1, 0, 0, 0, 1],  # Linha 1
    [1, 1, 0, 1, 1],  # Linha 2
    [0, 0, 1, 0, 0],  # Linha 3
    [1, 0, 1, 0, 0],  # Linha 4
    [1, 0, 1, 1, 0],  # Linha 5
],[ # nivel 4
    [1, 1, 0, 1, 1],  # Linha 1
    [0, 0, 0, 0, 0],  # Linha 2
    [1, 1, 0, 1, 1],  # Linha 3
    [0, 0, 0, 0, 1],  # Linha 4
    [1, 1, 0, 0, 0],  # Linha 5
], [ # nivel 5
    [1, 1, 1, 1, 1],  # Linha 1
    [1, 0, 0, 0, 1],  # Linha 2
    [1, 0, 0, 0, 1],  # Linha 3
    [1, 0, 0, 0, 1],  # Linha 4
    [1, 1, 1, 1, 1],  # Linha 5
], [ # nivel 6
    [0, 0, 1, 1, 1],  # Linha 1
    [0, 0, 0, 1, 1],  # Linha 2
    [1, 0, 0, 0, 1],  # Linha 3
    [1, 1, 0, 0, 0],  # Linha 4
    [1, 1, 1, 0, 0],  # Linha 5
], [ # nivel 7
    [1, 1, 1, 1, 1],  # Linha 1
    [1, 0, 1, 0, 1],  # Linha 2
    [1, 1, 1, 1, 1],  # Linha 3
    [1, 0, 1, 0, 1],  # Linha 4
    [1, 1, 1, 1, 1],  # Linha 5
], [ # nivel 8
    [1, 1, 1, 1, 1],  # Linha 1
    [1, 1, 1, 1, 1],  # Linha 2
    [1, 1, 1, 1, 1],  # Linha 3
    [1, 1, 1, 1, 1],  # Linha 4
    [1, 1, 1, 1, 1],  # Linha 5
], [ # nivel 9
    [1, 1, 1, 1, 1],  # Linha 1
    [0, 1, 1, 1, 0],  # Linha 2
    [0, 0, 1, 0, 0],  # Linha 3
    [0, 1, 1, 1, 0],  # Linha 4
    [1, 1, 1, 1, 1],  # Linha 5
], [ # nivel 10
    [1, 0, 0, 0, 1],  # Linha 1
    [0, 1, 0, 1, 0],  # Linha 2
    [0, 0, 1, 0, 0],  # Linha 3
    [0, 1, 0, 1, 0],  # Linha 4
    [1, 0, 0, 0, 1],  # Linha 5
]

# Invertendo cada matriz 5x5 horizontalmente que está dentro da matriz padrao_matriz_leds_invertida
padrao_matriz_leds = [
    [linha[::-1] for linha in nivel] for nivel in padrao_matriz_leds_invertida
]

# Função que copia profundamente uma matriz, criando uma nova matriz para cada sub-matriz
def copia_profunda(matriz):
    if isinstance(matriz, list):  # Verifica se o elemento é uma lista
        return [copia_profunda(elemento) for elemento in matriz]  # Chamada recursiva para cópia profunda
    return matriz  # Retorna o elemento se não for uma lista

# Copiando profundamente a matriz padrao_matriz_leds, garantindo uma nova estrutura independente
matriz = copia_profunda(padrao_matriz_leds)

# Função para limpar a matriz de LEDs (desligar todos os LEDs)
def limpar_matriz_led():
    for i in range(NUM_LEDS):  # Itera por todos os LEDs
        matriz_led[i] = (0, 0, 0)  # Define o LED como apagado
    matriz_led.write()  # Atualiza o estado da matriz de LEDs
    
# Função que converte uma posição linear em uma matriz 5x5 para um formato zig-zag
def converter_zigzag(posicao):
    linha = traz_linha(posicao)  # Determina a linha da posição
    coluna = traz_coluna(posicao)  # Determina a coluna da posição
    
    # Se a linha for ímpar, inverte a ordem das colunas (zig-zag)
    if linha % 2 == 0:
        return posicao
    else:
        return linha * 5 + (4 - coluna)

# Função para aplicar o padrão de LEDs amarelos na matriz
def aplicar_padrao_amarelo():
    for linha in range(5):  # Itera por cada linha
        for coluna in range(5):  # Itera por cada coluna
            posicao = converter_zigzag(linha * 5 + coluna)  # Converte posição linear para zig-zag
            if padrao_matriz_leds[nivel][linha][coluna] == 1:  # Se o padrão indicar LED ligado
                matriz_led[posicao] = (2, 2, 0)  # Define a cor amarela
            else:
                matriz_led[posicao] = (0, 0, 0)  # Desliga o LED
    matriz_led.write()  # Atualiza a matriz de LEDs

# Função para obter a linha correspondente a uma posição em uma matriz 5x5
def traz_linha(posicao):
    linha = posicao // 5  # Divide a posição linear por 5 para obter a linha
    return linha

# Função para obter a coluna correspondente a uma posição em uma matriz 5x5
def traz_coluna(posicao):
    coluna = posicao % 5  # Obtém o resto da divisão para determinar a coluna
    return coluna

# Função para alternar o estado de um LED entre ligado e desligado na posição fornecida
def mudanca_estado(posicao):
    linha = traz_linha(posicao)  # Obtém a linha da posição
    coluna = traz_coluna(posicao)  # Obtém a coluna da posição
    # Alterna entre 1 (ligado) e 0 (desligado)
    if padrao_matriz_leds[nivel][linha][coluna] == 1:
        padrao_matriz_leds[nivel][linha][coluna] = 0
    elif padrao_matriz_leds[nivel][linha][coluna] == 0:
        padrao_matriz_leds[nivel][linha][coluna] = 1

# Função para alternar o estado do LED atual e dos LEDs adjacentes
def alternar_leds(posicao):  
    posicao_cima = posicao - 5  # Determina a posição acima
    posicao_baixo = posicao + 5  # Determina a posição abaixo
    posicao_direita = posicao - 1  # Determina a posição à esquerda
    posicao_esquerda = posicao + 1  # Determina a posição à direita
    mudanca_estado(posicao)  # Alterna o estado do LED atual
    
    # Verifica os limites da matriz antes de alterar os LEDs adjacentes
    if not (posicao == 4 or posicao == 3 or posicao == 2 or posicao == 1 or posicao == 0):
        mudanca_estado(posicao_cima)  # Alterna o LED acima
    
    if not (posicao == 24 or posicao == 23 or posicao == 22 or posicao == 21 or posicao == 20):
        mudanca_estado(posicao_baixo)  # Alterna o LED abaixo
    
    if not (posicao == 4 or posicao == 9 or posicao == 14 or posicao == 19 or posicao == 24):
        mudanca_estado(posicao_esquerda)  # Alterna o LED à esquerda
    
    if not (posicao == 0 or posicao == 5 or posicao == 10 or posicao == 15 or posicao == 20):
        mudanca_estado(posicao_direita)  # Alterna o LED à direita
    
    # Exibe as posições afetadas no console
    #print(f"posicao atual: {posicao}; posicao cima: {posicao_cima}; posicao baixo: {posicao_baixo}; posicao direita: {posicao_direita}; posicao esquerda: {posicao_esquerda}")
    

# Função para acender o LED vermelho em uma posição específica
def acender_led_vermelho(posicao):   
    matriz_led[converter_zigzag(posicao)] = (2, 0, 0)  # Define a cor vermelha
    matriz_led.write()  # Atualiza a matriz de LEDs

# Função para verificar se todos os LEDs amarelos estão apagados
def verificar_leds_apagados(padrao_matriz_leds):
    # Verifica se todos os valores da matriz são zero
    todos_zeros = all(valor == 0 for linha in padrao_matriz_leds for valor in linha)
    return todos_zeros

# Função para apresentar informações no início do jogo no display OLED
def inicio_jogo():
    oled.fill(0)  # Limpa a tela
    oled.text("Bem vindo", 0, 0)  # Exibe mensagem de boas-vindas
    oled.text("O Jogo comecou", 0, 10)  # Indica início do jogo
    oled.text("Faz a jogada", 0, 20)  # Solicita uma jogada
    oled.show()
    utime.sleep(0.1)  # Aguarda um breve momento

inicio_jogo()  # Chamada para exibir mensagem inicial

# Função para apresentar informações das jogadas no Display OLED
def dados_jogo():
    global jogada  # Usa a variável global 'jogada' para acompanhar o progresso
    oled.fill(0)  # Limpa o display OLED
    oled.text(f"Nr jogadas: {nr_jogadas}", 0, 0)  # Exibe o número total de jogadas
    oled.text(f"Jogada: {jogada}", 0, 10)  # Exibe a jogada atual
    oled.text(f"Nivel: {nivel + 1}", 0, 30)  # Exibe o nível atual (incrementado para exibição)
    oled.show()  # Atualiza o display OLED para mostrar as informações

# Função para apresentar uma imagem no Display LCD TFT
def imagem(nome):
    f = open(f'{nome}.bmp', 'rb')  # Abre o arquivo BMP em modo leitura binária
    if f.read(2) == b'BM':  # Verifica o cabeçalho do arquivo (deve começar com "BM")
        dummy = f.read(8)  # Ignora 8 bytes (tamanho do arquivo e criador)
        offset = int.from_bytes(f.read(4), 'little')  # Lê o offset para os dados de imagem
        hdrsize = int.from_bytes(f.read(4), 'little')  # Lê o tamanho do cabeçalho
        width = int.from_bytes(f.read(4), 'little')  # Lê a largura da imagem
        height = int.from_bytes(f.read(4), 'little')  # Lê a altura da imagem
        if int.from_bytes(f.read(2), 'little') == 1:  # Verifica se o número de planos é 1
            depth = int.from_bytes(f.read(2), 'little')  # Lê a profundidade da cor (bits por pixel)
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:  # Verifica profundidade de 24 bits e sem compressão
                print("Image size:", width, "x", height)  # Exibe o tamanho da imagem
                rowsize = (width * 3 + 3) & ~3  # Calcula o tamanho de cada linha (alinhado a 4 bytes)
                if height < 0:
                    height = -height  # Corrige altura negativa (origem na parte inferior)
                    flip = False  # Sem flip vertical
                else:
                    flip = True  # Flip vertical
                w, h = width, height
                if w > 128: w = 128  # Limita a largura máxima a 128 pixels
                if h > 160: h = 160  # Limita a altura máxima a 160 pixels
                tft._setwindowloc((0, 0), (w, h))  # Configura a janela de exibição no TFT
                
                for row in range(h):  # Para cada linha da imagem
                    if flip:
                        pos = offset + row * rowsize  # Posição da linha com flip
                    else:
                        pos = offset + (height - 1 - row) * rowsize  # Posição da linha sem flip
                    
                    if f.tell() != pos:  # Move o cursor para a posição correta
                        f.seek(pos)
                    
                    line = f.read(rowsize)[:width * 3]  # Lê os dados da linha (até a largura necessária)
                    
                    for col in range(w - 1, -1, -1):  # Processa pixels da direita para a esquerda
                        bgr = line[col * 3:(col + 1) * 3]  # Obtém os componentes BGR
                        tft._pushcolor(TFTColor(bgr[2], bgr[1], bgr[0]))  # Converte para RGB e envia ao TFT

    spi.deinit()  # Finaliza a comunicação SPI

# Função principal
def main():
    # Exibir uma imagem inicial no OLED
    imagem("Inicio")
    
    # Variáveis globais para controlar o estado do jogo
    global jogada, leds_apagados, nivel, jogadas_total, padrao_matriz_leds, padrao_matriz_leds_invertida, final_jogo
    
    # Configuração inicial da posição do LED na matriz
    posicao_atual = 12  # Começando na posição 12 (centro da matriz 5x5)
    posicao_anterior = posicao_atual  # Guardar posição anterior para atualizar corretamente
    
    # Limpar a matriz de LEDs antes de iniciar o jogo
    limpar_matriz_led()
    
    # Aplicar o padrão inicial de LEDs amarelos na matriz
    aplicar_padrao_amarelo()
    
    # Acender o LED vermelho na posição inicial
    acender_led_vermelho(posicao_atual)
    
    # Loop principal do jogo
    while True:
        # Verificar se o botão B foi pressionado para reiniciar o jogo
        if botao_b.value() == 0:
            limpar_matriz_led()
            oled.fill(0)
            oled.text("Reiniciando", 0, 0)
            oled.text("Faz a jogada", 0, 10)
            oled.show()
            utime.sleep(2)  # Pausa para reiniciar o jogo
            
            # Se o nível for maior que 9, reinicia o jogo completamente
            if nivel > 9:
                final_jogo = True
                nivel = 0
            
            # Resetar o estado do jogo
            posicao_atual = 12  # Posição inicial
            padrao_matriz_leds = copia_profunda(matriz)
            aplicar_padrao_amarelo()
            acender_led_vermelho(posicao_atual)
            jogada = 0
            leds_apagados = False
            
        
        # Controle do jogo após reiniciar ou começar um novo nível
        if final_jogo:
            # Ler valores dos eixos do joystick
            x_val = VRx.read_u16()
            y_val = VRy.read_u16()

            # Verificar movimentação no eixo X (esquerda/direita)
            if x_val < (32768 - SENSIBILIDADE):  # Movimento para a esquerda
                if posicao_atual % 5 > 0:  # Verificar limite da matriz
                    posicao_atual -= 1
            elif x_val > (32768 + SENSIBILIDADE):  # Movimento para a direita
                if posicao_atual % 5 < 4:
                    posicao_atual += 1
            
            # Verificar movimentação no eixo Y (cima/baixo)
            if y_val < (32768 - SENSIBILIDADE):  # Movimento para cima
                if posicao_atual >= 5:  # Verificar limite da matriz
                    posicao_atual -= 5
            elif y_val > (32768 + SENSIBILIDADE):  # Movimento para baixo
                if posicao_atual < 20:
                    posicao_atual += 5
            
            # Atualizar a matriz de LEDs apenas se a posição mudou
            if posicao_atual != posicao_anterior:
                linha_anterior = posicao_anterior // 5
                coluna_anterior = posicao_anterior % 5
                
                # Verificar o estado do LED na posição anterior e atualizá-lo
                if padrao_matriz_leds[nivel][linha_anterior][coluna_anterior] == 1:
                    matriz_led[converter_zigzag(posicao_anterior)] = (2, 2, 0)  # Amarelo
                else:
                    matriz_led[converter_zigzag(posicao_anterior)] = (0, 0, 0)  # Apagar LED
                matriz_led.write()

                posicao_anterior = posicao_atual
                acender_led_vermelho(posicao_atual)

        # Alternar LEDs na posição atual ao pressionar o botão
        if botao.value() == 0:
            utime.sleep(0.2)  # Debounce do botão
            alternar_leds(posicao_atual)  # Alternar estado dos LEDs
            aplicar_padrao_amarelo()  # Reaplicar o padrão amarelo
            acender_led_vermelho(posicao_atual)  # Reacender o LED vermelho
            jogada += 1
            leds_apagados = verificar_leds_apagados(padrao_matriz_leds[nivel])  # Verificar se todos os LEDs amarelos foram apagados
            dados_jogo()  # Atualizar informações do jogo
        
         # Verificar se o jogador venceu o nível
        if leds_apagados:
            limpar_matriz_led()
            oled.fill(0)
            oled.text(f"Nr jogadas: {nr_jogadas}", 0, 0)
            oled.text(f"Jogada: {jogada}", 0, 10)
            oled.text(f"Vitoria na mosca", 0, 20)
            nivel += 1  # Avançar para o próximo nível
            oled.text(f"Proximo Nivel {nivel + 1}", 0, 30)
            oled.text("Faz a jogada", 0, 40)
            oled.show()
            
            # Resetar variáveis para o próximo nível
            jogadas_total += jogada
            jogada = 0
            leds_apagados = False
            posicao_atual = 12
            if not (len(padrao_matriz_leds) - 1 < nivel):
                aplicar_padrao_amarelo()
                acender_led_vermelho(posicao_atual)
            utime.sleep(0.1)
            
            # Finalizar jogo se todos os níveis foram completados
            if (len(padrao_matriz_leds) - 1) < nivel:
                limpar_matriz_led()
                oled.fill(0)
                oled.text(f"Jogadas: {jogadas_total}", 0, 0)
                oled.text("Vitoria na mosca", 0, 10)
                oled.text("Conseguiste :)", 0, 20)
                oled.text("Finalizar o jogo", 0, 30)
                oled.text("Clique no botao", 0, 40)
                oled.text("direita para", 0, 50)
                oled.text("Reiniciar", 0, 60)
                oled.show()
                
                # Resetar variáveis globais
                jogadas_total = 0
                jogada = 0
                leds_apagados = False
                final_jogo = False

        # Exibir dicas após 5 jogadas se o jogador solicitar
        if jogada > 5:
            if botao_a.value() == 0:
                img = "Resp_" + str(nivel + 1)
                imagem(img)  # Exibir dica
                utime.sleep(3.4)
                imagem("Inicio")  # Retornar para a tela inicial
        
        # Aguardar para evitar múltiplos movimentos rápidos
        utime.sleep(0.2)

# Pausa antes de iniciar o jogo
utime.sleep(1.0)

# Executar a função principal
main()
