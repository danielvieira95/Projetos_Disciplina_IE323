from utime import ticks_us
import random


def ler_arquivo(nome):
    try:
        with open(nome, 'r') as f:
            mensagem = f.read()
    except:
       mensagem  = ''
    return mensagem

def escrever_arquivo(nome, mensagem):
    with open(nome, 'w') as f:
        f.write(mensagem)

def numero_aleatorio(numero1, numero2):
    return random.randint(numero1, numero2)

def tempo_de_jogo(old):
    new = ticks_us()
    delta = abs(new - old)
    old = new
    return (delta, old)

import sys
def loop(func):
    old = ticks_us()
    while True:
        delta, old = tempo_de_jogo(old)
        try:
            func(delta)
        except Exception as e:
            with open('error.log', 'w') as f:
                sys.print_exception(e, f)
            sys.exit('error')
