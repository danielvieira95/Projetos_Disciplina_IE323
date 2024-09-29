import time  # Importa a biblioteca time para funções de temporização
from machine import Pin, I2C  # Importa as funções para controle de pinos e comunicação I2C
import neopixel  # Importa a biblioteca para controlar a matriz de LEDs WS2812B
from tcs34725 import TCS34725  # Importa a classe para controlar o sensor de cor TCS34725
import ssd1306  # Importa a biblioteca para controlar o display OLED
from utime import sleep_ms as delay  # Renomeia a função de atraso para simplificação

# Configuração do display OLED via I2C
i2c_oled = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)  # Configura a comunicação I2C para o display
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)  # Inicializa o display OLED com tamanho 128x64

# Configuração da matriz de LEDs WS2812B (Neopixel)
NUM_LEDS = 25  # Número de LEDs na matriz (5x5)
LED_PIN = 7  # Pino GPIO onde a matriz de LEDs está conectada
leds = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)  # Inicializa a matriz de LEDs

# Configuração do sensor de cor TCS34725
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Configura a comunicação I2C para o sensor de cor
sensor = TCS34725(i2c)  # Inicializa o sensor de cor TCS34725

# Valores calibrados para identificação da cor BRANCO
calibR = 0.36  # Valor de referência para a cor vermelha no branco
calibG = 0.37  # Valor de referência para a cor verde no branco
calibB = 0.26  # Valor de referência para a cor azul no branco
margem = 0.02  # Margem de erro para identificação de cores

# Ativando o sensor de cor
sensor.active(True)  # Ativa o sensor de cor TCS34725
sensor.integration_time(50)  # Define o tempo de integração (quanto tempo o sensor capta luz)
sensor.gain(4)  # Define o ganho do sensor (aumenta a sensibilidade para luz fraca)

delay(500)  # Pequeno atraso para garantir que o sensor esteja pronto

# Dicionário para as cores predefinidas
cores_predefinidas = {
    'Branco': (25, 25, 25),  # Branco total
    'Vermelho': (25, 0, 0),  # Vermelho
    'Verde': (0, 25, 0),  # Verde
    'Azul': (0, 0, 25),  # Azul
    'Ciano': (0, 25, 25),  # Ciano (mistura de azul e verde)
    'Magenta': (25, 0, 25),  # Magenta (mistura de vermelho e azul)
    'Amarelo': (25, 25, 0),  # Amarelo (mistura de vermelho e verde)
    'Preto': (0, 0, 0)  # Preto (ausência de luz)
}

def ler_sensor_cor():
    """Função para capturar os valores de cor do sensor de cor TCS34725"""
    leitura = sensor.read(True)  # Faz a leitura do sensor
    r = leitura[0]  # Valor da cor vermelha
    g = leitura[1]  # Valor da cor verde
    b = leitura[2]  # Valor da cor azul
    c = leitura[3]  # Valor da claridade (intensidade total da luz)
    return r, g, b, c  # Retorna os valores lidos

def captura_cor(r, g, b, c):
    """Processa os valores RGB e retorna a cor aproximada"""
    if c:  # Verifica se há luz suficiente para identificar a cor
        rp = r / c  # Normaliza o valor de vermelho pela claridade
        gp = g / c  # Normaliza o valor de verde pela claridade
        bp = b / c  # Normaliza o valor de azul pela claridade
        
        cor = "NA"  # Inicializa a variável da cor com "não identificada"
        
        # Define a cor com base nos valores normalizados e na calibração
        if c < 400:  
            cor = "Preto"
        elif rp <= (calibR + margem) and gp <= (calibG + margem) and bp <= (calibB + margem):
            cor = "Branco"
        elif rp > (calibR + margem) and gp <= (calibG + margem) and (bp + 0.06) > (calibB + margem):
            cor = "Magenta"
        elif rp > (calibR + margem) and gp <= (calibG + margem) and bp <= (calibB + margem):
            cor = "Vermelho"
        elif rp <= (calibR + margem) and gp > (calibG + margem) and bp <= (calibB + margem):
            cor = "Verde"
        elif rp <= (calibR + margem) and gp <= (calibG + margem) and bp > (calibB + margem):
            cor = "Azul"
        elif rp <= (calibR + margem) and gp > (calibG + margem) and bp > (calibB + margem):
            cor = "Ciano"
        elif rp > (calibR + margem) and gp > (calibG + margem) and bp <= (calibB + margem):
            cor = "Amarelo"
        
        delay(250)  # Pequeno atraso para estabilidade
    else:
        delay(2000)  # Se a claridade for insuficiente, espera mais tempo
    return cor  # Retorna a cor identificada

def ajustar_matriz_leds(r, g, b):
    """Ajusta a cor da matriz de LEDs WS2812B com os valores RGB fornecidos"""
    for i in range(NUM_LEDS):
        leds[i] = (r, g, b)  # Define a cor de cada LED da matriz
    leds.write()  # Atualiza a matriz de LEDs com as novas cores

def exibir_cor_oled(r, g, b):
    """Exibe os valores RGB no display OLED"""
    oled.fill(0)  # Limpa o display
    oled.text('R: {}'.format(r), 0, 0)  # Mostra o valor de vermelho
    oled.text('G: {}'.format(g), 0, 10)  # Mostra o valor de verde
    oled.text('B: {}'.format(b), 0, 20)  # Mostra o valor de azul
    oled.show()  # Atualiza o display com as informações

# Loop principal do programa
try:
    while True:
        r, g, b, c = ler_sensor_cor()  # Lê os valores do sensor de cor
        cor = captura_cor(r, g, b, c)  # Processa e identifica a cor
        
        if cor in cores_predefinidas:
            r_esperado, g_esperado, b_esperado = cores_predefinidas[cor]  # Obtém os valores RGB da cor identificada
            ajustar_matriz_leds(r_esperado, g_esperado, b_esperado)  # Ajusta a cor na matriz de LEDs
            exibir_cor_oled(r_esperado, g_esperado, b_esperado)  # Exibe os valores RGB no display OLED
        delay(500)  # Adicionando um pequeno atraso
except KeyboardInterrupt:
    oled.fill(0)  # Limpa o display
    oled.show()  # Atualiza o display com as informações
    for i in range(NUM_LEDS):
        leds[i] = (0, 0, 0)  # Define a cor de cada LED da matriz
    leds.write()  # Atualiza a matriz de LEDs com as novas cores
    print("Execução interrompida manualmente.")

