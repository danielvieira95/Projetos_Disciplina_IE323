# Desafio lógico - Apague os LEDs

Este projeto tem como seu objetivo, desenvolver um jogo interativo que estimule a memória e o raciocínio lógico dos jogadores. O desafio do jogo é apagar todos os LEDs de uma matriz 5x5, onde a cada clique em um LED, ele e seus LEDs adjacentes alternam entre aceso e apagado. O jogador precisa encontrar a sequência correta de cliques para que todos os LEDs fiquem apagados simultaneamente ou seja o jogador planeje uma sequência de ações estratégicas para atingir um estado final específico, onde todos os LEDs da matriz 5x5 estejam apagados.

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

## Diagramas de conexão de hardware
As conexões e configurações de hardware é da plataforma bitdoglab e que são as seguintes:
- Um botão, identificado como Botão A, está conectado no GPIO5 da Raspberry Pi Pico. O outro terminal do botão está conectado ao GND da placa. 
- Outro botão, identificado como Botão B, está conectado no GPIO6 da Raspberry pi pico. O outro terminal do botão também está conectado ao GND da placa.
- Um buzzer passivo, identificado como Buzzer A, está conectado - através de um transistor - no GPIO21 da Raspberry pi pico.
- Buzzer passivo, identificado como Buzzer B, está conectado no GPIO10 da Raspberry pi pico.
- O pino in de uma matriz de LEDs 5050 RGB de 5 linhas por 5 colunas tipo WS2812B (Neopixel) está conectada ao GPIO7. 
- Um Joystick analógico tipo KY023 tem a saída VRy conectada ao GPIO26 e a saída VRx ao GPIO27. Seu botão SW está conectada ao GPIO22, o outro terminal do botão está no GND. 
- Um display OLED 128 colunas por  x 64 linhas de 0,96 polegadas com comunicação I2C, tem seu pino SDA conectado ao GPIO14 e o pino SCL com o GPIO15, estes pinos são do canal I2C0. Esse display (normalmente configurado no endereço 0x3C).

Tem a conexão com elemento externo a placa da BitDogLab que segue-se explicação em baixo.

Se guiando neste esquema de ligações, mas ficar atento com a pinagem da bitdoglab de acordo com a versão de cada placa.

![Esquema de ligação](https://github.com/user-attachments/assets/12d94c46-1bfd-4142-b416-6c75f2d2dbad)

Neste caso é PCB da BitDogLab é da versão 5 que igual este conector

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

Na ligação BL pode ser GP10 ou GP8. é so ficar atento no código.

## Estrutura do Projeto

- `raiz`: main.py Código-fonte do projeto.
- `raiz`: ST7735.py, sysfont.py e ssd1306.py que são biblioteca necessária para o projeto.
	* ssd1306.py auxilia no display oled
	* ST7735.py auxilia no display LCD TFT 128*RGB160
	* sysfont.py auxilia nas fontes de letras para display LCD TFT
- `docs/`: Documentação técnica, documentação do usuário
- `README.md`: Este arquivo.


Links de referência das bibliotecas:
* [ST7735](https://github.com/boochow/MicroPython-ST7735/tree/master) biblioteca ST7735.py com alguns exemplos
* [sysfont](https://github.com/GuyCarver/MicroPython/blob/master/lib/sysfont.py) biblioteca das sysfont
* [ST7735](https://github.com/boochow/MicroPython-ST7735/issues/9) link que complementa uma duvida sobre usar este biblioteca ST7735.
* [BitDogLab](https://github.com/BitDogLab/BitDogLab/commit/db2704d02596209923995fc20823b8b6147ad800) Este link fonte da imagem dos esquema das ligações


## Como Executar

1. Instale as dependências: Certifique-se de que todas as bibliotecas necessárias estão instaladas no Raspberry Pi Pico

2. Usa a conexão apropriada dos componentes segundo diagrama de conexão hardware.

3. Carregue o código: Use a IDE do Thommy  para carregar o código main.py e bibliotecas necessárias no Raspberry Pi Pico.

4. Inicie o jogo: Assim que o código estiver rodando, siga as instruções no display OLED e LCD TFT 128*RGB*160 para iniciar e jogar.

## Instruções do Jogo 

### Início do Jogo:

No display OLED, aparecerá a mensagem: "Bem-vindo O jogo começou Faza jogada.
No display LCD TFT, aparecerá a mensegem: "Bem vindo O objetivo do jogo é apagar todos os LEDs! Use o Joystick para mover o seletor. Ao pressionar o Joystick, os LEDs ao lado do LED escolhido mudam de estado: apagados acendem e os acessos apagam. Botão A: Solicitar ajuda após 5 jogadas Botão B: Reiniciar o jogo"

Ao clicar botão da esquerda, o jogo inicia, e o display OLED exibirá: "Atenção, jogo começando." Em seguida, a mensagem "Nível: 1" será mostrada.

### Como Jogar:

A mecânica central do jogo envolve uma matriz de LEDs 5x5, onde cada LED representa uma posição que o jogador pode selecionar e alterar o estado entre "aceso" e "apagado" A principio vem um esta do. Usando o joystick, o jogador move um cursor de led vermelho sobre a matriz para escolher o LED a ser ativado. Ao clicar, o LED selecionado e os LEDs adjacentes (nas direções de cima, baixo, esquerda e direita) alternam entre os estados aceso e apagado.
Esse funcionamento cria um desafio, pois cada clique não afeta apenas o LED escolhido, mas também seus vizinhos, o que exige que o jogador planeje cuidadosamente os cliques para atingir o objetivo. A meta é encontrar uma sequência que leve todos os LEDs ao estado "apagado". Esse processo de tentativa e erro incentiva o jogador a identificar padrões e a desenvolver uma estratégia eficaz, promovendo habilidades de resolução de problemas e raciocínio lógico.


### Controles:

Use o eixo Y do joystick para movimentar o cursor para cima e para baixo. Use o eixo X para movimentar o cursor da direta e para esquerda.
Ao pressionar o botão SW de meio do joystick, o estado do led aone cursor esta muda estado e do adjacente também alterna o estado.
Ao Pressionar o botão B, o jogo reinicia na naquele nivel ou no final do jogo reinicia por completo jogo.
Botão A depois de cinco jogadas em cada nivel fica disponivel para pressionar, mostra folha de resposta daquele nivel. 


### Progresso no Jogo:

Após acertar, o display OLED mostrará a mensagem: "Próximo nível".
O processo será repetido para os próximos níveis até completar todos os três.

### Fim do Jogo:

Quando todos os níveis forem concluídos, o display OLED mostrará o número de erros cometidos e o tempo total para completar o jogo.
Para reiniciar, clique no botão à direita (Botão B). O display OLED exibirá: "Reiniciando o jogo".



## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

