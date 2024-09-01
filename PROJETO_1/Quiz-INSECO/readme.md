# Jogo de Quiz de Cores

Este projeto é um jogo interativo de interpretação e seleção de cores, desenvolvido para a plataforma BitDogLab V5, utilizando um microcontrolador Raspberry Pi Pico. O objetivo do jogo é reproduzir a cor mostrada na matriz de LEDs ajustando os valores RGB (vermelho, verde, azul) com um joystick.

## Funcionalidades

- Matriz de LEDs RGB (5x5): Mostra a cor que o jogador deve reproduzir.
- Display OLED: Exibe instruções e feedback durante o jogo.
- Joystick: Permite navegar entre os valores RGB e ajustá-los.
- Botões e Buzzers: Interagem com o jogo, fornecendo feedback sonoro para ações corretas ou incorretas.

## Componentes Necessários
- Placa BitDogLab V5
Ou ainda podes ter o componentes separados como:
- Raspberry Pi Pico
- Matriz de LEDs WS2812B (5x5)
- Display OLED 128x64 (I2C)
- Joystick analógico KY-023
- 2 Botões
- 2 Buzzers passivos
- Resistores, jumpers e uma placa de prototipagem

## Como Executar

1. Instale as dependências: Certifique-se de que todas as bibliotecas necessárias estão instaladas no Raspberry Pi Pico.

2. Usa a conexão apropriada dos componentes segundo diagrama de conexão hardware.

3. Carregue o código: Use a IDE do VScode para carregar o código main.py no Raspberry Pi Pico.

4. Inicie o jogo: Assim que o código estiver rodando, siga as instruções no display OLED para iniciar e jogar.

## Estrutura do Projeto

- `raiz`: Código-fonte do projeto.
- `docs/`: Documentação técnica e do usuário.
- `README.md`: Este arquivo.
  
## Diagramas de conexão de hardware
Usando Conexões e Configurações de Hardware existente na plataforma bitdoglab são este conexão que temos:
Um botão, identificado como Botão A, está conectado no GPIO5 da Raspberry Pi Pico. O outro terminal do botão está conectado ao GND da placa. 
Outro botão, identificado como Botão B, está conectado no GPIO6 da Raspberry pi pico. O outro terminal do botão também está conectado ao GND da placa.
Um buzzer passivo, identificado como Buzzer A, está conectado - através de um transistor - no GPIO21 da Raspberry pi pico.
Outro buzzer passivo, identificado como Buzzer B, está conectado no GPIO10 da Raspberry pi pico.
O pino in de uma matriz de LEDs 5050 RGB de 5 linhas por 5 colunas tipo WS2812B (Neopixel) está conectada ao GPIO7. 
Um joystick analógico tipo KY023 tem a saída VRy conectada ao GPIO26 e a saída VRx ao GPIO27. Seu botão SW está conectada ao GPIO22, o outro terminal do botão está no GND. 
Um display OLED 128 colunas por  x 64 linhas de 0,96 polegadas com comunicação I2C, tem seu pino SDA conectado ao GPIO14 e o pino SCL com o GPIO15, estes pinos são do canal I2C0. Esse display (normalmente configurado no endereço 0x3C).

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
