from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

# Configuração OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

def limpar_tela():
    oled.fill(0)

def escrever_tela(texto, x, y):
    oled.text(texto, x, y)

def mostrar_tela():
    oled.show()
