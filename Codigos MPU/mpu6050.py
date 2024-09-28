from machine import Pin, I2C
from machine import Pin, SoftI2C, ADC
from ssd1306 import SSD1306_I2C
import utime
import time
from ssd1306 import SSD1306_I2C
# Endereço I2C do MPU6050
MPU6050_ADDR = 0x68
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)
# LED RGB
# Configuração do LED RGB
led_r = Pin(13, Pin.OUT)
led_g = Pin(12, Pin.OUT)
led_b = Pin(11, Pin.OUT)
def set_rgb_color(r, g, b):
    led_r.value(r)
    led_g.value(g)
    led_b.value(b)

# Função para testar o LED RGB
def test_rgb():
    print("Red ON")
    set_rgb_color(1, 0, 0)
    time.sleep(2)

    print("Green ON")
    set_rgb_color(0, 1, 0)
    time.sleep(2)
    
    print("Blue ON")
    set_rgb_color(0, 0, 1)
    time.sleep(2)
    
    print("All OFF")
    set_rgb_color(0, 0, 0)
    time.sleep(2)
# Teste OLED
oled.fill(0)  # Limpar display
oled.text("BitDogLab", 0, 0)
oled.text("Unicamp 4.0", 0, 10)
oled.text("Daniel Vieira",0,40)
oled.show()
test_rgb()
# Registradores do MPU6050
MPU6050_REG_POWER_MGMT_1 = 0x6B
MPU6050_REG_ACCEL_XOUT_H = 0x3B
MPU6050_REG_ACCEL_YOUT_H = 0x3D
MPU6050_REG_ACCEL_ZOUT_H = 0x3F

# Configuração do I2C
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000) # Pino 8 para SDA, Pino 9 para SCL

# Função para ler um valor de um registro de 16 bits
def read_word_2c(reg):
    high = i2c.readfrom_mem(MPU6050_ADDR, reg, 1)[0]
    low = i2c.readfrom_mem(MPU6050_ADDR, reg+1, 1)[0]
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

# Inicialização do MPU6050
i2c.writeto_mem(MPU6050_ADDR, MPU6050_REG_POWER_MGMT_1, b'\x00')

# Loop principal
while True:
    # Leitura dos valores dos eixos X, Y e Z
    accel_x = read_word_2c(MPU6050_REG_ACCEL_XOUT_H)
    accel_y = read_word_2c(MPU6050_REG_ACCEL_YOUT_H)
    accel_z = read_word_2c(MPU6050_REG_ACCEL_ZOUT_H)
    oled.fill(0)  # Limpar display
    oled.text("BitDogLab", 0, 0)
    oled.text(f"Eixo x: {accel_x:}  ", 0, 20)
    oled.text(f"Eixo y: {accel_y:}",0,30)
    oled.text(f"Eixo x: {accel_z:} ",0,40)    
    oled.show()
   
        
    # Exibição dos valores
    print("Acelerômetro - X:", accel_x, " Y:", accel_y, " Z:", accel_z)

    # Espera um tempo antes de ler novamente
    utime.sleep(1)
