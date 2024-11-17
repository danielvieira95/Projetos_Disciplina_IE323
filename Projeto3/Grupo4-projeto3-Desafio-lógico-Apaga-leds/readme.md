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


Estou usando as seguintes bibliotecas externa em Python: ST7735  e sysfont
Me guiando neste esquema de ligações, mas ficar atento com a pinagem da bitdoglab de acordo com a versão de cada placa.

	![Esquema de ligações](https://github.com/danielvieira95/Projetos_Disciplina_IE323/blob/main/Projeto3/Grupo4-projeto3-Desafio-l%C3%B3gico-Apaga-leds/img/img1.png)


No meu caso é versão 5 que igual este esquema.


ligação que eu usei


LCD TFT 128x160 | Bitdoglab
--------- | ------
BL        | GP10/GP08
CS        | GP17
DC        | GP16
RST       | GP20
SDA       | GP19
SCL       | GP18
VCC       |  3V3
GND       |   GND

