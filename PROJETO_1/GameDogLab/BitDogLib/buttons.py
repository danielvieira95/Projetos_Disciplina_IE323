from machine import Pin

button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

button_a_pressed = 1
button_a_released = 1
button_b_pressed = 1
button_b_released = 1

def valor_botao_A():
    return button_a.value()

def valor_botao_B():
    return button_b.value()

def botao_A_pressionado():
    global button_a_pressed
    r = False
    a = valor_botao_A()
    if a == 0 and button_a_pressed != a:
        r = True
    button_a_pressed = a
    return r

def botao_A_solto():
    global button_a_released
    r = False
    a = valor_botao_A()
    if a == 1 and button_a_released != a:
        r = True
    button_a_released = a
    return r

def botao_B_pressionado():
    global button_b_pressed
    r = False
    b = valor_botao_B()
    if b == 0 and button_b_pressed != b:
        r = True
    button_b_pressed = b
    return r

def botao_B_solto():
    global button_b_released
    r = False
    b = valor_botao_B()
    if b == 0 and button_b_released != b:
        r = True
    button_b_released = b
    return r
