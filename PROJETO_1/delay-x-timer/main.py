from machine import Pin, I2C, ADC, Timer
from ssd1306 import SSD1306_I2C
import framebuf
import neopixel
import utime

LARGURA = 128  # Largura do display oLED
ALTURA = 64  # Altura do display oLED

# Modos de funcionamento do programa
SEM_MODO = 0
MODO_DELAY = 1
MODO_TIMER = 2

contador_botao_pressionado = 0 # Vai acumular o número de vezes que os botões foram pressionados
estado_botao_a = 0 # Estado que indica se o botão a está pressionado (igual a 1) ou não (igual a 0)
estado_botao_b = 0
estado_led = 0 # Estado que indica se a matriz de LEDs está acesa (igual a 1) ou não (igual a 0)
contador_loop = 0 # Acumula o número de iterações realizadas
modo_selecionado = 0 # Indica o modo de funcionamento do programa que foi selecionado (sem modo, modo delay ou modo timer)
timer_flag = 0 # Indica se o timer da "callback_delay" já atingiu o tempo

# Configuração do display oLED
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(LARGURA, ALTURA, i2c)

# Apaga todo o display
oled.fill(0)
oled.show()

# Salva os arrays de bytes com as imagens que serão exibidas no display oLED futuramente
snoopy_dormindo = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xf1\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xe0\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xe0\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xbe\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\x7f\x7f\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xfe\xff\xbf\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xdf\xff\xff\xe6\xff\xff\xff\xc0\xff\xff\xff\xff\xdf\xff\xff\xcf\x7f\xff\xff\xc0\xff\xff\xff\xff\xdf\xff\xff\xcf\x7f\xff\xff\xc0\xff\xff\xff\xff\xdf\xf8\x8f\xed\xff\xff\xff\xc0\xff\xff\xfe\xff\xdf\xef\xfb\xef\xff\xff\xff\xc0\xff\xff\xfe\xff\xdf\xbf\xfd\xef\xff\xff\xff\xc0\xff\xff\xfd\xff\xde\xff\xfe\xcf\xff\xff\xff\xc0\xff\xff\xfd\xdf\xfd\xff\xff\x5f\xff\xff\xff\xc0\xff\xff\xff\xff\xf3\xff\xff\xb7\xff\xff\xff\xc0\xff\xff\xff\xff\xf3\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfb\xff\xff\xff\x7f\xff\xff\xc0\xff\xff\xfd\xff\xfb\xe3\x3f\xff\x7f\xff\xff\xc0\xff\xff\xfd\xff\xf3\xff\xdf\xc0\x3f\xff\xff\xc0\xff\xff\xfe\xfe\x1c\x1f\xef\xff\xbf\xff\xff\xc0\xff\xff\xfc\x00\x7f\xf7\xef\xff\xff\xff\xff\xc0\xff\xff\xfb\xfc\x7f\xfc\xcf\xff\xff\xff\xff\xc0\xff\xff\xfb\xfc\x7f\xff\x1f\xff\xdf\xff\xff\xc0\xff\xff\xfb\xfc\x7f\xff\xff\xff\xdf\xff\xff\xc0\xff\xff\xfb\xfc\x3f\xff\xf8\x01\xdf\xff\xff\xc0\xff\xff\xfb\xfc\x3c\x20\x07\xff\xef\xff\xff\xc0\xff\xff\xfe\x0c\x27\xff\xff\xff\xef\xff\xff\xc0\xff\xff\xf7\xfc\x3f\xff\xff\xff\xef\xff\xff\xc0\xff\xff\xf7\xfc\x3f\xff\xff\xff\xf7\xff\xff\xc0\xff\xff\xf7\xfe\x3f\xff\xff\xff\xf7\xff\xff\xc0\xff\xff\xf7\xff\x7f\xff\xff\xff\xfb\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xfb\xff\xff\xc0\xff\xff\xef\xff\xff\xff\xff\xe3\xff\xff\xff\xc0\xff\xff\xef\x00\x70\x00\x00\x3e\x0d\xff\xff\xc0\xff\xff\xef\xff\xff\xff\xff\xff\xfe\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0') 
snoopy_atento = bytearray(b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\x9f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\x80\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xf0\x00\x7f\x3f\xff\xff\xff\xc0\xff\xff\xff\xff\xcf\xff\xff\x9f\xff\xff\xff\xc0\xff\xff\xff\xff\xbf\xff\xff\xdf\xff\xff\xff\xc0\xff\xff\xff\xff\x3f\xff\xff\xef\xff\xff\xff\xc0\xff\xff\xff\xff\x7f\xff\xff\xef\xff\xff\xff\xc0\xff\xff\xff\xf0\xff\xfb\xff\xf7\xff\xff\xff\xc0\xff\xff\xff\xee\xff\xfb\xff\xf7\xff\xff\xff\xc0\xff\xff\xff\xe8\xff\xff\xff\xf7\xff\xff\xff\xc0\xff\xff\xff\xe0\xff\xff\xff\x8b\xff\xff\xff\xc0\xff\xff\xff\xf0\xff\xff\xfd\x03\xff\xff\xff\xc0\xff\xff\xff\xff\x7f\xff\xf8\x0b\xff\xff\xff\xc0\xff\xff\xff\xff\x9f\xff\xf8\x0b\xff\xff\xff\xc0\xff\xff\xff\xff\xe7\xff\xf0\x0b\xff\xff\xff\xc0\xff\xff\xff\xff\xf8\xff\xf0\x17\xff\xff\xff\xc0\xff\xff\xff\xff\xff\x3f\xf0\x07\xff\xff\xff\xc0\xff\xff\xff\xff\xff\x9f\xf0\x0f\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xef\x84\x1f\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xef\x78\x7f\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xee\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xc1\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\x9c\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\x3d\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\x7e\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfe\xfe\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfc\xfe\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfd\xfe\x7f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfd\xee\x7f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfb\xee\x7f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfb\xec\x7f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xf9\xe0\x3f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfe\x7a\x2f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xbe\xdf\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xbe\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xf0\x36\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xdf\xf6\x7f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xb9\xef\xbf\xff\xff\xff\xff\xc0\xff\xff\xff\xff\x83\xff\xdf\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xf6\xbf\xdf\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xfc\x00\x3f\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0')
snoopy_acordado = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x3f\xe0\x00\x00\x00\x00\x00\x00\x00\x7f\xf0\x00\x00\x00\x00\x00\x00\x00\xff\xfe\x1f\xf0\x00\x00\x00\x00\x01\xff\xff\xff\xfc\x00\x00\x00\x00\x01\xff\xff\xff\xfe\x00\x00\x00\x00\x03\xff\xdd\xff\xff\x00\x00\x00\x00\x03\xff\x9d\xff\xff\x80\x00\x00\x00\x07\xff\xff\xff\xff\xc0\x00\x00\x00\x07\xff\xff\xfe\x0f\xe0\x00\x00\x00\x0f\xff\xff\xfe\x0f\xe0\x00\x00\x00\x0a\xff\xff\xff\xff\xe0\x00\x00\x00\x08\x7f\xff\xff\xff\xe0\x00\x00\x00\x08\x3f\xff\xff\xff\xe0\x00\x00\x00\x08\x3f\xff\xff\xff\xc0\x00\x00\x00\x18\x17\xff\xff\xff\x80\x00\x00\x00\x18\x1f\xff\xff\xf8\x00\x00\x00\x00\x08\x1b\xff\xff\x00\x00\x00\xc0\x00\x08\x1b\xff\xde\x03\xf0\x03\xc0\x00\x0c\x0c\x01\xfe\x0f\xfc\x0f\xe0\x00\x04\x08\x00\x7c\xff\xff\x07\xe0\x00\x04\x18\x00\x1b\xff\xff\x07\xe0\x00\x02\x18\x00\x07\xff\xff\x87\xe0\x00\x00\x40\x00\x07\xff\xff\x87\xf0\x00\x00\x00\x00\x07\xff\xff\xcb\xf0\x00\x00\x00\x00\x0f\xff\xff\xc3\xf0\x00\x00\x00\x00\x0f\xff\xff\xc1\xf0\x00\x00\x00\x00\x3f\xfc\x7f\xfd\xf8\x00\x00\x00\x00\x7f\xff\xbf\xff\xf8\x00\x00\x00\x00\xff\xff\xdf\xff\xf8\x00\x00\x00\x00\xfc\x9f\xdf\xff\xf8\x00\x1f\xff\xff\xff\xcf\xbf\xff\xe3\xc0\x1f\xff\xff\xff\xff\xff\xff\xff\xc0\x1f\xff\xff\xff\xff\xff\xff\xff\xe0\x3f\xff\xff\xff\xff\xff\xff\xff\xe0\x3f\xff\xff\xff\xff\xff\xff\xff\xe0\x3f\xff\xff\xff\xff\xff\xff\xff\xe0\x3f\xff\xff\xff\xff\xff\xff\xff\xe0\x3f\xff\xff\xff\xff\xff\xff\xff\xf0\x7f\xff\xff\xff\xff\xff\xff\xff\xf0\x7f\xff\xff\xff\xff\xff\xff\xff\xf0\x7f\xff\xff\xff\xff\xff\xff\xff\xf0\x7f\x00\x3f\xff\xff\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00')

# Configuração dos botões A e B
botao_a = Pin(5, Pin.IN, Pin.PULL_UP)
botao_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Configuração da matriz de LEDs
matriz_leds = neopixel.NeoPixel(Pin(7), 25)

# Inicializa a matriz com todos os LEDs apagados
for i in range(25):
    matriz_leds[i] = (0, 0, 0)
matriz_leds.write()

# Configuração do joystick
adc_x = ADC(Pin(27))

# Define os valores mínimos e máximos dos conversores AD do joystick e também o valor médio
adc_min = 176
adc_max = 65263
adc_medio_x = ((adc_max - adc_min)/2)

# Define um limiar para determinar uma mudança significativa do joystick
limite = 1000

# Configuração do timer
temporizador = Timer()

# Função responsável por verificar se o botão a foi pressionado. Caso o valor do botão seja 0, indica que ele está pressionado.
# Se o estado do botão for 0, isso quer dizer que o botão não estava pressionado na última verificação.
# Se o valor e o estado são 0, significa que o botão acabou de ser pressionado e deve ter seu estado alterado para 1 (indicando que está pressionado),
# e a variável contadora deve ser somada 1.
def verifica_botao_a(botao_a, contador_botao_pressionado, estado_botao_a):
    if (botao_a.value() == 0) & (estado_botao_a == 0):
        contador_botao_pressionado += 1
        estado_botao_a = 1
# Caso o valor do botão seja 1, indica que ele não está pressionado. Se o estado do botão for 1, quer dizer que o botão estava pressionado na última verificação.
# Se o valor e o estado são 1, significa que o botão acabou de ser solto e deve ter seu estado alterado para 0 (indicando que não está mais pressionado),
    elif (botao_a.value() == 1) & (estado_botao_a == 1):
        estado_botao_a = 0
    return(contador_botao_pressionado, estado_botao_a)

def verifica_botao_b(botao_b, contador_botao_pressionado, estado_botao_b):
    if (botao_b.value() == 0) & (estado_botao_b == 0):
        contador_botao_pressionado += 1
        estado_botao_b = 1
    elif (botao_b.value() == 1) & (estado_botao_b == 1):
        estado_botao_b = 0
    return(contador_botao_pressionado, estado_botao_b)

# Função irá atualizar o display apresentando a atual quantidade de vezes que os botões foram pressionados e também exibe o Snoopy correspondente
def atualiza_display(snoopy, contador_botao_pressionado):
    oled.fill(0)
    oled.text("Contador: " + str(contador_botao_pressionado), 22, 3)
# Caso seja o Snoopy acordando, é uma image menor, então a posição em x é diferente
    if (snoopy == snoopy_acordado):
        fbuf_snoopy = framebuf.FrameBuffer(snoopy, 70, 45, framebuf.MONO_HLSB) # Objeto que contém a imagem formada pelos bytes que vão compor a imagem, com altura e largura definidos
        oled.blit(fbuf_snoopy, 32, 18) # Imagem vai aparecer em x = 32 e y = 18
    else:    
        fbuf_snoopy = framebuf.FrameBuffer(snoopy, 90, 45, framebuf.MONO_HLSB) # Objeto que contém a imagem formada pelos bytes que vão compor a imagem, com altura e largura definidos
        oled.blit(fbuf_snoopy, 22, 18) # Imagem vai aparecer em x = 22 e y = 18
    oled.show()

# Função irá ligar todos os LEDs da matriz e atualizar a variável que indica o estado do led para 1 (matriz acesa)
def liga_led(estado_led):
    for i in range(25):
        matriz_leds[i] = (5, 0, 0)
    matriz_leds.write()
    estado_led = 1
    return estado_led

# Função irá desligar todos os LEDs da matriz e atualizar a variável que indica o estado do led para 0 (matriz apagada)
def desliga_led(estado_led):
    for i in range(25):
        matriz_leds[i] = (0, 0, 0)
    matriz_leds.write()
    estado_led = 0
    return estado_led

# Verifica o atual estado da matriz de LEDs e inverte esse estado
def alterna_led(estado_led):
    if (estado_led == 0):
        estado_led = liga_led(estado_led)
    else:
        estado_led = desliga_led(estado_led)
    return estado_led

# Essa callback é utilizada no modo delay, e atualiza a flag "timer_flag" indicando que o temporizador atingiu sua contagem
def callback_delay(timer):
    global timer_flag
    timer_flag = 1

# Callback utilizada no modo timer, irá mudar o estado da matriz de LEDs e acrescentar 1 na contagem de iterações da rotina
def callback_timer(timer):
    global contador_loop, estado_led
    estado_led = alterna_led(estado_led)
    contador_loop += 1

# Apresenta a tela de início no display oLED pedindo para escolher um modo e entra em uma rotina de verifição do valor do joystick
def seleciona_modo(modo_selecionado):
    # Tela de início
    oled.fill(0)
    oled.text("Escolha um modo:", 0, 10)
    oled.text("Delay <---", 0, 30)
    oled.text("---> Timer ", 50, 50)
    oled.show()
# Verifica o valor no eixo x do joystick. Caso o valor medido seja maior ou menor que o valor médio (e um valor limite de variação), 
# significa que um lado foi escolhido e, portanto, um modo foi selecionado, que será indicado no display oLED
    while (modo_selecionado == SEM_MODO):
        adc_value_x = adc_x.read_u16()
        if (adc_value_x > (adc_medio_x + limite)):
            modo_selecionado = MODO_DELAY
            oled.fill(0)
            oled.text("Modo delay", 0, 30)
            oled.show()
            utime.sleep(3)
        elif (adc_value_x < (adc_medio_x - limite)):
            modo_selecionado = MODO_TIMER
            oled.fill(0)
            oled.text("Modo timer", 0, 30)
            oled.show()
            utime.sleep(3)
    return modo_selecionado

while True:
    modo_selecionado = seleciona_modo(modo_selecionado)
# Caso o modo de funcionamento escolhido seja o modo delay, a rotina que será executada por 5 vezes consiste em iniciar verificando se os botões foram pressionados,
# atualizar o display com a imagem do Snoopy dormindo e o valor do contador, acender a matriz de LEDs e então vai iniciar o delay de 3 segundos.
# Como isso interrompe o funcionamento do código, não é possível registrar que o botão foi pressionado. Após o fim do delay, a matriz de LEDs apagada,
# é iniciado um timer de 3 segundos e o código entra em um laço de repetição que irá verificar os botões e atualizar o display, com imagem do Snoopy acordando,
# de maneira contínua. O laço só tem fim quando o timer atinge 3 segundos e atualiza a flag do timer e a rotina finalmente é reiniciada.
    if (modo_selecionado == MODO_DELAY):
        estado_led = desliga_led(estado_led) # Garante que toda vez que inicia uma rotina, a matriz de LEDs está apagada
        contador_loop = 0 # Garante que contador de iterações da rotina inicia em estado inicial
        for contador_loop in range(5):
            contador_botao_pressionado, estado_botao_a = verifica_botao_a(botao_a, contador_botao_pressionado, estado_botao_a)
            contador_botao_pressionado, estado_botao_b = verifica_botao_b(botao_b, contador_botao_pressionado, estado_botao_b)
            estado_botao_a = 0
            estado_botao_b = 0
            atualiza_display(snoopy_dormindo, contador_botao_pressionado)
            estado_led = alterna_led(estado_led)
            utime.sleep(3)
            temporizador.init(mode=Timer.ONE_SHOT, period=3000, callback=callback_delay) # A callback irá alterar o estado da flag do timer ao atingir o tempo
            estado_led = alterna_led(estado_led)
            while(timer_flag == 0):
                contador_botao_pressionado, estado_botao_a = verifica_botao_a(botao_a, contador_botao_pressionado, estado_botao_a)
                contador_botao_pressionado, estado_botao_b = verifica_botao_b(botao_b, contador_botao_pressionado, estado_botao_b)
                atualiza_display(snoopy_acordado, contador_botao_pressionado)
            timer_flag = 0
            temporizador.deinit()
            contador_loop += 1
        contador_botao_pressionado = 0
        modo_selecionado = SEM_MODO # Após o fim da rotina do modo, o programa volta para a tela inicial de seleção
# Caso o modo selecionado seja o timer, um temporizador periódico de 3 segundos é iniciado. Quando é atingido, ele acrescenta na contagem de iterações e altera
# o estado da matriz de LEDs. Enquanto isso, os botões são verificados constantemente e o display com contador e o Snoopy atento é atualizado.
# Após 10 iterações, a rotina é finalizada e retorna à tela inicial de seleção de modo.
    elif (modo_selecionado == MODO_TIMER):
        estado_led = desliga_led(estado_led)
        temporizador.init(period = 3000, mode = Timer.PERIODIC, callback = callback_timer)
        contador_loop = 0
        while(contador_loop < 10):
            contador_botao_pressionado, estado_botao_a = verifica_botao_a(botao_a, contador_botao_pressionado, estado_botao_a)
            contador_botao_pressionado, estado_botao_b = verifica_botao_b(botao_b, contador_botao_pressionado, estado_botao_b)
            atualiza_display(snoopy_atento, contador_botao_pressionado)
        temporizador.deinit()
        contador_botao_pressionado = 0
        modo_selecionado = SEM_MODO