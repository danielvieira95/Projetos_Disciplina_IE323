import serial.tools.list_ports

PID_MICRO_PYTHON = 0x0005
# VID da rapsberry pi pico e pico w
VID = 0x2E8A

# Busca por todas as portas com o VID da rapsberry pi pico e pico w
def find_pico_porta():
    portas = serial.tools.list_ports.comports()
    return [porta for porta in portas if VID == porta.vid]

# Verifica se a porta dada está com o firmware de micropython
def is_micropython(porta):
    return porta.pid == PID_MICRO_PYTHON
    
# Busca por uma porta
def find_porta(device_path):
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        if porta.device == device_path:
            return porta