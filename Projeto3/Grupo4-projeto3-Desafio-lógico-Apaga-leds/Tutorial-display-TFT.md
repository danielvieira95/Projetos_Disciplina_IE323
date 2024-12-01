# Tutorial para Uso do Display TFT 1.8" com BitDogLab

Este guia fornece um tutorial para configurar e usar um display TFT de 1.8" (ST7735, resolução 128x160) com a plataforma **BitDogLab** baseada no microcontrolador Raspberry Pi Pico.

## Requisitos

- **BitDogLab V5** ou similar com microcontrolador Raspberry Pi Pico.
- Display LCD TFT de 1.8" (ST7735).
- Biblioteca `ST7735.py` (disponível no repositório de referências).
- Biblioteca de fontes básicas para texto (`sysfont.py`).
- Interface SPI configurada no microcontrolador.
- Fonte de alimentação compatível com o display.

## Esquema de Ligações

| **Pino do Display** | **Função**       | **Pino no BitDogLab** |
|----------------------|------------------|------------------------|
| SCK (Clock)          | SPI Clock (SCK) | GPIO18                |
| MOSI (Data)          | SPI Data (MOSI) | GPIO19                |
| DC (Data/Command)    | Controle de DC   | GPIO16                |
| RST (Reset)          | Reset do display| GPIO20                |
| CS (Chip Select)     | Seleção do Chip | GPIO17                |
| BL (Backlight)       | Controle do LED | GPIO10                |
| VCC                  | Voltagem corrente continua|  3V3         |
| GND                  | Ground(terra) |   GND                  |
## Configuração do Software

1. **Baixe as bibliotecas necessárias**:
   - [`ST7735.py`](https://github.com/boochow/MicroPython-ST7735/tree/master)
   - [`sysfont.py`](https://github.com/GuyCarver/MicroPython/blob/master/lib/sysfont.py)

2. **Salve os arquivos** no sistema de arquivos do Raspberry Pi Pico utilizando um programa como `Thonny IDE`.

3. **Instale a biblioteca SPI** se ainda não estiver configurada.

4. **Código Exemplo**:
   - ## Para texto 
```python
from machine import Pin, SPI # Comunicação SPI e manipulação de GPIOs
from ST7735 import TFT # Biblioteca para displays TFT ST7735
from sysfont import sysfont # Fonte básica para textos no display TFT

# Configuração da interface SPI para o display
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

# Inicializa o display TFT
tft = TFT(spi, 16, 20, 17)  # pinos DC, RST, CS
tft.initr()  # Inicializa em modo padrão
tft.rgb(True)  # Define o modo de cores RGB
tft.rotation(1)  # Define a rotação de 180 graus ou seja variar de 0 - 3. Começa na vertical com o topo voltado para os pinos e gira 90 graus no sentido horário a cada passo.
tft.fill(TFT.BLACK)  # Preenche a tela com preto


# Configuração do pino para controle do backlight
backlight = Pin(10, Pin.OUT)
backlight.value(1)  # Ativa o backlight

# Exemplo: Escrevendo texto na tela
tft.text((10, 10), "BitDogLab V5", TFT.WHITE, sysfont)
tft.text((10, 30), "ST7735 Display", TFT.GREEN, sysfont)

```
   - ## Para imagem

```python
from machine import Pin, SPI
from ST7735 import TFT, TFTColor

# Configuração da interface SPI para o display
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))

# Inicializa o display TFT
tft = TFT(spi, 16, 20, 17)  # pinos DC, RST, CS
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

# Configuração do pino para controle do backlight
backlight = Pin(10, Pin.OUT)
backlight.value(1)


# Função para apresentar uma imagem no Display LCD TFT
def imagem(nome):
    try:
        f = open(f'{nome}.bmp', 'rb')  # Abre o arquivo BMP em modo leitura binária
        if f.read(2) == b'BM':  # Verifica o cabeçalho do arquivo (deve começar com "BM")
            dummy = f.read(8)  # Ignora 8 bytes (tamanho do arquivo e criador)
            offset = int.from_bytes(f.read(4), 'little')  # Lê o offset para os dados de imagem
            hdrsize = int.from_bytes(f.read(4), 'little')  # Lê o tamanho do cabeçalho
            width = int.from_bytes(f.read(4), 'little')  # Lê a largura da imagem
            height = int.from_bytes(f.read(4), 'little')  # Lê a altura da imagem
            if int.from_bytes(f.read(2), 'little') == 1:  # Verifica se o número de planos é 1
                depth = int.from_bytes(f.read(2), 'little')  # Lê a profundidade da cor (bits por pixel)
                if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:  # Verifica profundidade de 24 bits e sem compressão
                    print("Image size:", width, "x", height)  # Exibe o tamanho da imagem
                    rowsize = (width * 3 + 3) & ~3  # Calcula o tamanho de cada linha (alinhado a 4 bytes)
                    if height < 0:
                        height = -height  # Corrige altura negativa (origem na parte inferior)
                        flip = False  # Sem flip vertical
                    else:
                        flip = True  # Flip vertical
                    print(f"Exibindo imagem: {nome}.bmp ({width}x{height})")
                    w, h = width, height
                    if w > 128: w = 128  # Limita a largura máxima a 128 pixels
                    if h > 160: h = 160  # Limita a altura máxima a 160 pixels
                    tft._setwindowloc((0, 0), (w, h))  # Configura a janela de exibição no TFT
                    
                    for row in range(h):  # Para cada linha da imagem
                        if flip:
                            pos = offset + row * rowsize  # Posição da linha com flip
                        else:
                            pos = offset + (height - 1 - row) * rowsize  # Posição da linha sem flip
                        
                        if f.tell() != pos:  # Move o cursor para a posição correta
                            f.seek(pos)
                        
                        line = f.read(rowsize)[:width * 3]  # Lê os dados da linha (até a largura necessária)
                        
                        for col in range(w - 1, -1, -1):  # Processa pixels da direita para a esquerda
                            bgr = line[col * 3:(col + 1) * 3]  # Obtém os componentes BGR
                            tft._pushcolor(TFTColor(bgr[2], bgr[1], bgr[0]))  # Converte para RGB e envia ao TFT

        spi.deinit()  # Finaliza a comunicação SPI
    except Exception as e:
        print("Erro ao exibir a imagem:", e)

# Exibir uma imagem
imagem("Inicio")  # Substitua "imagem" pelo nome do seu arquivo BMP (sem extensão)
```




## Ajustes no Código
Resolução do display: Certifique-se de ajustar para 128x160 no arquivo ST7735.py se necessário.
Fonte e texto: Para exibir texto, use a biblioteca sysfont.py ou fontes customizadas.

## Soluções de Problemas
Consulte o link de discussões para dúvidas comuns, como configurações de hardware ou software.
Verifique os cabos e a alimentação do display se ele não inicializar corretamente.

## Links de referência
* [ST7735](https://github.com/boochow/MicroPython-ST7735/tree/master) biblioteca ST7735.py com alguns exemplos
* [sysfont](https://github.com/GuyCarver/MicroPython/blob/master/lib/sysfont.py) biblioteca das sysfont
* [ST7735](https://github.com/boochow/MicroPython-ST7735/issues/9) link que complementa uma duvida sobre usar este biblioteca ST7735.
* [BitDogLab](https://github.com/BitDogLab/BitDogLab/commit/db2704d02596209923995fc20823b8b6147ad800) Este link da fonte da imagem dos esquema das ligações

## Créditos
Código traduzido por Guy Carver e modificado por boochow.

Integração com BitDogLab por Gelson de Barros Ferreira e Wallif Campos.

# Com este guia, você poderá iniciar facilmente o uso do display TFT de 1.8" com sua plataforma BitDogLab.
