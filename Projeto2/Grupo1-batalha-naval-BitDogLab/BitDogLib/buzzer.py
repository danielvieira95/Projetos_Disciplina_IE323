from machine import Pin, PWM
import time

# Indica que o buzzer esta no pino PWM 21
buzzer = PWM(Pin(21))

# Essa função toca um som de morte
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
        
    buzzer.deinit()  # Desliga o buzzer

# Essa função toca um som de explosão
def som_explosao():
    explosion_tones = [100, 150, 200, 250, 300, 200, 100]

    for tone in explosion_tones:
        buzzer.freq(tone)
        buzzer.duty_u16(32768) 
        time.sleep(0.1)  # pausa breve entre as notas

    buzzer.deinit()  # Desliga o buzzer

# Essa função toca um som de agua
def som_agua():
    tones = [800, 600, 400, 300, 200, 100, 50]

    for tone in tones:
        buzzer.freq(tone)
        buzzer.duty_u16(32768)  
        time.sleep(0.05)  # pausa breve entre as notas

    buzzer.deinit()  # Desliga o buzzer