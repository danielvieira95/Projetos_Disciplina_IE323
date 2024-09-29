# Esse módulo possui métodos utéis para programação da BitDogLab, os quais não se encaixavam
# nos outros módulos
# 
from utime import ticks_us, sleep
from machine import reset
import random
from .led import apagar_leds

#Essa função lê um arquivo e retorna seu valor
def ler_arquivo(nome):
    try:
        with open(nome, 'r') as f:
            mensagem = int(f.read())
    except:
       mensagem  = ''
    return mensagem

# Essa função escreve uma mensagem em um arquivo
def escrever_arquivo(nome, mensagem):
    with open(nome, 'w') as f:
        f.write(mensagem)

# Essa função retorna um numero aleatório entre numero1 e numero2
def numero_aleatorio(numero1, numero2):
    return random.randint(numero1, numero2)

# Retorna quanto tempo decorrido desde o tempo dado por old
def tempo_de_jogo(old):
    new = ticks_us()
    delta = abs(new - old)
    old = new
    return (delta, old)

# Executa a função do jogo em loop
def loop(func):
    old = ticks_us()
    while True:
        delta, old = tempo_de_jogo(old)
        func(delta)

# Essa função dorme a BitDogLab pelos segundos passados no argumento
def dormir(segundos):
    sleep(segundos)

# Essa função reinicia a BitDogLab de forma a apagar os LEDs
def reiniciar():
    apagar_leds()
    reset()
