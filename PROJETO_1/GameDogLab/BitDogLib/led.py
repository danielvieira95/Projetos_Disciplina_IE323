# Importação das Bibliotecas: Importa as bibliotecas Pin e neopixel necessárias para controlar os LEDs.
# lib
from machine import Pin
import neopixel

# Número de LEDs na sua matriz 5x5
# lib / aula
NUM_LEDS = 25
ROW_SIZE = 5
COL_SIZE = 5

# Inicializar a matriz de NeoPixels no GPIO7
# A Raspberry Pi Pico está conectada à matriz de NeoPixels no pino GPIO7

# lib
LED_MAP = [[04, 03, 02, 01, 00],
           [05, 06, 07, 08, 09],
           [14, 13, 12, 11, 10],
           [15, 16, 17, 18, 19],
           [24, 23, 22, 21, 20]]

np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

def ligar_led(x, y, cor):
    '''
    liga um led na posição e cor especificada
    '''
    if 0 > x >= ROW_SIZE:
        print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
        return
    if 0 > y >= COL_SIZE:
        print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
        return

    indice = LED_MAP[y][x]
    # Verifica se o índice está dentro do intervalo permitido
    np[indice] = cor  # Define a cor do LED específico
    np.write()  # Atualiza a matriz de LEDs para aplicar a mudança

def apagar_led(x, y):
    '''
    apaga um led na posição especificada
    '''
    if 0 > x  and x >= ROW_SIZE:
        print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
        return
    if 0 > y and y >= COL_SIZE:
        print("Índice x fora do intervalo. Por favor, escolha um índice de 0 a", NUM_LEDS - 1)
        return

    indice = LED_MAP[y][x]
    np[indice] = (0,0,0)  # Define a cor do LED específico
    np.write()  # Atualiza a matriz de LEDs para aplicar a mudança

def apagar_leds():
    '''
    apaga todos os leds
    '''
    i = 0
    while i < 5:
        j = 0
        while j < 5:
            apagar_led(i,j)
            j = j + 1
        i = i + 1

