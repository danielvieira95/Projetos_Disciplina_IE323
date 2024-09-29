from machine import Pin

# Indica que o botão A está no pino 5
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
# Indica que o botão A está no pino 6
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Variaveis de controle
button_a_pressed = 1
button_a_released = 1
button_b_pressed = 1
button_b_released = 1

# Essa função retorna o valor do botão A
def valor_botao_A():
    return button_a.value()

# Essa função retorna o valor do botão B
def valor_botao_B():
    return button_b.value()

# Essa função retorna se o botão A está pressionado
def botao_A_pressionado():
    global button_a_pressed
    r = False
    a = valor_botao_A()
    if a == 0 and button_a_pressed != a:
        r = True
    button_a_pressed = a
    return r

# Essa função retorna se o botão A está solto
def botao_A_solto():
    global button_a_released
    r = False
    a = valor_botao_A()
    if a == 1 and button_a_released != a:
        r = True
    button_a_released = a
    return r

# Essa função retorna se o botão B está pressionado
def botao_B_pressionado():
    global button_b_pressed
    r = False
    b = valor_botao_B()
    if b == 0 and button_b_pressed != b:
        r = True
    button_b_pressed = b
    return r

# Essa função retorna se o botão B está solto
def botao_B_solto():
    global button_b_released
    r = False
    b = valor_botao_B()
    if b == 1 and button_b_released != b:
        r = True
    button_b_released = b
    return r