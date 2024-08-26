from machine import ADC, Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import neopixel, time

adc_vry = ADC(Pin(27)) # inicializa analog_y
button_a = Pin(5, Pin.IN, Pin.PULL_UP) # inicializa
button_b = Pin(6, Pin.IN, Pin.PULL_UP) # inicializa
i2c = SoftI2C(scl=Pin(15), sda=Pin(14)) # inicializa display oled
oled = SSD1306_I2C(128, 64, i2c) # inicializa display oled
NUM_LEDS = 25 # inicializa matriz leds
obj_leds5x5 = neopixel.NeoPixel(Pin(7), NUM_LEDS) # inicializa matriz leds

# Constantes
brilho = 2 # 0a255 em verde
espera = 0.14 # tempo em segundos entre leituras do analog
lim_min_y =15000
lim_max_y =45000

# Referencia dos LEDs 5x5
# [24, 23, 22, 21, 20],
# [15, 16, 17, 18, 19],
# [14, 13, 12, 11, 10],
# [ 5,  6,  7,  8,  9],
# [ 4,  3,  2,  1,  0]

A = [23, 2,21,16,13,6, 3,18,11,8, 1,12]
B = [23,22,21,16,13,6, 3,18, 8,1,12, 2]
C = [23,22,21,16,13,6, 3, 1, 2]
D = [23,22,16,13, 6,3,18,11, 8,2]
E = [23,22,21,16,13,6, 3, 1,12,2]
led_letras = [A,B,C,D,E]

num_questao=0
lista_questoes = [0,1,2,3,4,5,6,7,8,9]

def logica_circular(entrada,maxi):
    if entrada > maxi:
        entrada = 0
    if entrada < 0:
        entrada = maxi
    return entrada

def escolhe_letra():
    indice_letra = 0

    escolhendo = True
    while escolhendo:
        analog_Y = adc_vry.read_u16()
        if analog_Y < lim_min_y:
            indice_letra+=1
            indice_letra=logica_circular(indice_letra,4)
        elif analog_Y > lim_max_y:
            indice_letra-=1
            indice_letra=logica_circular(indice_letra,4)
        
        for led_i in range(NUM_LEDS):
            obj_leds5x5[led_i] = (0, 0, 0) # Desligar todos os LEDs
        
        desenho_letra = led_letras[indice_letra]
        for led_i in desenho_letra:
            obj_leds5x5[led_i] = (0, brilho, 0) # 0a255, brilho em RGB
            obj_leds5x5.write() # Mostra a letra sendo escolhida
            
        if button_a.value() == 0: # Sai do menu de letras e cai no menu de num_da_questao
            escolhendo = False # Quebra o while True, letra permanece acesa
        
        time.sleep(espera)


# Menu de selecao de numero da questao
while True:
    analog_Y = adc_vry.read_u16()
    if analog_Y < lim_min_y:
        num_questao+=1
        num_questao = logica_circular(num_questao,9)
    elif analog_Y > lim_max_y:
        num_questao-=1
        num_questao = logica_circular(num_questao,9)
    
    oled.fill(0)  # Limpar display
    oled.text("bot A:num B:letra", 0, 0) # instrucao ao usuario navegar entre menus
    oled.text("Questao {}".format(num_questao+1), 0, 10) # Exibe numero da questao no Display OLED
    oled.show()
    
    if button_b.value() == 0: # Sai do menu questoes e entra no menu de letras
        escolhe_letra() # Acessa selecao de Alternativas A...E
    
    time.sleep(espera) # Espera antes da próxima leitura