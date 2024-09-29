# Esse módulo falcilita a comunicação WiFi, quando feita entre apenas 2 BitDogLabs

import network
import socket
import time
import json
import _thread
from utime import ticks_ms, sleep
from .utils import reiniciar
from .led import carinha_triste
from .oled import limpar_tela, mostrar_tela, escrever_tela


# A variável fila será usada para adicionar as mensagens que chegam
fila = []
# Objeto network
wlan = network.WLAN()
# Objeto conexão
conn = socket.socket()
# A variável pacote será utilizada como ID dos pacotes enviados
pacote = 0
# Essa variável armazena o ID das mensagens que chegam, seu objetivo é 
# controle de mensagens repetidas
pacotes_recebidos = []

# Essa função inicia a BitDogLab como servidor
def iniciar_servidor(ssid:str, senha:str, grupo:int):
    global wlan
    # Uma vez que grupo representa o primeiro trio do IP, ele apenas pode ser de 0 à 255
    if grupo < 0 or grupo > 255:
        print('grupo inválido')
        reiniciar()
    print('Iniciando Server')
    # Configura o BitoDogLab como servidor
    wlan = network.WLAN(network.AP_IF)
    # Adiciona nome da rede e senha do servidor
    wlan.config(essid=ssid, password=senha)
    # Inicia a rede
    wlan.active(True)
    # Adiciona as configurações necessárias para a rede
    wlan.ifconfig((f'{grupo}.200.200.1', '255.255.255.252','0.0.0.0','0.0.0.0'))
    print('Ponto de Acesso Ativo:', wlan.ifconfig())

# Essa função abre a porta 8080 e espera pela conexão
def servidor_conectar():
    global conn
    # Aceita conexão de qualquer IP na porta 8080
    addr = socket.getaddrinfo('0.0.0.0', 8080)[0][-1]
    # Inicia socket
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    print('Aguardando conexão...')
    conn, addr = server_socket.accept()
    print('Cliente conectado:', addr)

# Essa função inicia a BitDogLab como cliente
def cliente_conectar(ssid:str, senha:str, grupo:int):
    global wlan, conn
    # Uma vez que grupo repreta o primeiro trio do IP, ele apenas pode ser de 0 à 255
    if grupo < 0 or grupo > 255:
        print('grupo inválido')
        reiniciar()
    print('Iniciando Client')
    # Configura a BitDogLab como cliente
    wlan = network.WLAN(network.STA_IF)
    # Inicia a rede
    wlan.active(True)
    # Adiciona as configurações necessárias para a rede
    wlan.ifconfig((f'{grupo}.200.200.2', '255.255.255.252','0.0.0.0','0.0.0.0'))
    print('Cliente Ativo:', wlan.ifconfig())
    wlan.connect(ssid, senha)
    
    # Aguarda conexão ao servidor
    while True:
        # se não conseguir estabelecer a conexão em 7 segundos reiniciamos a conexão
        for i in range(7):
            print("Tentando conectar")
            # se a conexão estiver estabelicida não precisamos esperar o resto dos 7 segundos
            if wlan.isconnected():
                break
            time.sleep(1)
        # se a conexão estiver estabelicida saimos do loop
        if wlan.isconnected():
            break
        print('Tentando novamente')
        # reiniciar conexão do zero
        del wlan
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.ifconfig((f'{grupo}.200.200.2', '255.255.255.252','0.0.0.0','0.0.0.0'))
        wlan.connect(ssid, senha)

    # Conecta ao servidor
    addr = socket.getaddrinfo(f'{grupo}.200.200.1', 8080)[0][-1]
    print('Conectado ao AP:', addr)
    conn = socket.socket()
    conn.connect(addr)
    print('Conectado ao AP:', addr)

# Essa função consiste de um loop infinito que espera receber mensagens, e ao receber adiciona a
# fila e aos pacotes_recebidos. 
# A função somente aceita mensagem em JSON. 
# Por padrão o tamanho do buffer(tamanho da mensagem que consegue receber) é de 1KB
def receber_via_wifi(tamanho_buffer = 1024):
    global conn
    global pacote
    global fila
    global pacotes_recebidos
    while True:
        print('Esperando dados...')
        # Espera por receber uma mensagem com tamanho máximo igual a tamanho_buffer
        data = conn.recv(tamanho_buffer)
        # Decodifica a mensagem para UTF-8 e remove espaços no começo ou final
        pck = data.decode('utf-8').strip()
        print(f"Recebido: {pck}")
        try:
            # Converte a mensagem de JSON para um formato que o python entenda
            pck = json.loads(pck)
            # Se não recebeu um pacote com esse ID ainda (não está nos pacotes_recebidos), 
            # adiciona na fila e nos pacotes_recebidos
            if not pck[0] in pacotes_recebidos:
                fila.append(pck)
                pacotes_recebidos.append(pck[0])
            # Se o pacote recebido não é um ACK então envia um ACK
            if pck[2] != 1:
                enviar_ack([pck[0]])
                # Incrementa em 1 o ID que será usado na próxima mensagem que enviará
                pacote += 1
        except:
            # Caso o dado não for válido será ignorado
            print(f'Dado Invalido {pck}')

# Essa função envia uma mensagem
def enviar_via_wifi(msg:list):
    global conn
    global pacote
    # A mensagem é formada por um ID, a mensagem e a flag que indica se é um ACK
    msg = [pacote, msg, 0]
    # A mensagem é convertida para JSON
    pck = f'{json.dumps(msg)}\n'
    # Id do pacote que será enviado
    pacote_enviado = pacote
    # Enviará a mensagem, esperará 1s, caso não recebeu um ACK, envia denovo
    while True:
        # Envia a mensagem codificada em UTF-8
        conn.send(pck.encode())
        print('Enviado:', pck)
        sleep(1)
        msg_recebida = ler_ack()
        # Se um ACK foi enviado para a mensagem que está enviando então saia do Loop
        if len(msg_recebida) > 0 and msg_recebida[1][0] == pacote_enviado:
            print('ACK Recebido')
            break
            
    # Incrementa em 1 o ID que será usado na próxima mensagem que enviará
    pacote += 1

# Essa função envia um ACK
def enviar_ack(id_pacote_recebido:list):
    global conn
    global pacote
    
    # A mensagem é formada por um ID, ID do pacote recebido e a flag que indica se é um ACK
    msg = [pacote, id_pacote_recebido, 1]
    # A mesnagem é convertida para JSON
    pck = f'{json.dumps(msg)}\n'
    # Envia a mensagem codificada em UTF-8
    conn.send(pck.encode())
    # Incrementa em 1 o ID que será usado na próxima mensagem que enviará
    pacote += 1
    print('Enviado ACK:', pck)
    
# Essa função verifica se tem alguma mensagem na fila, se tiver retorna o primeiro elemento e o 
# remove da fila, senão retorna uma lista vazia
def ler_wifi() -> list:
    global fila
    if len(fila) > 0:
        return fila.pop(0)
    return []

# Essa função verifica se tem algum ACK na fila, se tiver a retorna e a remove da fila,
#  senão retorna uma lista vazia
def ler_ack()->list:
    global fila
    for i,msg in enumerate(fila):
        if msg[2] == 1:
            return fila.pop(i)
    return []

def teste_forca_wifi():
    return wlan.status('rssi')

# Essa função faz com que a thread principal espere por uma mensagem, ela verifica se 
# tem uma nova mensagem a cada 2s. Além disso também verifica se a conexão não foi perdida
def esperar_receber():
    global wlan
    old = ticks_ms()
    while True:
        # print(wlan.status('rssi'))
        new = ticks_ms()
        if new - old >= 2000:
            old = new
            # Verifica se perdeu a conexão
            if not wlan.isconnected():
                print(f'Conexão Perdida')
                carinha_triste((10,0,0))
                limpar_tela()
                escrever_tela('Conexão Perdida', 0, 0)
                mostrar_tela()
                desligar_wifi()
                sleep(1)
                reiniciar()
        
        # Obtem o 1 item da fila, se não houver nada na fila recebe uma lista vazia
        dado = ler_wifi()
        # Se houver uma mensagem, e ela não for um ACK, então a retorne
        if len(dado) > 0 and dado[2] != 1:
            return dado[1]

# Para uma conexão WiFi acontecer precisa de um servidor e um cliente
# Essa função recebe o grupo(primeiro trio do IP) e se é um servidor
# Então inicializa-o corretamete, Mostrando no OLED informações necessárias   
def definir_servidor_ou_cliente(grupo:int, is_servidor:bool):
    
    # Defini nome da rede
    ssid = f'BitDogLab_{grupo}'
    # Defini a senha da rede
    senha = f'BitDogLab_{grupo}'
    
    # Caso for um servidor, inicia como um servidor
    if is_servidor:
        limpar_tela()
        escrever_tela("Aguardando", 0, 0)
        escrever_tela("Conexao", 0, 10)
        mostrar_tela()
        iniciar_servidor(ssid, senha, grupo)
        servidor_conectar()
    # Caso não for um servidor, inicia como cliente
    else:        
        limpar_tela()
        escrever_tela("Tentando", 0, 0)
        escrever_tela("Conectar", 0, 10)
        mostrar_tela()
        cliente_conectar(ssid, senha, grupo)
    # Inicia no segundo core a função receber_via_wifi
    _thread.start_new_thread(receber_via_wifi, ())
    limpar_tela()
    escrever_tela("Conexao", 0, 0)
    escrever_tela("Estabelecida", 0, 10)
    mostrar_tela()
        
# Essa função desliga o WiFi
def desligar_wifi():
    wlan.active(False)
    print('Wi-Fi Desligado')
