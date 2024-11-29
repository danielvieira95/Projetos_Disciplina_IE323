from machine import Pin, SoftI2C  # Configura GPIOs e interface I2C
from ssd1306 import SSD1306_I2C  # Controla displays OLED
from bme680 import *  # Permite interagir com sensores BME680
import machine, neopixel  # Funções de hardware e controle de LEDs RGB
from time import sleep
from led import *  # Funções para gerenciar LEDs individuais em uma matriz
from machine import PWM, UART  # PWM para buzzer e UART para #comunicação serial

# Inicialização do Buzzer 
buzzer_a = PWM(Pin(21))
buzzer_a.freq(1000)  # Ajustar a frequência para o som desejado

# Configuração UART para o HC-05
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

# Inicialização do I2C para os sensores BME680 e para o display OLED
i2c_bme1 = SoftI2C(scl=Pin(3), sda=Pin(2))
i2c_bme2 = SoftI2C(scl=Pin(1), sda=Pin(0))
i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))

# Inicialização do display OLED
oled = SSD1306_I2C(128, 64, i2c_oled)

# Inicialização dos sensores BME680
bme1 = BME680_I2C(i2c=i2c_bme1)
bme2 = BME680_I2C(i2c=i2c_bme2)

# Configuração da matriz de LED
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)  


intensity = 0.1  # Ajuste do brilho da Matriz RGB

# Definição das cores
GREEN = (int(0 * intensity), int(255 * intensity), int(0 * intensity))  
BLUE = (int(0 * intensity), int(0 * intensity), int(255 * intensity))  
RED = (int(255 * intensity), int(0 * intensity), int(0 * intensity))  

# Configuração do botão
button = Pin(5, Pin.IN, Pin.PULL_UP)  

beeped = False  # Variável para rastrear se o beep já foi emitido
current_sensor = 1  # Variável para controlar qual sensor está sendo exibido

# Função que controla o Buzzer
def beep(buzzer, duration=500):
    buzzer.duty_u16(30000)  # Liga o buzzer 
    sleep(duration / 1000) 
    buzzer.duty_u16(0)  # Desliga o buzzer

# Função para mostrar os parâmetros dos sensores no display OLED 
def display_sensor_data(sensor):
    oled.fill(0)  

    if sensor == 1:
        temp = str(round(bme2.temperature, 2)) + ' C'
        hum = str(round(bme2.humidity, 2)) + ' %'
        pres = str(round(bme2.pressure, 2)) + ' hPa'
        gas = str(round(bme2.gas / 1000, 2)) + ' KOhms'
        oled.text('Sensor 1', 0, 0)
    else:
        temp = str(round(bme1.temperature, 2)) + ' C'
        hum = str(round(bme1.humidity, 2)) + ' %'
        pres = str(round(bme1.pressure, 2)) + ' hPa'
        gas = str(round(bme1.gas / 1000, 2)) + ' KOhms'
        oled.text('Sensor 2', 0, 0)

    oled.text('Temp: {}'.format(temp), 0, 10)
    oled.text('Umidade: {}'.format(hum), 0, 20)
    oled.text('Pressao: {}'.format(pres), 0, 30)
    oled.text('Gas: {}'.format(gas), 0, 40)
    oled.show()

# Essa função serve para alternar entre os sensores quando o botão é #pressionado
def read_button():
    global current_sensor
    if button.value() == 0:
        sleep(0.2)
        current_sensor = 2 if current_sensor == 1 else 1

# Essa função serve para configurar as cores para cada coluna de LEDs
def set_led_colors(sensor1_color, sensor2_color):
    for row in range(ROW_SIZE):
        ligar_led(3, row, sensor1_color)
        ligar_led(4, row, sensor1_color)
        ligar_led(0, row, sensor2_color)
        ligar_led(1, row, sensor2_color)
    np.write()

# Essa função envia os dados do sensor com marcadores claros para o App #Inventor
def enviar_dados_bluetooth(sensor, temp, hum, pres, gas):
    # Formatar os dados com marcadores e separador '|'
    if sensor == 1:
        uart.write(f"S1|{temp:.2f}|{hum:.2f}|{pres:.2f}|{gas:.2f}|\n")
    elif sensor == 2:
        uart.write(f"|S2|{temp:.2f}|{hum:.2f}|{pres:.2f}|{gas:.2f}\n")

while True:
    read_button()
    display_sensor_data(current_sensor)

    temp1 = bme2.temperature
    temp2 = bme1.temperature

# Cores da matriz de led se alteram de acordo com a temperatura
    color1 = GREEN if temp1 < 25 else BLUE if temp1 <= 30 else RED 
    color2 = GREEN if temp2 < 25 else BLUE if temp2 <= 30 else RED

    set_led_colors(color1, color2)

# Buzzer aciona quando a temperatura é maior que 30°C
    if (temp1 >= 30 or temp2 >= 30) and not beeped:
        beep(buzzer_a, duration=500)
        beeped = True
    elif temp1 < 30 and temp2 < 30:
        beeped = False

# Dados são enviados para o bluetooth
    enviar_dados_bluetooth(1, temp1, bme2.humidity, bme2.pressure, bme2.gas / 1000)
    enviar_dados_bluetooth(2, temp2, bme1.humidity, bme1.pressure, bme1.gas / 1000)
    sleep(1)
