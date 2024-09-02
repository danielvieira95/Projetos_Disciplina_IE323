from machine import Pin, SoftI2C # Pin -> Configurar entrada/saida digitais
#SoftI2C-> criar interface I2C em pinos específicos do microcont.
from ssd1306 import SSD1306_I2C # Controlar displays OLED
import machine, neopixel # machine --> Controlar diretamente o hardware microcont./ #NeoPixel -> Controlar LEDS RGB 
import time # funções relacionadas ao tempo

i2c = SoftI2C(scl=Pin(15), sda=Pin(14)) # pinos que serão utilizados no i2c
oled = SSD1306_I2C(128, 64, i2c) # controla display OLED 
oled.fill(0)  # Limpa o display

np = neopixel.NeoPixel(machine.Pin(7), 25) # controlar os leds/ Matriz de Led conectada #no pino 7/25 - Número de Leds da matriz

it=1# intensidade do LED, pode variar de 1 a 255

# definir cores para os LEDs
BLU = (0, 0, 1*it)# BLUE
GRE = (0, 1*it, 0)# GREEN
RED = (1*it, 0, 0) # RED
YEL = (1*it, 1*it, 0)# YELLOW
MAGE = (1*it, 0, 1*it)# MANGENTA
CYA = (0, 1*it, 1*it)# CYAN
WHI = (1*it, 1*it, 1*it)# WHIE
BLA = (0, 0, 0)# BLACK

# all_off -> significa que a matriz estará toda apagada 
all_off = [
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA]
    ]
# Definindo como queremos que a matriz de led se comporte em cada situação
quadrado1 = [
        [BLU, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA]
    ]

quadrado2 = [
    [BLU, BLU, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLU, BLU],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

quadrado3 = [
    [BLU, BLU, BLU, BLA, BLA],
    [BLA, BLA, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

quadrado4 = [
    [BLU, BLU, BLU, BLU, BLA],
    [BLA, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLA],
    [BLA, BLU, BLU, BLU, BLU],
    [BLA, BLA, BLA, BLA, BLA]
]

quadrado5 = [
    [BLU, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLU]
]

retangulo1 = [
    [BLU, BLU, BLU, BLU, BLA],
    [BLA, BLU, BLU, BLU, BLU],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]


retangulo2 = [
    [BLU, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLU],
    [BLU, BLU, BLU, BLU, BLU],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

#configuração do botão
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

def led_matrix(pattern): # definindo uma função para a matriz de led
    
    inverted_matrix = pattern[::-1] # Inverter a matriz
    
    # Exibir a matriz invertida nos LEDs
    for i in range(5):
        for j in range(5):
            np[i * 5 + j] = inverted_matrix[i][j]
    
    np.write() # envia os dados para os leds
    
led_matrix(all_off) # função chamada para começar com a matriz apagada

# Definindo as funções para aparecer a parte escrita no OLED e como a matriz RGB vai se #comportar
# comando oled.show é para mostrar no oled a escrita
# comando oled.fill é para apagar o oled depois
def case0():
    
    oled.text("Pressione A  ", 12, 12)
    oled.text("para ", 40, 24)
    oled.text("voltar", 36, 36)
    oled.show()
    oled.fill(0)
  
def case1():
    
    oled.text("Projeto 1 - ", 12, 12)
    oled.text("BitDogLab", 24, 24)
    oled.text("Matematica", 36, 36)
    oled.show()
    oled.fill(0)

def case2():
    oled.text("Vamos comecar  ", 12, 12)
    oled.text("calculando ", 24, 24)
    oled.text("a area do", 24, 36)
    oled.text("quadrado!", 24, 46)
    oled.show()
    oled.fill(0)

def case3():
    
    oled.text("Como calcular  ", 24, 12)
    oled.text("a area do ", 24, 24)
    oled.text("quadrado?", 24, 36)
    oled.show()
    oled.fill(0)
    
def case4():
    oled.text("Mutiplicar  ", 24, 24)
    oled.text("a x b ", 24, 36)
    oled.show()
    oled.fill(0)

def case5():
    
    oled.rect(50, 25, 24, 24, 1)  # Parâmetros: (x, y, largura, altura, cor)
    oled.text('a', 59, 15)  # Parâmetros: (texto, x, y)
    oled.text('b', 75, 33)  # Parâmetros: (texto, x, y)
    oled.show()
    oled.fill(0)

def case6():
    
    oled.text("Exercicios:", 24, 24)
    oled.show()
    oled.fill(0)
    led_matrix(all_off)

def case7():
    oled.text("Para saber a", 14, 12)
    oled.text("area basta", 14, 24)
    oled.text("contar os leds", 14, 36)
    oled.text("acessos", 14, 46)
    oled.show()
    oled.fill(0)

def case8():
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("quadrado 1x1?", 24, 36)
    oled.show()
    oled.fill(0)
    

def case9():

    oled.rect(55, 28, 12, 12, 1)  # Parâmetros: (x, y, largura, altura, cor)
    oled.text('1', 58, 20)  # Parâmetros: (texto, x, y)
    oled.text('1', 68, 30)  # Parâmetros: (texto, x, y)
    oled.show()
    oled.fill(0)
    led_matrix(quadrado1) # chama a função led_matrix com o valor quadrado1
    
def case10():
    led_matrix(all_off)
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("quadrado 2x2?", 24, 36)
    oled.show()
    oled.fill(0)

def case11():
    
    oled.rect(50, 25, 24, 24, 1)  # Parâmetros: (x, y, largura, altura, cor)
    oled.text('2', 59, 15)  # Parâmetros: (texto, x, y)
    oled.text('2', 75, 33)  # Parâmetros: (texto, x, y)
    oled.show()
    oled.fill(0)
    led_matrix(quadrado2)
    
def case12():
    led_matrix(all_off)
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("quadrado 3x3?", 24, 36)
    oled.show()
    oled.fill(0)
    
def case13():
    
    oled.rect(40, 20, 32, 32, 1)  # Parâmetros: (x, y, largura, altura, cor)
    oled.text('3', 54, 10)  # Parâmetros: (texto, x, y)
    oled.text('3', 73, 30)  # Parâmetros: (texto, x, y)
    oled.show()
    oled.fill(0)
    led_matrix(quadrado3)

def case14():
    led_matrix(all_off)
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("quadrado 4x4?", 24, 36)
    oled.show()
    oled.fill(0)

def case15():
    
    oled.rect(35, 18, 40, 40, 1)
    oled.text('4', 50, 8)
    oled.text('4', 78, 35)
    oled.show()
    oled.fill(0)
    led_matrix(quadrado4)

def case16():
    led_matrix(all_off)
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("quadrado 5x5?", 24, 36)
    oled.show()
    oled.fill(0)
    
def case17():
    
    oled.rect(30, 15, 45, 45, 1)
    oled.text('5', 50, 7)
    oled.text('5', 78, 34)
    oled.show()
    oled.fill(0)
    led_matrix(quadrado5)


def case18():
    led_matrix(all_off)
    oled.text("Agora vamos  ", 24, 12)
    oled.text("calcular ", 24, 24)
    oled.text("a area do", 24, 36)
    oled.text("retangulo!", 24, 46)
    oled.show()
    oled.fill(0)

def case19():
    oled.text("Como calcular  ", 24, 12)
    oled.text("a area do ", 24, 24)
    oled.text("retangulo?", 24, 36)
    oled.show()
    oled.fill(0)
    
def case20():
    
    oled.text("Mutiplicar  ", 24, 24)
    oled.text("a x b ", 36, 36)
    oled.show()
    oled.fill(0)

def case21():
    
    oled.rect(35, 18, 58, 29, 1)
    oled.text('a', 58, 8)
    oled.text('b', 98, 30)
    oled.show()
    oled.fill(0)


def case22():
    
    oled.text("Exercicios:", 24, 24)
    oled.show()
    oled.fill(0)
    led_matrix(all_off)

def case23():
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("retangulo 4x2?", 24, 36)
    oled.show()
    oled.fill(0)

def case24():    

    oled.rect(35, 18, 58, 29, 1)
    oled.text('4', 58, 8)
    oled.text('2', 98, 30)
    oled.show()
    oled.fill(0)
    led_matrix(retangulo1)

def case25():
    led_matrix(all_off)
    oled.text("Qual a area  ", 24, 12)
    oled.text("de um ", 24, 24)
    oled.text("retangulo 5x3?", 24, 36)
    oled.show()
    oled.fill(0)
    
def case26():
    oled.rect(30, 15, 68, 34, 1)
    oled.text('5', 63, 8)
    oled.text('3', 98, 30)
    oled.show()
    led_matrix(retangulo2)
    
def case27():
    led_matrix(all_off)
    oled.text("FIM", 36, 36)
    oled.show()
    oled.fill(0)
    
def switch_case_dicionario (value):# Essa função define quais as funções que serão #chamadas
    
    cases = {
        
        1: case1,
        2: case2,
        3: case3,
        4: case4,
        5: case5,
        6: case6,
        7: case7,
        8: case8,
        9: case9,
        10: case10,
        11: case11,
        12: case12,
        13: case13,
        14: case14,
        15: case15,
        16: case16,
        17: case17,
        18: case18,
        19: case19,
        20: case20,
        21: case21,
        22: case22,
        23: case23,
        24: case24,
        25: case25,
        26: case26,
        27: case27
        
        }
    
    return cases.get(value, case0)() # essa função é utilizada para procurar as cases na #função acima
    

count = 0 # define variável count

while(True): # inicia um loop --> controlar o botão 
    if button_a.value() == 0:
        count = count -1
        if count < 0:
            count = 0
        
    if button_b.value() == 0:
        count = count + 1
        if count > 27:
            count = 27

    switch_case_dicionario(count) # chama a função switch_case com o valor atual de #count
    time.sleep_ms(140) #delay 