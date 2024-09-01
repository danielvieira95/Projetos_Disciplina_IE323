# Jogo de Quiz de Cores

Este projeto é um jogo interativo de interpretação e seleção de cores, desenvolvido para a plataforma BitDogLab V5, utilizando um microcontrolador Raspberry Pi Pico. O objetivo do jogo é reproduzir a cor mostrada na matriz de LEDs ajustando os valores RGB (vermelho, verde, azul) com um joystick.

## Funcionalidades

- Matriz de LEDs RGB (5x5): Mostra a cor que o jogador deve reproduzir.
- Display OLED: Exibe instruções e feedback durante o jogo.
- Joystick: Permite navegar entre os valores RGB e ajustá-los.
- Botões e Buzzers: Interagem com o jogo, fornecendo feedback sonoro para ações corretas ou incorretas.

## Componentes Necessários

- Raspberry Pi Pico
- Matriz de LEDs WS2812B (5x5)
- Display OLED 128x64 (I2C)
- Joystick analógico KY-023
- 2 Botões
- 2 Buzzers passivos
- Resistores, jumpers e uma placa de prototipagem

## Como Executar

1. Instale as dependências: Certifique-se de que todas as bibliotecas necessárias estão instaladas no Raspberry Pi Pico.

2. Conecte os componentes: Utilize o diagrama de pinos incluído na pasta diagrams para conectar todos os componentes corretamente.

3. Carregue o código: Use a IDE do Arduino ou Thonny para carregar o código jogo_quiz_cores.py no Raspberry Pi Pico.

4. Inicie o jogo: Assim que o código estiver rodando, siga as instruções no display OLED para iniciar e jogar.

## Estrutura do Projeto

- `src/`: Código-fonte do projeto.
- `diagrams/`: Diagramas de conexão de hardware.
- `docs/`: Documentação técnica e do usuário.
- `README.md`: Este arquivo.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

Citations:
[1] https://picockpit.com/raspberry-pi/pt/gaming-on-the-raspberry-pi-pico/
[2] https://github.com/penguintutor/pico-lcd-quiz
[3] https://www.youtube.com/watch?v=nd5Rd9SnRkc
[4] https://www.robocore.net/placa-raspberry-pi/raspberry-pi-pico
[5] https://www.youtube.com/watch?v=RxQg9iFc0sc
[6] https://portalescolarmaker.com.br/makey-makey-quiz-cores/
[7] https://www.raisa.com.br/placa-raspberry-pi-pico-com-microcontrolador-dual-core
