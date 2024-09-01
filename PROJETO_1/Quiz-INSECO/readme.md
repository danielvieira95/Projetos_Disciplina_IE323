# Jogo de Quiz de interpretação e seleção de cores

Este projeto é um jogo interativo de interpretação e seleção de cores, desenvolvido com a plataforma BitDogLab V5, utilizando um microcontrolador Raspberry Pi Pico. O objetivo do jogo é tentar reproduzir a cor mostrada na matriz de LEDs ajustando os valores das variáveis RGB (vermelho, verde, azul) com um joystick.

### Autores

Gelson de Barros Ferreira, RA: 212732  
Wallif Campos alves de Souza, RA: 290031

## Funcionalidades

- Matriz de LEDs RGB (5x5): Mostra a cor que o jogador deve reproduzir.
- Display OLED: Exibe instruções e feedback durante o jogo.
- Joystick: Permite navegar entre os valores RGB, ajustá-los e selecionar para comparação.
- Buzzers: Interagem com o jogo, fornecendo feedback sonoro para ações corretas ou incorretas.
- Botões: Interagem no jogo, para feedback do inicio Botão A e recomeço do jogo Botão B

## Componentes Necessários
- Placa BitDogLab V5
  
### Ou ainda pode ter componentes separados como:
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
As conexões e configurações de hardware são as da plataforma bitdoglab que temos aqui:
- Um botão, identificado como Botão A, está conectado no GPIO5 da Raspberry Pi Pico. O outro terminal do botão está conectado ao GND da placa. 
- Outro botão, identificado como Botão B, está conectado no GPIO6 da Raspberry pi pico. O outro terminal do botão também está conectado ao GND da placa.
- Um buzzer passivo, identificado como Buzzer A, está conectado - através de um transistor - no GPIO21 da Raspberry pi pico.
- Buzzer passivo, identificado como Buzzer B, está conectado no GPIO10 da Raspberry pi pico.
- O pino in de uma matriz de LEDs 5050 RGB de 5 linhas por 5 colunas tipo WS2812B (Neopixel) está conectada ao GPIO7. 
- Um Joystick analógico tipo KY023 tem a saída VRy conectada ao GPIO26 e a saída VRx ao GPIO27. Seu botão SW está conectada ao GPIO22, o outro terminal do botão está no GND. 
- Um display OLED 128 colunas por  x 64 linhas de 0,96 polegadas com comunicação I2C, tem seu pino SDA conectado ao GPIO14 e o pino SCL com o GPIO15, estes pinos são do canal I2C0. Esse display (normalmente configurado no endereço 0x3C).

## Instruções do Jogo 

### Início do Jogo:

No display OLED, aparecerá a mensagem: "Bem-vindo ao Quiz de Cores! Clique no botão à esquerda para começar." Este botão é o Botão A no hardware.
Ao clicar no Botão A, o jogo inicia, e o display OLED exibirá: "Atenção, jogo começando." Em seguida, a mensagem "Nível: 1" será mostrada.

### Como Jogar:

No nível 1, os primeiros cinco LEDs da primeira linha da matriz 5050 RGB (posições 0 a 4) acenderão com uma cor aleatória. O objetivo é recriar essa cor ajustando manualemnte as variáveis R G B.
No display OLED, você verá a pergunta: "Crie a cor sorteada (RGB)". Conforme você ajusta os valores de R, G e B com o joystick, a cor será exibida na matriz e o valor atual será mostrado no OLED.
- Para o nível 1, há 8 combinações possíveis de cores:
* R: 0 ou 100
* G: 0 ou 100
* B: 0 ou 100
- Para o nível 2, há 27 combinações possíveis de cores:
* R: 0, 50 ou 100
* G: 0, 50 ou 100
* B: 0, 50 ou 100
- Para o nível 3, há 125 combinações possíveis de cores:
* R: 0, 25, 50, 75 ou 100
* G: 0, 25, 50, 75 ou 100
* B: 0, 25, 50, 75 ou 100

### Controles:

Use o eixo Y do joystick para alternar entre R, G e B. Use o eixo X para ajustar o valor selecionado.
Ao pressionar o botão SW do joystick, o valor ajustado será comparado com a cor exibida na matriz de LEDs.
Se a cor estiver correta, o LED na posição 24 acenderá e o display OLED mostrará "Parabéns, cor correta". Os buzzers A e B tocarão um som de acerto.
Se a cor estiver incorreta, o display OLED mostrará "Opa, está incorreto, tente de novo". Os buzzers A e B tocarão um som de erro. Você pode tentar novamente até 20 vezes antes do fim do jogo.

### Progresso no Jogo:

Após acertar, o display OLED mostrará a mensagem: "Próximo nível".
O processo será repetido para os próximos níveis até completar todos os três.

### Fim do Jogo:

Quando todos os níveis forem concluídos, o display OLED mostrará o número de erros cometidos e o tempo total para completar o jogo.
Para reiniciar, clique no botão à direita (Botão B). O display OLED exibirá: "Reiniciando o jogo".

### Folha de Respostas e curiosidade. 

Como no nivel 3 há 5 possíveis valores para cada componente (R, G, B), o número total de combinações será: 5x5x5 = 125 Cores. Sendo elas: 

(0, 0, 0)      Preto                        (0, 0, 25)    Azul Muito Escuro          (0, 0, 50)    Azul Escuro                  (0, 0, 75)    Azul Marinho              (0, 0, 100)   Azul
(0, 25, 0)     Verde Muito Escuro           (0, 25, 25)   Turquesa Escuro            (0, 25, 50)   Ciano Escuro                 (0, 25, 75)   Ciano Médio               (0, 25, 100)  Ciano
(0, 50, 0)     Verde Escuro                 (0, 50, 25)   Turquesa Médio             (0, 50, 50)   Turquesa Claro               (0, 50, 75)   Ciano Claro               (0, 50, 100)  Ciano Vivo
(0, 75, 0)     Verde Médio Escuro           (0, 75, 25)   Verde Mar                  (0, 75, 50)   Turquesa Vivo                (0, 75, 75)   Verde Água                (0, 75, 100)  Ciano Brilhante
(0, 100, 0)    Verde                        (0, 100, 25)  Verde Limão Escuro         (0, 100, 50)  Verde Limão Médio            (0, 100, 75)  Verde Limão Claro         (0, 100, 100) Ciano Puro
(25, 0, 0)     Vermelho Muito Escuro        (25, 0, 25)   Magenta Escuro             (25, 0, 50)   Roxo Escuro                  (25, 0, 75)   Roxo Médio                (25, 0, 100)  Roxo
(25, 25, 0)    Oliva Escura                 (25, 25, 25)  Cinza Escuro               (25, 25, 50)  Cinza Azulado Escuro         (25, 25, 75)  Cinza Azulado Médio       (25, 25, 100) Cinza Azulado Claro
(25, 50, 0)    Verde Oliva                  (25, 50, 25)  Verde Musgo Escuro         (25, 50, 50)  Verde Musgo                  (25, 50, 75)  Turquesa Pastel           (25, 50, 100) Ciano Pastel
(25, 75, 0)    Verde Escuro Médio           (25, 75, 25)  Verde Escuro               (25, 75, 50)  Verde Musgo Claro            (25, 75, 75)  Verde Água Médio          (25, 75, 100) Turquesa Brilhante
(25, 100, 0)   Verde Limão Escuro           (25, 100, 25) Verde Limão                (25, 100, 50) Verde Neon                   (25, 100, 75) Verde Neon Claro          (25, 100, 100) Turquesa Neon
(50, 0, 0)     Vermelho Escuro              (50, 0, 25)   Magenta Médio              (50, 0, 50)   Magenta Escuro               (50, 0, 75)   Magenta                   (50, 0, 100)  Rosa Escuro
(50, 25, 0)    Laranja Escuro               (50, 25, 25)  Marrom                     (50, 25, 50)  Roxo Claro                   (50, 25, 75)  Rosa Médio Escuro         (50, 25, 100) Rosa Médio
(50, 50, 0)    Amarelo Escuro               (50, 50, 25)  Marrom Claro               (50, 50, 50)  Cinza Médio                  (50, 50, 75)  Cinza Azul                (50, 50, 100) Azul Claro
(50, 75, 0)    Verde Limão Médio            (50, 75, 25)  Verde Neon Médio           (50, 75, 50)  Verde Claro                  (50, 75, 75)  Verde Água Claro          (50, 75, 100) Turquesa Claro
(50, 100, 0)   Verde Vivo                   (50, 100, 25) Verde Brilhante            (50, 100, 50) Verde Claro Brilhante        (50, 100, 75) Verde Limão Brilhante     (50, 100, 100) Turquesa Vivo
(75, 0, 0)     Vermelho Médio               (75, 0, 25)   Vermelho Rosado Escuro     (75, 0, 50)   Rosa Escuro                  (75, 0, 75)   Magenta Claro             (75, 0, 100)  Magenta Brilhante
(75, 25, 0)    Marrom Vermelho              (75, 25, 25)  Marrom Claro Escuro        (75, 25, 50)  Roxo Médio                   (75, 25, 75)  Roxo Claro                (75, 25, 100) Rosa Claro Escuro
(75, 50, 0)    Laranja Médio                (75, 50, 25)  Laranja Rosado             (75, 50, 50)  Rosa Médio                   (75, 50, 75)  Rosa                      (75, 50, 100) Rosa Claro
(75, 75, 0)    Amarelo                      (75, 75, 25)  Amarelo Claro Escuro       (75, 75, 50)  Verde Oliva Claro            (75, 75, 75)  Cinza Claro               (75, 75, 100) Azul Pastel
(75, 100, 0)   Verde Limão Vivo             (75, 100, 25) Verde Limão Brilhante      (75, 100, 50) Verde Neon Claro             (75, 100, 75) Verde Neon Brilhante      (75, 100, 100) Turquesa Brilhante
(100, 0, 0)    Vermelho                     (100, 0, 25)  Vermelho Rosado            (100, 0, 50)  Rosa                         (100, 0, 75)  Rosa Claro                (100, 0, 100) Magenta Claro
(100, 25, 0)   Laranja                      (100, 25, 25) Laranja Claro Escuro       (100, 25, 50) Rosa Médio                   (100, 25, 75) Rosa Claro Médio          (100, 25, 100) Rosa Claro Brilhante
(100, 50, 0)   Laranja Brilhante            (100, 50, 25) Laranja Pastel             (100, 50, 50) Rosa Pastel                  (100, 50, 75) Rosa Brilhante            (100, 50, 100) Magenta
(100, 75, 0)   Amarelo Claro                (100, 75, 25) Amarelo Limão              (100, 75, 50) Verde Claro Pastel           (100, 75, 75) Verde Limão Claro         (100, 75, 100) Turquesa Suave
(100, 100, 0)  Amarelo Brilhante            (100, 100, 25) Verde Limão Brilhante     (100, 100, 50) Verde Brilhante             (100, 100, 75) Verde Limão Claro Brilhante (100, 100, 100) Branco

Essas são as descrições gerais das cores possíveis.

Modelos de criação das cores: 

As cores primárias RGB (Red, Green, Blue) são usadas em dispositivos eletrônicos e baseiam-se na mistura aditiva de luz, onde a combinação máxima de todas as cores resulta em branco. Em contraste, o modelo CMY/CMYK (Ciano, Magenta, Amarelo, Preto) é utilizado em impressão e pintura, baseado na mistura subtrativa de pigmentos, onde a combinação de todas as cores idealmente resulta em preto. O modelo RYB (Vermelho, Amarelo, Azul) é uma convenção histórica no ensino de arte, usada pelos pintores para criar outras cores a partir dessas três primárias. A diferença principal é que RGB é aditivo (para luz) e CMY/CMYK e RYB são subtrativos (para pigmentos), refletindo a forma como as cores são criadas e percebidas em diferentes contextos.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
