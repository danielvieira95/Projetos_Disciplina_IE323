from machine import I2C, Pin,SoftI2C 
from ssd1306 import SSD1306_I2C  
import ssd1306
import bme280
import time

# Configuração do barramento I2C0 para o display OLED e o sensor BME280
i2c1 = SoftI2C(scl=Pin(15), sda=Pin(14))  # pinos que serão utilizados no i2c
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Ajuste os pinos conforme sua conexão I2C

# Inicializa o display OLED
oled = ssd1306.SSD1306_I2C(128, 64, i2c1)

# Inicializa o sensor BME280
bme = bme280.BME280(i2c=i2c)

def display_temperature_humidity(temperature, humidity):
    oled.fill(0)  # Limpa o display
    oled.text('Temp: {}'.format(temperature), 0, 0)  # Exibe a temperatura
    oled.text('Humidity: {}'.format(humidity), 0, 10)  # Exibe a umidade
    oled.show()  # Atualiza o display

while True:
    # Leitura dos dados do sensor
    data = bme.values
    temperature = data[0]
    humidity = data[2]

    # Exibe a temperatura e umidade no display
    display_temperature_humidity(temperature, humidity)
    
    time.sleep(1)  # Aguarda 2 segundos antes da próxima leitura