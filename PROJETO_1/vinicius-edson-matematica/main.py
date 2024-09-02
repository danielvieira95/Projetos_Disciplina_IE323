from machine import Pin, ADC, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
import neopixel, time, utime
from pergunta_resposta import Question

# ==========================  INICIALIZACAO DE PERIFERICOS =========================
adc_vrx = ADC(Pin(26)) # inicializa pino VRx (GPIO26)
adc_vry = ADC(Pin(27)) # inicializa pino VRx (GPIO27)
button_a = Pin(5, Pin.IN, Pin.PULL_UP) # configura botao A
button_b = Pin(6, Pin.IN, Pin.PULL_UP) # configura botao B
i2c = SoftI2C(scl=Pin(15), sda=Pin(14)) # configura Display oled no GP14
oled = SSD1306_I2C(128, 64, i2c) # configura Display oled 128x64 pixels
NUM_LEDS = 25 # Número de LEDs na sua matriz 5x5
np = neopixel.NeoPixel(Pin(7), NUM_LEDS) # Inicializa matriz LEDs no GPIO7
alto_falante = PWM(Pin(21)) # inicializa buzzer passivo no pino GP4
# ==========================  INICIALIZACAO DE PERIFERICOS =========================

# ============================  DEFINIÇÃO DE CONSTANTES ============================
cont_pergunta=0
lista_pergunta = [0,1,2,3,4]

# Referencia para matriz de LEDs, Atenção, é um Zig-Zag!!
#  4, 3, 2, 1, 0
#  5, 6, 7, 8, 9
# 14,13,12,11,10
# 15,16,17,18,19
# 24,23,22,21,20

# LEDS das Alternativas
A = [23,2,21,16,13,6,3,18,11,8,1,12]
B = [23,22,21,16,13,6,3,18,8,1,12,2]
C = [23,22,21,16,13,6,3,1,2]
D = [23,22,16,13,6,3,18,11,8,2]
E = [23,22,21,16,13,6,3,1,12,2]

alternativa = [A,B,C,D,E]

#Dicionário para escolha das alternativas corretas
resposta = {'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4}

#Leds correspondente ao rostinho feliz e triste na Matriz de Leds
rosto_feliz = [6,8,15,23,22,21,19]
rosto_triste = [6,8,24,16,17,18,20]

# Frequências das notas musicais (escala temperada)
notas = {
    'C4': 261,
    'E4': 329,
    'G4': 392,
    'G3': 196  # Sol uma oitava abaixo
}

# Música "Super Mario Bros" - Parte Inicial
musica_super_mario = [
    ('E4',6),('E4',8),('E4',10),('C4',4),('E4',11),('G4',24),('G3',16)]
tempo_mario = 24
volume = 1000 # Era 32768
# ===========================  DEFINIÇÃO DE CONSTANTES =========================


# ==========================  FUNCOES PARA APRESENTACAO =========================
def tocar_musica(musica):
    for nota, duracao in musica:
        freq = notas[nota]
        alto_falante.freq(freq)
        alto_falante.duty_u16(volume if freq > 0 else 0) # era 32768
        time.sleep_ms(tempo_mario*duracao)  # Controla a duração das notas
        alto_falante.duty_u16(0)
        time.sleep_ms(50)  # Pequena pausa entre as notas

# Funcoes da apresentacao
def limpa_matriz_leds():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
        np.write()

def preenche_matriz_led_zig_zag():
    for i in range(NUM_LEDS):
        np[i] = (2, 2, 2)
        np.write()
        time.sleep(0.045)

def ola_aluno_bem_vindo():
    oled.fill(0)  # Limpar display
    oled.text("OLA, ALUNO!", 0, 0)
    oled.text("BEM VINDO!", 0, 10)
    oled.show()

def letra_m():
    mat = [24,15,14,5,4,6,12,8,0,9,10,19,20]
    for i in mat:
        np[i] = (0,2,0)
        np.write()
        time.sleep(0.1)

def rosto_feliz_piscando():
    for i in rosto_feliz:
        np[i] = (0,2,0)
        np.write()
    time.sleep(0.5)
    # Piscada
    np[6] = (0,0,0)
    np.write()
    time.sleep(0.2)
    np[6] = (0,2,0)
    np.write()
# ==========================  FUNCOES PARA APRESENTACAO =========================


# ===========================  SEQUENCIA DE APRESENTAÇÃO ========================
limpa_matriz_leds()
preenche_matriz_led_zig_zag()
ola_aluno_bem_vindo()
tocar_musica(musica_super_mario)
letra_m()
limpa_matriz_leds()
rosto_feliz_piscando()
time.sleep(3)

# ===========================  SEQUENCIA DE APRESENTAÇÃO ========================


# =============================  PERGUNTAS E RESPOSTAS ==========================

pergunta = Question(25)
resp = Question(25)

# =============================  PERGUNTAS E RESPOSTAS ==========================


# ===========================   ESCOLHA DAS ALTERNATIVAS =========================
def contagem(eixo_y):
    global cont_pergunta
    
    if eixo_y < 20000:
        cont_pergunta+=1
        if cont_pergunta>4:
            cont_pergunta=0
    elif eixo_y > 40000:
        cont_pergunta-=1
        if cont_pergunta<0:
            cont_pergunta=4
    return cont_pergunta  

def rosto_feliz_desenho():
    for i in rosto_feliz:
        np[i]=(0,2,0)
        np.write()
    oled.fill(0)
    oled.text("ACERTOOUUU",0,0)
    oled.show()  
    time.sleep(2)
    limpa_matriz_leds()
        
def rosto_triste_desenho():
    for i in rosto_triste:
        np[i]=(2,0,0)
        np.write()
        
    oled.fill(0)
    oled.text("ERROOUUUU",0,0)
    oled.show()  
    time.sleep(2)
    limpa_matriz_leds()

def desenha_alternativa(question):
    for i in alternativa[question]:
        np[i] = (0, 2, 0)
        np.write()
  
def opcoes(num_da_questao, alternativa_correta):
    escolha = True
    while escolha:
    # Ler valores analógicos de VRx e VRy
        vrx_value = adc_vrx.read_u16()
        vry_value = adc_vry.read_u16()
        b = contagem(vry_value)

    # Desligar todos os LEDs
        limpa_matriz_leds()
        desenha_alternativa(b)
        resp.opcoes_oled(num_da_questao,b)
            
        if button_a.value() == 0:
            limpa_matriz_leds()
            if b==alternativa_correta:
                rosto_feliz_desenho()
            else:
                rosto_triste_desenho()
            escolha = False        
        if button_b.value() == 0:
            escolha = False
    # Esperar um pouco antes da próxima leitura
        time.sleep(0.1)
# ===========================   ESCOLHA DAS ALTERNATIVAS =========================


# ============================== INTERFACE PRINCIPAL==============================

respostas_corretas = ['A','C','B','E','D'] # Aqui escolhemos a sequência de respostas corretas da questão de 1 a 5

correct = [resposta[respostas_corretas[0]],
           resposta[respostas_corretas[1]],
           resposta[respostas_corretas[2]],
           resposta[respostas_corretas[3]],
           resposta[respostas_corretas[4]]]

def mostrando_pergunta(question):
    if question==0:
        pergunta.pergunta01()
        opcoes(question, correct[0])  # o parametro em opções corresponde a alternativa correta
    elif question==1:
        pergunta.pergunta02()
        opcoes(question, correct[1]) # o parametro em opções corresponde a alternativa correta
    elif question==2:
        pergunta.pergunta03()
        opcoes(question, correct[2]) # o parametro em opções corresponde a alternativa correta
    elif question==3:
        pergunta.pergunta04()
        opcoes(question, correct[3]) # o parametro em opções corresponde a alternativa correta
    elif question==4:
        pergunta.pergunta05()
        opcoes(question, correct[4]) # o parametro em opções corresponde a alternativa correta
        
def mensagem_menu():
        # Teste OLED
    oled.fill(0)  # Limpar display
    oled.text("PERGUNTA", 0, 0)
    oled.text("(A) Selecionar", 0, 20)
    oled.text("(B) Voltar", 0, 30)
    
def seleciona_pergunta(ordem_pergunta):
    mensagem_menu()
    for i in lista_pergunta:
        if i == ordem_pergunta:
            oled.text("Questao {}".format(ordem_pergunta+1), 0, 10)
            oled.show()
            if button_a.value() == 0:
                mostrando_pergunta(ordem_pergunta)

while True:
    # Ler valores analógicos de VRx e VRy
    vrx_value = adc_vrx.read_u16()
    vry_value = adc_vry.read_u16()
    
    num_pergunta = contagem(vry_value)
    seleciona_pergunta(num_pergunta)
    
    # Esperar um pouco antes da próxima leitura
    time.sleep(0.15)
# ============================== INTERFACE PRINCIPAL==============================
