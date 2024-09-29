from machine import Pin, ADC

# Indica que o eixo X do Joystick esta no pino 27
xAxis = ADC(Pin(27))
# Indica que o eixo X do Joystick esta no pino 26
yAxis = ADC(Pin(26))
# Indica que o eixo X do Joystick esta no pino 22
button = Pin(22,Pin.IN, Pin.PULL_UP)

# Essa função retorna se o valor em X é para cima ou para baixo
# Para isso determinamos que abaixo de 600 é para baixo
# Acima de 6000 pra cima
def joystick_x():
    xValue = xAxis.read_u16()
    if xValue <= 600:
        return 1
    elif xValue >= 60000:
        return -1
    return 0

# Essa função retorna se o valor em Y é para esquerda ou para direita
# Para isso determnamos que abaixo de 600 é para esquerda
# Acima de 6000 pra deireita
def joystick_y():
    yValue = yAxis.read_u16()
    if yValue <= 600:
        return -1
    elif yValue >= 60000:
        return 1
    return 0

# retorna o valor do botão
def valor_botao_joystick():
    return button.value()

# Variável de controle
button_pressed = 1
# Essa função retorna se o botão do joystick está pressionado apenas uma vez por vez que é pressionado
def botao_joystick_pressionado():
    global button_pressed
    r = False
    a = valor_botao_joystick()
    if a == 0 and button_pressed != a:
        r = True
    button_pressed = a
    return r

# Variável de controle
button_released = 1
# Essa função retorna se o botão do joystick foi solto
def botao_joystick_solto():
    global button_released
    r = False
    a = valor_botao_joystick()
    if a == 1 and button_released != a:
        r = True
    button_released = a
    return r
