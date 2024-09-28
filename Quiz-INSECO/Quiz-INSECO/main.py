from machine import Pin, I2C, ADC, PWM, Timer
import neopixel
import ssd1306
import time
import random

# Configurações do display OLED no canal I2C0
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Configurações da matriz de LEDs
led_pin = Pin(7, Pin.OUT)
leds = neopixel.NeoPixel(led_pin, 25)

# Configurações do joystick
vrx = ADC(Pin(27))  # Eixo X
vry = ADC(Pin(26))  # Eixo Y
sw = Pin(22, Pin.IN, Pin.PULL_UP)  # Botão de seleção

# Configurações dos botões e buzzers
botao_a = Pin(5, Pin.IN, Pin.PULL_UP) # botão da esquerda
botao_b = Pin(6, Pin.IN, Pin.PULL_UP) # botão da direita
buzzer_a = PWM(Pin(21)) # buzzer da esquerda
buzzer_b = PWM(Pin(10)) # buzzer da direita

# Configurações iniciais
colors = {"Red": 0, "Green": 0, "Blue": 0}
color_names = ["Red", "Green", "Blue"]

attempts = 20 #numero de tentativas
selected_color = 0 # seleçao inicia das cores RGB Red -> 0; Green -> 1; Blue -> 2
current_color = None #variavel de armazenamento do cor atual
start_time = 0 #variavel de armazenamento do tempo de inicio do jogo
errors = 0 # numeros de erros
rounds = 0 # numeros de jogadas feitas
started_game = False # Variavel de controlo do inicio do jogo
ended_game = False # variavel de controlo de fim do jogo
led_attempt = 24 #posição do led da matriz de LEDS que vai começar as tentativas em ordem decrescente 
level = 1 # nivel de jogos
level_value = 0 # o numero de passo de troca dos valores de RGB
win = 0 # contagem de vitorias

# função do nivel do jogo:
def random_value(option):
    if option == 1:
        # Valores específicos: 0 e 100
        values = [0,100]
    elif option == 2:
        # Valores específicos: 0, 50 e 100
        values = [50, 100]
    elif option == 3:
        # Valores específicos: 0, 25, 50, 75 e 100
        values = [25, 50, 75, 100]
    else:
        raise ValueError("Opção inválida. Escolha 1, 2 ou 3.")
    
    return random.choice(values)


# funcao  que converte o 0 á 100 para 0 á 50
def converter_valor(valor):
    # Verifica se o valor está dentro do intervalo esperado
    if 0 <= valor <= 100:
        return (valor * 50) // 100
    else:
        raise ValueError("O valor deve estar entre 0 e 100.")
# Função para tocar som
def play_sound(buzzer, frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)
    time.sleep(duration)
    buzzer.duty_u16(0)

# Função para atualizar o display OLED
def update_oled(r, g, b):
    global current_color
    oled.fill(0)
    oled.text(f"Cria a cor..", 0, 0)
    oled.text(f"sorteada", 0, 10)
    oled.text(f"RGB:{color_names[selected_color]}", 0, 20)
    oled.text(f"R:{r} ", 0, 30) #if r != current_color['r'] else oled.text(f"R:{r} <", 0, 30)
    oled.text(f"G:{g} ", 0, 40) #if g != current_color['g'] else oled.text(f"G:{g} <", 0, 40)
    oled.text(f"B:{b} ", 0, 50) #if b != current_color['b'] else oled.text(f"B:{b} <", 0, 50)
    oled.show()

# Função para acender LED com cor aleatória
#Ajustar o código para não repetir a mesma cor num mesmo jogo
def light_random_led():
    global current_color
    current_color = {"r": random_value(level), "g": random_value(level), "b": random_value(level)} #random.choice(predefined_colors) {"name": "Vermelho", "r": 100, "g": 0, "b": 0}
    for i in range(5):
        leds[i] = (converter_valor(current_color['r']), converter_valor(current_color['g']), converter_valor(current_color['b']))    
    leds.write()
    oled.fill(0)
    oled.text(f"Nivel: {level}", 0, 0)
    #oled.text(f"{level}", 0, 10)
    oled.show()
    time.sleep(3)

# Função para iniciar o jogo
def start_game():
    colors["Red"] = 0
    colors["Green"] = 0
    colors["Blue"] = 0    
    global started_game, ended_game
    if started_game == False:
        global errors, rounds
        oled.fill(0)
        oled.text("Atencao!", 0, 0) #oled.text("Texto a imprimir", eixo x, eixo y)
        oled.text("Jogo comecando", 0, 10)
        oled.show()
        time.sleep(3)
        light_random_led()
        #time.sleep(3)
        started_game = True
        ended_game = False


# Função para reiniciar Leds
def reset_leds():
    for i in range(25):
        leds[i] = (0, 0, 0)
    leds.write()

# Função para verificar a cor
def check_color():
    global errors, rounds,led_attempt,level,win
    r = colors["Red"]
    g = colors["Green"]
    b = colors["Blue"]
    if r == current_color['r'] and g == current_color['g'] and b == current_color['b']:
        leds[led_attempt] = (converter_valor(r), converter_valor(g), converter_valor(b))
        leds.write()
        play_sound(buzzer_a, 1000, 0.2)
        play_sound(buzzer_b, 1000, 0.2)
        oled.fill(0)
        oled.text("Parabens!", 0, 0)
        oled.text("Cor correta.", 0, 10)
        oled.show()
        time.sleep(4)
        rounds += 1
        level += 1
        win += 1
        if rounds == 3:        
            end_game()
        else:
            next_game()      
    else:
        errors += 1
        leds[led_attempt] = (converter_valor(r), converter_valor(g), converter_valor(b))
        leds.write()
        led_attempt = led_attempt - 1
        play_sound(buzzer_a, 500, 0.4)
        play_sound(buzzer_b, 500, 0.4)
        oled.fill(0)
        oled.text("Opa!", 0, 0)
        oled.text("Tente de novo.", 0, 10)
        oled.show()
        time.sleep(2)
        if errors == attempts:
            end_game()
        

            
def next_game():
    global started_game, led_attempt, attempts
    oled.fill(0)
    #oled.text("Parabens!", 0, 0)
    oled.text(f"Proximo nivel.", 0, 10)
    oled.show()
    time.sleep(4)
    reset_leds()
    started_game = False
    led_attempt = 24
    attempts = 0
    start_game()
    

# Função para finalizar o jogo
def end_game():
    global ended_game,led_attempt
    total_time = time.time() - start_time
    oled.fill(0)
    oled.text("Fim de Jogo!", 0, 0)
    oled.text(f"Erros: {errors}", 0, 10)
    oled.text(f"Jogadas: {rounds + errors}", 0, 20)
    oled.text(f"Certos: {win}", 0, 30)
    oled.text(f"Tempo: {int(total_time)}s", 0, 40)
    oled.show()
    time.sleep(6)
    oled.fill(0)
    oled.text("Para reiniciar...", 0, 0)
    oled.text("clique botao...", 0, 10)
    oled.text("a direita!", 0, 20)
    oled.show()
    ended_game = True
    

# Apresendado no inicio do jogo
def start():
    reset_leds()
    oled.fill(0)
    oled.text("Bem vindo", 0, 0)
    oled.text("Jogo vai comecar", 0, 10)
    oled.text("clique botao...", 0, 20)
    oled.text("a esquerda!", 0, 30)
    oled.show()
    time.sleep(0.1)
start()

# Loop principal
while True:
    
    if botao_a.value() == 0:
        start_time = time.time()
        start_game()
    
    if botao_b.value() == 0:
        start_time = time.time()
        reset_leds()
        oled.fill(0)
        oled.text("Reiniciando", 0, 0)
        oled.show()
        time.sleep(2)
        started_game = False
        errors = 0
        rounds = 0
        win = 0
        level = 1
        led_attempt = 24
        attempts = 0
        start_game()
        
    
    if current_color:
        x_value = vrx.read_u16()
        y_value = vry.read_u16()

        if level == 1:
            level_value = 100
        if level == 2:
            level_value = 50
        if level == 3 :
            level_value = 25

        # Ajuste do valor da cor com o eixo X
        if x_value > 45000:
            colors[color_names[selected_color]] = max(colors[color_names[selected_color]] - level_value, 0)
        elif x_value < 20000:
            colors[color_names[selected_color]] = min(colors[color_names[selected_color]] + level_value, 100)
            

        # Navegação pelas cores com o eixo Y
        if y_value > 45000:
            selected_color = (selected_color + 1) % 3
            time.sleep(0.3)
        elif y_value < 20000:
            selected_color = (selected_color - 1) % 3
            time.sleep(0.3)

        if ended_game != True:
            update_oled(colors["Red"], colors["Green"], colors["Blue"])

        if sw.value() == 0 and ended_game != True:
            check_color()

    time.sleep(0.1)
