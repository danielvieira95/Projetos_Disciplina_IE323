from machine import Pin, SoftI2C  # Configurar entradas/saídas digitais e criar interface I2C
from ssd1306 import SSD1306_I2C  # Controlar displays OLED
import machine, neopixel  # Controlar diretamente o hardware microcontrolador
import time  # Funções relacionadas ao tempo
import ahtx0  # Controlar sensores AHT10

# Configuração do barramento I2C para o display OLED e sensores AHT10
i2c1 = SoftI2C(scl=Pin(15), sda=Pin(14))  # Pinos para o display OLED
i2c2 = SoftI2C(scl=Pin(3), sda=Pin(2))  # Pinos para o primeiro sensor AHT10
i2c3 = SoftI2C(scl=Pin(1), sda=Pin(0))  # Pinos para o segundo sensor AHT10

oled = SSD1306_I2C(128, 64, i2c1)  # Inicializa o display OLED

# Inicializa a matriz de LED
np = neopixel.NeoPixel(machine.Pin(7), 25)  # 25 LEDs controlados via pino 7

intensity = 0.1  # 50% do brilho
# Definir cores para os LEDs
GREEN = (int(0 * intensity), int(255 * intensity), int(0 * intensity))  # Verde com brilho reduzido
RED = (int(255 * intensity), int(0 * intensity), int(0 * intensity))  # Vermelho com brilho reduzido
BLU = (int(0 * intensity), int(0 * intensity), int(255 * intensity))  # Vermelho com brilho reduzido
# Inicializa os sensores AHT10
sensor1 = ahtx0.AHT10(i2c2)
sensor2 = ahtx0.AHT10(i2c3)

def set_led_color(color):
    """Define a cor de toda a matriz de LEDs."""
    for i in range(25):
        np[i] = color  # Define a cor para cada LED
    np.write()  # Atualiza a matriz de LEDs

def display_temperature_humidity(temp1, humidity1, temp2, humidity2):
    """Exibe as temperaturas e umidades no display OLED."""
    oled.fill(0)  # Limpa o display
    oled.text('Sensor1', 0, 0)
    oled.text('Temp: {:.1f} C'.format(temp1), 0, 10)  # Exibe a temperatura do sensor 1
    oled.text('Umidade: {:.1f} %'.format(humidity1), 0, 20)  # Exibe a umidade do sensor 1
    oled.text('Sensor2', 0, 30)
    oled.text('Temp: {:.1f} C'.format(temp2), 0, 40)  # Exibe a temperatura do sensor 2
    oled.text('Umidade: {:.1f} %'.format(humidity2), 0, 50)  # Exibe a umidade do sensor 2
    oled.show()  # Atualiza o display

while True:
    try:
        # Leitura dos dados dos sensores
        temperature1 = sensor1.temperature
        humidity1 = sensor1.relative_humidity
        temperature2 = sensor2.temperature
        humidity2 = sensor2.relative_humidity
        
        # Exibe os dados no display OLED
        display_temperature_humidity(temperature1, humidity1, temperature2, humidity2)
        
        # Controle da cor da matriz de LED com base na temperatura do sensor 1
        if temperature2 < 25:
            set_led_color(GREEN)  # Acende verde se a temperatura for menor que 25°C
        elif temperature2 > 30:
            set_led_color(RED)  # Acende vermelho se a temperatura for maior que 30°C
        else:
            set_led_color(BLU)  # Desliga os LEDs se estiver entre 25°C e 30°C

    except OSError as e:
        oled.fill(0)
        oled.text('Error:', 0, 0)
        oled.text(str(e), 0, 10)
        oled.show()

    time.sleep(1)  # Aguarda 2 segundos antes de fazer nova leitura

