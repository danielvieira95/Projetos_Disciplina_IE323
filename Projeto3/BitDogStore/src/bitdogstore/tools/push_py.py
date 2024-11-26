if __name__ != "__main__":
    from . import ampy
import os
import textwrap

#Carregar um arquivo python na placa
def push(file, destine, device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    with open(file, 'rb') as f:
        file_manager.put(destine, f.read())

#Carregar uma pasta na placa
def mkdir(dir, device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    file_manager.mkdir(dir, True)

#Remover um arquivo da placa
def rm(path, device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    file_manager.rm(path)

def execute(command ,device):
    board = ampy.pyboard.Pyboard(device)
    board.enter_raw_repl()
    board.exec_(textwrap.dedent(command))
    board.exit_raw_repl()
    
def clean_leds(device):
    command = '''
    from machine import Pin, SoftI2C
    from ssd1306 import SSD1306_I2C
    import neopixel
    
    # Inicia o I2C, passando os pinos de SCL e SDA
    i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
    # Captura o oled no I2C
    oled = SSD1306_I2C(128, 64, i2c)
    
    # Essa função limpa a tela
    oled.fill(0)
    
    # Número de LEDs na sua matriz 5x5
    ROW_SIZE = 5
    COL_SIZE = 5
    NUM_LEDS = ROW_SIZE * COL_SIZE
    
    # Inicializar a matriz de NeoPixels no GPIO7
    # A Raspberry Pi Pico está conectada à matriz de NeoPixels no pino GPIO7
    
    # lib
    # mapeia os indicies em uma matriz para utilização mais intuitiva
    LED_MAP = [[i for i in range(j*COL_SIZE+COL_SIZE-1,j*COL_SIZE-1, -1)]
        if j % 2 == 0
        else [i for i in range(j*COL_SIZE, j*COL_SIZE+COL_SIZE)]
        for j in range(0,ROW_SIZE)]
        
    np = neopixel.NeoPixel(Pin(7), NUM_LEDS)
    
    i = 0
    while i < 5:
        j = 0
        while j < 5:
            off = [0,0,0]
            indice = LED_MAP[j][i]
            np[indice] = off
            j = j + 1
        i = i + 1
    np.write()
    '''
    execute(command, device)
    
def remove_dir(device):
    command = """
        try:
            import os
        except ImportError:
            import uos as os
                
        def remove_all(path="."):
            try:
                for entry in os.listdir(path):
                    full_path = f"{path}/{entry}"
                    if os.stat(full_path)[0] & 0x4000:  # Check if it's a directory
                        remove_all(full_path)  # Recursively remove contents
                        os.rmdir(full_path)  # Remove the directory itself
                    else:
                        os.remove(full_path)  # Remove the file
            except Exception as e:
                pass
        remove_all()
    """
    execute(command, device)

#Remover uma pasta da placa
def rmdir(dir, device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    file_manager.rmdir(dir)

#Listar arquivos na placa
def ls(device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    return file_manager.ls(long_format=False,recursive=True)

#Listar arquivos na placa
def ls_dir(dir,device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    return file_manager.ls(directory=f'/{dir}', long_format=False,recursive=True)
    
#Carregar um arquivos da placa
def get(file, device):
    board = ampy.pyboard.Pyboard(device)
    file_manager = ampy.files.Files(board)
    return file_manager.get(file)

def get_default_firmware():
    file_path = os.path.realpath(__file__)
    file_path = file_path.removesuffix('push_py.py')
    return os.path.join(file_path,'default.uf2')
    
if __name__ == "__main__":
    import ampy
    remove_dir('/dev/ttyACM0')