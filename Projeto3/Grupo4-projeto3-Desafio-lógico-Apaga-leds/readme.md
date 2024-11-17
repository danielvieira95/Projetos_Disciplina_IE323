# Desafio lógico - Apague os LEDs

Este projeto tem como seu objetivo, desenvolver um jogo interativo que estimule a memória e o raciocínio lógico dos jogadores. O desafio do jogo é apagar todos os LEDs de uma matriz 5x5, onde a cada clique em um LED, ele e seus LEDs adjacentes alternam entre aceso e apagado. O jogador precisa encontrar a sequência correta de cliques para que todos os LEDs fiquem apagados simultaneamente.

### Autores

Gelson de Barros Ferreira, RA: 212732  
Wallif Campos alves de Souza, RA: 290031

## Funcionalidades

- Matriz de LEDs WS2812B 5x5: Para exibir o estado dos LEDs no jogo.
- Joystick KY023: Para capturar a entrada do jogador e identificar o LED a ser ativado.
- Display OLED 128x64 com I2C: Para mostrar instruções e status do jogo.
- Display LCD TFT 128x160 : Para mostrar a resolução do nível atual e detalhes e instruções inicias. 
- Botões: Para permitir funcionalidades adicionais, como reset e navegação no jogo.
- Buzzers: Para fornecer feedback sonoro ao jogador durante a interação.

## Componentes Necessários
- Placa BitDogLab V5
- Display LCD TFT 1.8" 128*RGB*160
  
### Ou ainda pode ter componentes separados como:
  - Raspberry Pi Pico W
  - Matriz de LEDs WS2812B (5x5)
  - Display OLED 128x64 (I2C)
  - Joystick analógico KY-023
  - Display LCD TFT 1.8" 128*RGB*160
  - 2 Botões
  - 2 Buzzers passivos
  - Resistores, jumpers e uma placa de prototipagem


Me guiando neste esquema de ligações, mas ficar atento com a pinagem da bitdoglab de acordo com a versão de cada placa.

![Esquema de ligação](https://github.com/user-attachments/assets/12d94c46-1bfd-4142-b416-6c75f2d2dbad)

No meu caso é PCB da BitDogLab é da versão 5 que igual este conector

![copnector IDC macho da BitDogLab V5](https://github.com/user-attachments/assets/8f7299b2-dda5-4b00-ba58-591bc7e0cb60)

Ligação  entre o display LCD TFT 128XRGB160 com BitDogLab foi esta:


LCD TFT 128x160 | Bitdoglab
--------- | ------
BL        | GP10/GP8
CS        | GP17
DC        | GP16
RST       | GP20
SDA       | GP19
SCL       | GP18
VCC       |  3V3
GND       |   GND

Na ligação BL pode ser GP10 ou GP8.

## Estrutura do Projeto

- `raiz`: main.py Código-fonte do projeto.
- `raiz`: ST7735.py, sysfont.py e ssd1306.py que são biblioteca necessária para o projeto.
	* ssd1306.py auxilia no display oled
	* ST7735.py auxilia no display LCD TFT 128*RGB160
	* sysfont.py auxilia nas fontes de letras para display LCD TFT
- `docs/`: Documentação técnica, documentação do usuário
- `README.md`: Este arquivo.


Links de referência das bibliotecas:
* [sysfont](https://github.com/GuyCarver/MicroPython/blob/master/lib/sysfont.py)
* [ST7735](https://github.com/boochow/MicroPython-ST7735/issues/9
)
* [ST7735](https://github.com/boochow/MicroPython-ST7735/tree/master)
* [BitDogLab](https://github.com/BitDogLab/BitDogLab/commit/db2704d02596209923995fc20823b8b6147ad800
)




## Como Executar

1. Instale as dependências: Certifique-se de que todas as bibliotecas necessárias estão instaladas no Raspberry Pi Pico

2. Usa a conexão apropriada dos componentes segundo diagrama de conexão hardware.

3. Carregue o código: Use a IDE do VScode para carregar o código main.py no Raspberry Pi Pico.

4. Inicie o jogo: Assim que o código estiver rodando, siga as instruções no display OLED para iniciar e jogar.

