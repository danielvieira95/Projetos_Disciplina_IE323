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
tft.fill(TFT.BLACK)  # Preenche a tela com preto

# Configuração do pino para controle do backlight
backlight = Pin(10, Pin.OUT)
backlight.value(1)  # Ativa o backlight

# Exemplo: Escrevendo texto na tela
tft.text((10, 10), "BitDogLab V5", TFT.WHITE, sysfont)
tft.text((10, 30), "ST7735 Display", TFT.GREEN, sysfont)

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
