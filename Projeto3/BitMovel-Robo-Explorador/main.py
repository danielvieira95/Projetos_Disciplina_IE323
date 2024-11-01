from machine import Pin, PWM, UART
import neopixel, utime

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

# Configura o pino XX para emitir pulso pelo sensor ultrassônico HC-SR04 e o pino YY para receber o pulso
envia_pulso_ultrassom = Pin(2, Pin.OUT) # trigger
recebe_pulso_ultrassom = Pin(3, Pin.IN) # echo

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
        if (tempo_sinal_baixo > (tempo_inicial + 23324)):
            break

    tempo_inicial = utime.ticks_us()
    tempo_sinal_alto = tempo_inicial

    while recebe_pulso_ultrassom.value() == 1:
        tempo_sinal_alto = utime.ticks_us()
        if (tempo_sinal_alto > (tempo_inicial + 23324)):
            break

    diferenca_tempo = tempo_sinal_alto - tempo_sinal_baixo
    distancia_cm = (diferenca_tempo * VELOCIDADE_SOM) / (2 * 10000)
    print("distancia [cm]:", distancia_cm)
    return(distancia_cm)

# Inicia com os motores parados
leds_rodas("parar")
parar_motores()

# Loop para receber os comandos da UART (que são os comandos transmitidos pelo celucar) e controlar os motores
while True:
    if uart.any() > 0:                   # Caso tenha algum dado na UART, pode ler o comando que chegou
        comando = uart.readline().decode('utf-8').strip() # Decodifica o comando que chegou
        
        print(comando)

        if ("a" in comando) and (objeto_proximo == 0):
            leds_rodas("avancar")
            mover_avancar()
        elif ("z" in comando) and (objeto_proximo == 0):
            leds_rodas("avancar_AD")
            mover_avancar_AD()
        elif ("y" in comando) and (objeto_proximo == 0):
            leds_rodas("avancar_AE")
            mover_avancar_AE()
        elif "r" in comando:
            leds_rodas("retroceder")
            mover_retroceder()
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

    distancia = verifica_distancia()
    if ((distancia < 20) and (objeto_proximo == 0)):
        objeto_proximo = 1
    elif ((distancia > 20) and (objeto_proximo == 1)):
        objeto_proximo = 0