from machine import Pin, PWM, UART, SoftI2C
import neopixel, utime


# Classe para o sensor AHT10
class AHT10:
    def __init__(self, i2c):
        self.i2c = i2c
        self.address = 0x38  # Endereço padrão do AHT10
        
        # Inicializar o sensor
        try:
            self.i2c.writeto(self.address, bytes([0xE1, 0x08, 0x00]))
            utime.sleep_ms(10)
        except Exception as e:
            print("Erro ao inicializar AHT10:", e)

    def medir(self):
        try:
            # Comando de medição
            self.i2c.writeto(self.address, bytes([0xAC, 0x33, 0x00]))
            utime.sleep_ms(80)
            
            # Ler 6 bytes de dados
            dados = self.i2c.readfrom(self.address, 6)
            
            # Extrair umidade e temperatura
            umidade = ((dados[1] << 16) | (dados[2] << 8) | dados[3]) >> 4
            temperatura = ((dados[3] & 0x0F) << 16 | (dados[4] << 8) | dados[5])
            
            # Conversão para valores reais
            umidade_real = umidade * 100.0 / 0x100000
            temperatura_real = temperatura * 200.0 / 0x100000 - 50
            
            return temperatura_real, umidade_real
        
        except Exception as e:
            print("Erro ao ler AHT10:", e)
            return None, None


#Classe para implementação do driver PCA9685 para controle dos servo motores
class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.MODO1 = 0x00
        self.PRESCALE = 0xFE
        self.LED0_ON_L = 0x06
        
        # Inicialização padrão
        self.reset()
        self.set_pwm_freq(50)  # Frequência para servomotores

    def reset(self):
        self.i2c.writeto_mem(self.address, self.MODO1, bytes([0x00]))

    def set_pwm_freq(self, freq_hz):
        prescale = int((25000000 / (4096 * freq_hz)) - 1)
        old_mode = self.i2c.readfrom_mem(self.address, self.MODO1, 1)[0]
        new_mode = (old_mode & 0x7F) | 0x10
        
        self.i2c.writeto_mem(self.address, self.MODO1, bytes([new_mode]))
        self.i2c.writeto_mem(self.address, self.PRESCALE, bytes([prescale]))
        self.i2c.writeto_mem(self.address, self.MODO1, bytes([old_mode]))
        
        utime.sleep_ms(5)
        self.i2c.writeto_mem(self.address, self.MODO1, bytes([old_mode | 0xA0]))

    def set_pwm(self, channel, on, off):
        base_reg = self.LED0_ON_L + 4 * channel
        
        self.i2c.writeto_mem(self.address, base_reg, bytes([on & 0xFF]))
        self.i2c.writeto_mem(self.address, base_reg + 1, bytes([on >> 8]))
        self.i2c.writeto_mem(self.address, base_reg + 2, bytes([off & 0xFF]))
        self.i2c.writeto_mem(self.address, base_reg + 3, bytes([off >> 8]))

class ServoController:
    def __init__(self, i2c):
        self.pca = PCA9685(i2c)
        
        # Configurações de pulso para servomotores
        self.SERVO_MIN = 150   # Pulso mínimo (0 graus)
        self.SERVO_MAX = 600   # Pulso máximo (180 graus)
        self.SERVO_CENTER = 375  # Pulso central (90 graus)

    def map_angle_to_pulse(self, angle):
        """
        Mapeia ângulo para valor de pulso
        0° -> SERVO_MIN
        90° -> SERVO_CENTER
        180° -> SERVO_MAX
        """
        # Limitar ângulo entre 0 e 180
        angle = max(0, min(180, angle))
        
        # Interpolação linear
        pulse = int(self.SERVO_MIN + 
                    (self.SERVO_MAX - self.SERVO_MIN) * 
                    angle / 180)
        return pulse

    def mover_servo(self, canal, angulo):
        """
        Move o servo para um ângulo específico
        
        :param canal: Canal do PCA9685 (0-15)
        :param angulo: Ângulo de 0 a 180 graus
        """
        pulse = self.map_angle_to_pulse(angulo)
        self.pca.set_pwm(canal, 0, pulse)


# Configuração I2C
i2c = SoftI2C(scl=Pin(3), sda=Pin(2), freq=400000)

# Configuração da matriz de LEDs
matriz_leds = neopixel.NeoPixel(Pin(7), 25)

# Pino para acionar a ponte H TB6612FNG e permitir que os motores funcionem
aciona_motor = Pin(20, Pin.OUT)

# Pinos de controle da direção e velocidade (PWM) do motor esquerdo
direcao_motor_esquerdo_1 = Pin(4, Pin.OUT)
direcao_motor_esquerdo_2 = Pin(9, Pin.OUT)
PWM_esquerdo = PWM(Pin(8))
PWM_esquerdo.freq(1000)  # Frequência do PWM (1 kHz)

# Pinos de controle da direção e velocidade (PWM) do motor direito
direcao_motor_direito_1 = Pin(18, Pin.OUT)
direcao_motor_direito_2 = Pin(19, Pin.OUT)
PWM_direito = PWM(Pin(16))
PWM_direito.freq(1000)

# Configuração da UART0 para receber comandos do módulo Bluetooth HC-05
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Configura o duty cicle, que representa a porcentagem de velocidade dos motores. Sendo 65536 o máximo (100 %), 32768 representa 50%, que será a velocidade do motor
duty = 32768

# Configurando o Buzzer A no pino 21
alto_falante = PWM(Pin(21))
alto_falante.freq(200)

# Inicializa a matriz com todos os LEDs apagados
for i in range(25):
    matriz_leds[i] = (0, 0, 0)
matriz_leds.write()

# Configura o pino 17 para emitir pulso pelo sensor ultrassônico HC-SR04 e o pino 28 para receber o pulso
envia_pulso_ultrassom = Pin(17, Pin.OUT) # trigger
recebe_pulso_ultrassom = Pin(28, Pin.IN) # echo


# Define a duração do pulso do ultrassom (em microssegundos), a velocidade do som utilizada para cálculo da distância (em metros por segundo) e uma variavel
# que indica quando há um objeto próximo sendo detectado pelo sensor ultrassônico
DURACAO_PULSO_US = 10
VELOCIDADE_SOM = 343
objeto_proximo = 0

# Função para controlar os LEDs que indicam o sentido da movimentação das rodas
def leds_rodas(funcao):
    leds_azul = []
    leds_roxo = []
    leds_vermelho = []
    leds_branco = []

    if funcao == "avancar": 
        leds_azul = [5, 10, 15, 9, 14, 19] 
    elif funcao == "avancar_AD":
        leds_azul = [9, 10, 19]
        leds_roxo = [5, 14, 15]
    elif funcao == "avancar_AE":
        leds_azul = [5, 14, 15]
        leds_roxo = [9, 10, 19]
    elif funcao == "retroceder":
        leds_vermelho = [5, 10, 15, 9, 14, 19]
    elif funcao == "retroceder_RD":
        leds_vermelho = [9, 10, 19]
        leds_roxo = [5, 14, 15]
    elif funcao == "retroceder_RE":
        leds_vermelho = [5, 14, 15]
        leds_roxo = [9, 10, 19]
    elif funcao == "direita":
        leds_azul = [9, 10, 19]
        leds_vermelho = [5, 14, 15]    
    elif funcao == "esquerda":        
        leds_azul = [5, 14, 15]
        leds_vermelho = [9, 10, 19]
    elif funcao == "parar": 
        leds_branco = [5, 10, 15, 9, 14, 19]
        
    for i in range(25):
        if i in leds_branco:
            matriz_leds[i] = (5, 5, 5)
        elif i in leds_azul:
            matriz_leds[i] = (0, 0, 5)
        elif i in leds_vermelho:
            matriz_leds[i] = (5, 0, 0)
        elif i in leds_roxo:
            matriz_leds[i] = (4, 0, 5)
        else:
            matriz_leds[i] = (0, 0, 0)  # Apaga outros LEDs
    matriz_leds.write()

# Função para mover os motores para frente. É necessário setar a direção 1 de ambos os motores para que ele avance
def mover_avancar():
    aciona_motor.value(1)                # Habilita o driver do motor (ponte H)
    direcao_motor_esquerdo_1.value(1)
    direcao_motor_esquerdo_2.value(0)
    PWM_esquerdo.duty_u16(duty)          # Envia a velocidade média para o motor
    direcao_motor_direito_1.value(1)
    direcao_motor_direito_2.value(0)
    PWM_direito.duty_u16(duty)

# Função para avançar para a direita. Para isso, a velocidade da roda direita precisa ser menor (metade, nesse caso) do que a roda esquerda
def mover_avancar_AD():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(1)
    direcao_motor_esquerdo_2.value(0)
    PWM_esquerdo.duty_u16(duty)
    direcao_motor_direito_1.value(1)
    direcao_motor_direito_2.value(0)
    PWM_direito.duty_u16(int(duty/2))    # Envia metade da velocidae média para a roda direita

# Função para avançar para a esquerda. Para isso, a velocidade da roda esquerda precisa ser menor (metade, nesse caso) do que a roda direita
def mover_avancar_AE():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(1)
    direcao_motor_esquerdo_2.value(0)
    PWM_esquerdo.duty_u16(int(duty/2))
    direcao_motor_direito_1.value(1)
    direcao_motor_direito_2.value(0)
    PWM_direito.duty_u16(duty)

# Função para movor os motores para trás. É necessário setar a direção 2 de ambos os motores para que ele retroceda
def mover_retroceder():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(0)
    direcao_motor_esquerdo_2.value(1)
    PWM_esquerdo.duty_u16(duty)
    direcao_motor_direito_1.value(0)
    direcao_motor_direito_2.value(1)
    PWM_direito.duty_u16(duty)

# Função para retroceder para a direita
def mover_retroceder_RD():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(0)
    direcao_motor_esquerdo_2.value(1)
    PWM_esquerdo.duty_u16(duty)
    direcao_motor_direito_1.value(0)
    direcao_motor_direito_2.value(1)
    PWM_direito.duty_u16(int(duty/2))

# Função para retroceder para a esquerda
def mover_retroceder_RE():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(0)
    direcao_motor_esquerdo_2.value(1)
    PWM_esquerdo.duty_u16(int(duty/2))
    direcao_motor_direito_1.value(0)
    direcao_motor_direito_2.value(1)
    PWM_direito.duty_u16(duty)
    
# Função para girar para a direita. Como o veículo gira em torno do próprio eixo, basta girar as rodas em sentido oposto para que o robô gire
def mover_direita():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(1)
    direcao_motor_esquerdo_2.value(0)
    PWM_esquerdo.duty_u16(int(duty/2))
    direcao_motor_direito_1.value(0)
    direcao_motor_direito_2.value(1)
    PWM_direito.duty_u16(int(duty/2))

# Função para girar para a esquerda. Mesma ideia do anterior, mas com os sentidos invertidos
def mover_esquerda():
    aciona_motor.value(1)
    direcao_motor_esquerdo_1.value(0)
    direcao_motor_esquerdo_2.value(1)
    PWM_esquerdo.duty_u16(int(duty/2))
    direcao_motor_direito_1.value(1)
    direcao_motor_direito_2.value(0)
    PWM_direito.duty_u16(int(duty/2))

# Função que para ambosos motores. Primeiro são setadas velocidades igual a zero e nenhum sentido de giro, para então desativar a ponte H 
def parar_motores():
    direcao_motor_esquerdo_1.value(0)
    direcao_motor_esquerdo_2.value(0)
    PWM_esquerdo.duty_u16(0)
    direcao_motor_direito_1.value(0)
    direcao_motor_direito_2.value(0)
    PWM_direito.duty_u16(0)
    aciona_motor.value(0)

# Função que verifica a distância que o sensor ultrassônico está de obstáculos
def verifica_distancia():
        
    envia_pulso_ultrassom.low()
    utime.sleep_us(5)
    envia_pulso_ultrassom.high()
    utime.sleep_us(DURACAO_PULSO_US)
    envia_pulso_ultrassom.low()
    
    tempo_inicial = utime.ticks_us()
    tempo_sinal_baixo = tempo_inicial

    while recebe_pulso_ultrassom.value() == 0:
        tempo_sinal_baixo = utime.ticks_us()
        if (tempo_sinal_baixo - tempo_inicial > 23324):            
            return None

    tempo_inicial_eco = utime.ticks_us()
    tempo_sinal_alto = tempo_inicial_eco

    while recebe_pulso_ultrassom.value() == 1:
        tempo_sinal_alto = utime.ticks_us()
        if (tempo_sinal_alto - tempo_inicial_eco > 23324):            
            return None

    duracao_pulso = tempo_sinal_alto - tempo_sinal_baixo
    distancia_cm = (duracao_pulso * VELOCIDADE_SOM) / (2 * 10000)
    
            
    return distancia_cm


# Inicia com os motores parados
leds_rodas("parar")
parar_motores()

# Cria um objeto para o sensor AHT10
sensor_aht10 = AHT10(i2c)

# Cria controlador de servos
servo_controller = ServoController(i2c)

angulo_h=60
angulo_v=150

# Função para controlar servomotores
def controlar_servomotores(comando):
    
    global angulo_h, angulo_v
    min_angulo_h=0
    max_angulo_h=120
    min_angulo_v=90
    max_angulo_v=180
    
    if servo_controller is None:
        return
    
    # Servo 1 no canal 0
    if "u" in comando:
        angulo_h=min(angulo_h+1, max_angulo_h) #incremente ángulo horizontal limitado por max_angulo_h
        servo_controller.mover_servo(14, angulo_h) 
    elif "U" in comando:
        angulo_h=max(angulo_h-1, min_angulo_h)  #decrementa ángulo horizontal limitado por min_angulo_h
        servo_controller.mover_servo(14, angulo_h)   
    elif "s1c" in comando:
        servo_controller.centralizar_servo(14) # Centro
    
    # Servo 2 no canal 1
    if "V" in comando:
        angulo_v=min(angulo_v+1, max_angulo_v) #incremente ángulo vertical limitado por max_angulo_v
        servo_controller.mover_servo(15, angulo_v)  
    elif "v" in comando:
        angulo_v=max(angulo_v-1, min_angulo_v) #decrementa ángulo vertical limitado por min_angulo_v
        servo_controller.mover_servo(15, angulo_v)    
    elif "s2c" in comando:
        servo_controller.centralizar_servo(15) 

# Loop para receber os comandos da UART (que são os comandos transmitidos pelo celular) e controlar os motores
while True:
    if uart.any() > 0:                                     # Caso tenha algum dado na UART, pode ler o comando que chegou
        comando = uart.readline().decode('utf-8').strip()  # Decodifica o comando que chegou
        
        if ("a" in comando) and (objeto_proximo == 0):     # Caso não haja objeto próximo, pode se mover para frente
            leds_rodas("avancar")
            mover_avancar()
            comando="s2+"
        elif ("z" in comando) and (objeto_proximo == 0):
            leds_rodas("avancar_AD")
            mover_avancar_AD()
        elif ("y" in comando) and (objeto_proximo == 0):
            leds_rodas("avancar_AE")
            mover_avancar_AE()
        elif "r" in comando:
            leds_rodas("retroceder")
            mover_retroceder()
            comando="s2-"
        elif "x" in comando:
            leds_rodas("retroceder_RD")
            mover_retroceder_RD()
        elif "w" in comando:
            leds_rodas("retroceder_RE")
            mover_retroceder_RE()     
        elif "d" in comando:
            leds_rodas("direita")
            mover_direita()
        elif "e" in comando:
            leds_rodas("esquerda")
            mover_esquerda()
        elif "p" in comando:
            leds_rodas("parar")
            parar_motores()
        elif "b" in comando:             # Liga a buzina, indicando que o botão foi apertado
            alto_falante.duty_u16(800)
        elif "B" in comando:             # Desliga a buzina, indicando que o botão foi solto
            alto_falante.duty_u16(0)
        else:
            controlar_servomotores(comando)

    # Verifica se há algum obstáculo próximo. Caso tenha, a variável que indica proximidade é setada (colocada como verdadeira), e isso impede movimentação frontal
    distancia = verifica_distancia()
    if not distancia == None:
        if ((distancia < 20) and (objeto_proximo == 0)):
            objeto_proximo = 1
            parar_motores()
        elif ((distancia > 20) and (objeto_proximo == 1)):
            objeto_proximo = 0

        # Leitura de temperatura e umidade
        temperatura, umidade = sensor_aht10.medir()
        if temperatura is not None and umidade is not None:
            # Imprime distância, temperatura [°C] e umidade relativa [%]
            print(f"{distancia:>6.2f} cm | Temp: {temperatura:>5.1f} C | Umidade: {umidade:>5.1f} %")
            # Envia temperatura e umidade relativa pelo HC-05
            uart.write(temperatura)
            uart.write(umidade)
        else:
            print("Erro ao ler sensor AHT10")
            # Imprime distância
            print(f"{distancia:>6.2f} cm")