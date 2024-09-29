# Importando bibliotecas 
from machine import Pin, SoftI2C # Pin:Configurar entrada/saida digitais
#SoftI2C:Criar interface I2C em pinos específicos do microcont.
from ssd1306 import SSD1306_I2C  # Controlar displays OLED
import machine, neopixel # machine: Controlar diretamente o hardware microcont./         #NeoPixel -> Controlar LEDS RGB 
import time  # funções relacionadas ao tempo

i2c = SoftI2C(scl=Pin(15), sda=Pin(14)) # pinos que serão utilizados no i2c
oled = SSD1306_I2C(128, 64, i2c)  # controla display OLED 
oled.fill(0)  # Limpa o display

np = neopixel.NeoPixel(machine.Pin(7), 25)  # controlar os leds/ Matriz de Led conectada  # no pino 7/25 - Número de Leds da matriz

it=10 #ajustar intensidade da matriz de led

# definir cores para os LEDs
BLU = (0, 0, 255*it) # BLUE
GRE = (0, 255*it, 0) # GREEN
RED = (255*it, 0, 0)  # RED
YEL = (255*it, 255*it, 0) # YELLOW
MAGE = (255*it, 0, 255*it) # MANGENTA
CYA = (0, 255*it, 255*it) # CYAN
WHI = (255*it, 255*it, 255*it) # WHITE
BLA = (0, 0, 0) # BLACK

# all_off -> significa que a matriz estará toda apagada 
all_off = [
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA],
        [BLA, BLA, BLA, BLA, BLA]
    ]

#atomo 1 oxigênio
atomo1 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLU, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]
#atomo 2 nitrogênio
atomo2 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, GRE, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

# atomo 3 Argonio
atomo3 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, WHI, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

#dioxido de carbono
atomo4 = [
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, RED, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA],
    [BLA, BLA, BLA, BLA, BLA]
]

# ar1 mostra a composição do ar padrão
ar1 = [
    [RED, GRE, GRE, GRE, BLA],
    [BLA, GRE, GRE, GRE, BLA],
    [BLA, BLU, BLU, BLU, BLA],
    [BLA, GRE, GRE, GRE, BLA],
    [BLA, GRE, GRE, GRE, WHI]
]

# ar2 mostra a composição do ar com poluição
ar2= [
    [RED, GRE, GRE, GRE, RED],
    [RED, GRE, GRE, GRE, RED],
    [RED, BLU, BLU, BLU, RED],
    [RED, GRE, GRE, GRE, RED],
    [RED, GRE, GRE, GRE, WHI]
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

    
led_matrix(all_off) 

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
    oled.text("Pressione B  ", 12, 12)
    oled.text("para ", 40, 24)
    oled.text("avancar", 36, 36)
    oled.show()
    oled.fill(0) 
    
def case2():
    oled.text("Projeto 2 - ", 12, 12)
    oled.text("BitDogLab", 24, 24)
    oled.show()
    oled.fill(0)

def case3():
    oled.text("Composicao  ", 24, 12)
    oled.text("do Ar ", 24, 24)
    oled.show()
    oled.fill(0)

def case4():
    oled.text("O Ar e composto", 7, 12)
    oled.text("pelos", 7, 24)
    oled.text("seguintes ", 7, 36)
    oled.text("elementos:", 7, 46)
    oled.show()
    oled.fill(0)

def case5():
    led_matrix(all_off)
    oled.text("21% O2 ", 24, 12)
    oled.text("78% N2 ", 24, 24)
    oled.text("1% Ar ", 24, 36)
    oled.text("0,03% CO2 ", 24, 46)
    oled.show()
    oled.fill(0)
  
def case6():
    led_matrix(ar1)
    
def case7():
    led_matrix(all_off)
    oled.text("Poluicao", 24, 12)
    oled.show()
    oled.fill(0)

def case8():
    led_matrix(all_off)
    oled.text("Com a poluicao", 12, 12)
    oled.text("temos um", 12, 24)
    oled.text("aumento de ", 12, 36)
    oled.text("CO2 no ar", 12, 46)
    oled.show()
    oled.fill(0)
    
def case9():
     led_matrix(ar2)
     

def case10():
    led_matrix(all_off)
    oled.fill(0)
    oled.text("FIM ", 24, 24)
    oled.show()
    oled.fill(0)
    
def case11():
    oled.text("Vamos", 24, 12)
    oled.text("Fazer um ", 24, 24)
    oled.text("Experimento?", 24, 36)
    oled.show()
    oled.fill(0)
    
def case12():
    oled.text("Efeito Estufa  ", 7, 12)
    oled.text("e o Aquecimento ", 7, 24)
    oled.text("Global", 7, 36)
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
        if count > 12:
            count = 12

    switch_case_dicionario(count) # chama a função switch_case com o valor atual de #count
    time.sleep_ms(140) #delay
