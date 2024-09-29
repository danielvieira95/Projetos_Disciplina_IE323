from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import gc

# Inicia o I2C, passando os pinos de SCL e SDA
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
# Captura o oled no I2C
oled = SSD1306_I2C(128, 64, i2c)

# Variavel para armazenar o texto atualmente sendo mostrado
texto_atual = []
# Variavel para armazenar o texto previamente mostrado na tela
texto_antigo = []

# Essa função limpa a tela
def limpar_tela():
    global texto_atual
    texto_atual = []
    oled.fill(0)

# Essa função salva o texto previamente mostrado na tela
def salvar_texto_antigo():
    global texto_antigo
    texto_antigo = texto_atual

# Essa função carrega o texto previamente mostrado na tela na tela novamente
def carregar_texto_antigo():
    limpar_tela()
    for i in texto_antigo:
        escrever_tela(*i)
    mostrar_tela()

# Essa função recebe um texto e uma posição X, Y e escreve seu valor na tela
def escrever_tela(texto, x, y):
    global texto_atual
    texto_atual.append((texto, x, y))
    oled.text(texto, x, y)

# Essa função atualiza a a tela
def mostrar_tela():
    oled.show()

def explosao_oled():
    '''roda animação de explosão'''
    play_pbm('explosion.pbm')

def agua_oled():
    '''roda animação de agua'''
    play_pbm('watersplash.pbm')

def read_until(f, end_value):
    '''lê bytes de um arquivo até encontrar o valor end_value
    retorna os bytes lidos'''
    byte = f.read(1)
    ret = []
    while byte and byte != end_value:
        ret.append(byte)
        byte = f.read(1)
    return b''.join(ret)

def play_pbm(arquivo, duracao_frame=15):
    '''exibe um ou multiplos frames de um arquivo pbm'''
    f = open(arquivo, 'rb')
    linebreak = b'\n' # valor em byte da quebra de linha
    value = 1
    while value:
        # lê a primeira linha do pbm corresponde ao tipo de pbm
        value = read_until(f, linebreak)

        # verificar se o arquivo acabou
        if not value:
            return

        # verificar que imagem está no formato correto
        if value != b'P4':
            raise(Exception('arquivo inválido precisa ser no formato P4'))

        # ler tamanho da imagem
        value = read_until(f, linebreak)
        # verificar se o arquivo acabou
        if not value:
            raise(Exception('arquivo em formato estranho'))
        x,y = map(int,value.split())

        # ler imagem
        end = x*y//8 # cada bit representa um pixel por isso dividimos pelo valor de bits em um byte para obter a quantidade de bytes até o final da imagem
        buffer = bytearray(f.read(end))

        # exibir imagem no display oled
        fb = framebuf.FrameBuffer(buffer, x, y, framebuf.MONO_HLSB)
        del x
        del y
        del buffer
        oled.fill(0)
        oled.blit(fb, 8, 0)
        del fb
        oled.show()
        utime.sleep_ms(duracao_frame)
        gc.collect()
    f.close()
