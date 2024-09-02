from machine import Pin, SoftI2C # Pin:Configurar entrada/saida digitais
#SoftI2C:Criar interface I2C em pinos específicos do microcont.
from ssd1306 import SSD1306_I2C  # Controlar displays OLED
import machine, neopixel  # machine: Controlar diretamente o hardware microcont./         #NeoPixel -> Controlar LEDS RGB 
import time # funções relacionadas ao tempo


i2c = SoftI2C(scl=Pin(15), sda=Pin(14))  # pinos que serão utilizados no i2c
oled = SSD1306_I2C(128, 64, i2c) # controla display OLED 
oled.fill(0)  # Limpa o display

np = neopixel.NeoPixel(machine.Pin(7), 25)  # controlar os leds/ Matriz de Led conectada  # no pino 7/25 - Número de Leds da matriz

it=1 # intensidade do LED, pode variar de 1 a 255

# definir cores para os LEDs
BLU = (0, 0, 1*it) # BLUE
GRE = (0, 1*it, 0) # GREEN
RED = (1*it, 0, 0)  # RED
YEL = (1*it, 1*it, 0) # YELLOW
MAGE = (1*it, 0, 1*it) # MANGENTA
CYA = (0, 1*it, 1*it) # CYAN
WHI = (1*it, 1*it, 1*it) # WHIE
BLA = (0, 0, 0) # BLACK

# all_off -> significa que a matriz estará toda apagada 
all_off = [
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA]
    ]
# Colocamos uma cor diferente para cada átomo para facilitar a visualização
atomo1 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

atomo2 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, GRE, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

atomo3 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, YEL, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

atomo4 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, MAGE, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]
# no car1/car2 está o padrão da matriz de Led que queremos para mostrar a camada de #valência do carbono
car1 = [
    [RED, BLA, BLA, BLA, RED],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, YEL, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [RED, BLA, BLA, BLA, RED]
]

car2 = [
    [BLA, BLA, RED, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [RED, BLA, YEL, BLA, RED],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, RED, BLA, BLA]
]
# no o1/o2 está o padrão da matriz de Led que queremos para mostrar a camada de #valência do oxigênio
o1 = [
    [RED, BLA, BLA, BLA, RED],
    [BLA, BLA, BLA, BLA, BLA],
    [RED, BLA, YEL, BLA, RED],
    [BLA, BLA, BLA, BLA, BLA],
    [RED, BLA, BLA, BLA, RED]
]

o2 = [
    [BLA, BLA, RED, BLA, BLA],
    [RED, BLA, BLA, BLA, RED],
    [BLA, BLA, YEL, BLA, BLA],
    [RED, BLA, BLA, BLA, RED],
    [BLA, BLA, RED, BLA, BLA]
]
# no he1/he2/he3/he4 está o padrão da matriz de Led que queremos para mostrar a #camada de valência do hélio
he1 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, RED, BLA, BLA, BLA],
    [BLA, BLA, GRE, BLA, BLA],
    [BLA, BLA, BLA, RED, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

he2 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, RED, BLA, BLA],
    [BLA, BLA, GRE, BLA, BLA],
    [BLA, BLA, RED, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

he3 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, RED, BLA],
    [BLA, BLA, GRE, BLA, BLA],
    [BLA, RED, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

he4 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, RED, GRE, RED, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]
# no h1/h2/h3/h4/h5/h6/h7/h8 está o padrão da matriz de Led que queremos para mostrar a #camada de valência do hidrogênio
h1 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, RED, BLA, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

h2 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, RED, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

h3 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, RED, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

h4 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, RED, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]


h5 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, BLA, RED, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

h6 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, RED, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

h7 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, RED, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

h8 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLU, RED, BLA],
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
    oled.text("Quimica", 36, 36)
    oled.show()
    oled.fill(0)

def case2():
    oled.text("Vamos  ", 36, 12)
    oled.text("estudar ", 36, 24)
    oled.text("quimica!", 36, 36)
    oled.show()
    oled.fill(0)
    
def case3():
    oled.text("Vamos ver os", 24, 12)
    oled.text("atomos e suas ", 24, 24)
    oled.text("camadas de ", 24, 36)
    oled.text("valencia", 24, 46)
    oled.show()
    oled.fill(0)

def case4():
    oled.text("Exemplo 1", 24, 36)
    oled.show()
    oled.fill(0)
  
def case5():
    oled.text("Atomo de  ", 24, 12)
    oled.text("Hidrogenio ", 24, 24)
    oled.text("Simbolo:H", 24, 36)
    oled.show()
    oled.fill(0)

def case6():
    led_matrix(all_off)
    oled.text("1 eletron  ", 24, 12)
    oled.text("na camada ", 24, 24)
    oled.text("de valencia", 24, 36)
    oled.show()
    oled.fill(0)

# Essa função (case7) define como queremos que a matriz de led se comporte
def case7():
    led_matrix(atomo1)
    led_matrix(h1)
    time.sleep_ms(15)
    led_matrix(h2)
    time.sleep_ms(15)
    led_matrix(h3)
    time.sleep_ms(15)
    led_matrix(h4)
    time.sleep_ms(15)
    led_matrix(h5)
    time.sleep_ms(15)
    led_matrix(h6)
    time.sleep_ms(15)
    led_matrix(h7)
    time.sleep_ms(15)
    led_matrix(h8)
    time.sleep_ms(15)
    
def case8():
    led_matrix(all_off)
    oled.text("Exemplo 2", 24, 36)
    oled.show()
    oled.fill(0)

def case9():
    oled.text("Atomo de  ", 24, 12)
    oled.text("Helio ", 24, 24)
    oled.text("Simbolo:He", 24, 36) 
    oled.show()
    oled.fill(0)

def case10():
    led_matrix(all_off)
    oled.text("2 eletrons  ", 24, 12)
    oled.text("na camada ", 24, 24)
    oled.text("de valencia", 24, 36)
    oled.show()
    oled.fill(0)
  
def case11():
    led_matrix(atomo2)
    led_matrix(he1)
    time.sleep_ms(25)
    led_matrix(he2)
    time.sleep_ms(25)
    led_matrix(he3)
    time.sleep_ms(25)
    led_matrix(he4)
    time.sleep_ms(25)

def case12():
    led_matrix(all_off)
    oled.text("Exemplo 3", 24, 36)
    oled.show()
    oled.fill(0)
    
def case13():
    oled.text("Atomo de  ", 24, 12)
    oled.text("Carbono ", 24, 24)
    oled.text("Simobolo:C", 24, 36)
    oled.show()
    oled.fill(0)
    
def case14():
    led_matrix(all_off)
    oled.text("4 eletrons  ", 24, 12)
    oled.text("na camada ", 24, 24)
    oled.text("de valencia", 24, 36)
    oled.show()
    oled.fill(0)
    
def case15():
    led_matrix(atomo3)
    led_matrix(car1)
    time.sleep_ms(80)
    led_matrix(car2)
    time.sleep_ms(80)
    
def case16():
    led_matrix(all_off)
    oled.text("Exemplo 4", 24, 36)
    oled.show()
    oled.fill(0)

def case17():
    oled.text("Atomo de  ", 24, 12)
    oled.text("Oxigenio ", 24, 24)
    oled.text("Simbolo:O", 24, 36)
    oled.show()
    oled.fill(0)

def case18():
    led_matrix(all_off)
    oled.text("6 eletrons  ", 24, 12)
    oled.text("na camada ", 24, 24)
    oled.text("de valencia", 24, 36)
    oled.show()
    oled.fill(0)
    
def case19():
    led_matrix(atomo4)
    led_matrix(o1)
    time.sleep_ms(80)
    led_matrix(o2)
    time.sleep_ms(80)
    
def case20():
    led_matrix(all_off)
    oled.text("FIM", 36, 36)
    oled.show()
    oled.fill(0)

def switch_case_dicionario (value): # Essa função define quais as funções que serão #chamadas 
    
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
        20: case20
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
        if count > 20:
            count = 20

    switch_case_dicionario(count) # chama a função switch_case com o valor atual de #count
    time.sleep_ms(140) #delay 