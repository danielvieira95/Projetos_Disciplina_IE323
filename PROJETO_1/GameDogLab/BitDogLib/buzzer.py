from machine import Pin, PWM
import time

buzzer = PWM(Pin(21))

def som_morreu():
    # Sequência de notas
    melody = [200, 50]
    
    # Ritmo para cada nota
    tempo = [50, 50, 50, 50]  # tempo em milissegundos
    
    # Reprodução das notas
    for i in range(len(melody)):
        buzzer.freq(melody[i])
        buzzer.duty_u16(20000)
        time.sleep(tempo[i] / 1000)
        buzzer.duty_u16(0)
        time.sleep(10 / 1000)  # pausa breve entre as notas
