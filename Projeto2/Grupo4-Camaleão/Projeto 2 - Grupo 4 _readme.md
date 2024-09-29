# Tecnologia de Camaleão Imitando Cores da Natureza


Este projeto simula a capacidade de camuflagem dos camaleões, imitando as cores da natureza mediante um sistema embarcado. Utilizando um sensor de cor TCS34725, o sistema identifica a cor primária RGB de um objeto e reproduz esse cor em uma matriz de LEDs RGB WS2812B (Neopixel). Um display OLED exibe os valores exatos das cores (R, G, B) captada pelo sensor, proporcionando uma interface visual clara e informativa.
O projeto será desenvolvido utilizando a plataforma BitDogLab com o microcontrolador Raspberry Pi Pico, programado em Python no ambiente MicroPython usando o IDE Thonny.

## Objetivo

O objetivo deste sistema é capturar cores RGB primários usando um sensor de cor e reproduzi-los em uma matriz de LEDs RGB. Ao mesmo tempo, os valores RGB exatos são exibidos em um display OLED, promovendo uma experiência interativa e educacional no aprendizado de combinação de cores.


### Autores

Gelson de Barros Ferreira, RA: 212732  
Wallif Campos Alves de Souza, RA: 290031

## Funcionalidades

- Matriz de LEDs RGB (5x5): Mostra a cor nos leds sensor capturou .
- Display OLED: Exibe os valores RGB capturados.
- Sensor de cor TCS34725: Capta as cores RGB primarias

## Componentes Necessários
- Placa BitDogLab V5
  
### Ou ainda pode ter componentes separados como:
  - Raspberry Pi Pico
  - Matriz de LEDs WS2812B (5x5)
  - Display OLED 128x64 (I2C)
  - Sensor de Cor TCS34725 

## Como Executar

1. Instale as dependências: Certifique-se de que todas as bibliotecas necessárias estão instaladas no Raspberry Pi Pico.

2. Usa a conexão apropriada dos componentes segundo diagrama de conexão hardware.

3. Segue as instruções de como instalar o jogo.


## Estrutura do Projeto

- `raiz`: main.py Código-fonte do projeto.
- `raiz`: Documentação técnica
- `raiz`: folha de cores RGB primarias
- `README.md`: Este arquivo.
  
## Diagramas de conexão de hardware

- Matriz de LEDs WS2812B (Neopixel) :Pino de entrada (IN) conectado ao GPIO7 do Raspberry Pi Pico.
- Tela OLED (128x64) : Pino SDA conectado ao GPIO14 e SCL ao GPIO15 (I2C1).
- Sensor de cor TCS34725 : Pino SDA conectado ao GPIO0 e SCL ao GPIO1 (I2C0).


##  Instruções de como instalar o jogo
Passo 1: Instalar a IDE Thonny 
Baixe e instale o IDE Thonny a partir do site oficial. 

Passo 2: Configurar IDE thonny com o MicroPython ( Raspberry PI Pico)
Abra o IDE Thonny e clique no ícone de aonde tem configure interpreter (localizado no lado direito abaixo).
Seleciona MicroPython ( Raspberry PI Pico)
Seleciona a porta do microcontrolador
Copie o código do repositório pretendido e salva com na opção que vai aparecer  Raspberry com nome main.py e faça o mesmo no código da biblioteca, mas como nome de TCS34725.py. Caso já tenha um código salvo, apenas substitua. 

Passo 3: Enviar o Código para o plataforma Bitdoglab
No IDE Thonny, digitando o F5 para enviar e correr com programa no bitloglab ou clica no botão run. 

Passo 4: Ver o Código Funcionando, 
Após enviar o código, o Pico vai rodar o main.py automaticamente. Se tudo estiver certo, programa vai começar.



## Explicação do Código
Importação das Bibliotecas : O código utiliza bibliotecas como machine para controle do hardware, neopixel para controlar a matriz de LEDs, tcs34725 para o sensor de núcleo e ssd1306 para o display OLED.

Configuração do OLED e Sensor de Cor : O OLED está configurado no canal I2C1, enquanto o sensor de cor utiliza o canal I2C0. O sensor de cor é inicializado com tempo de integração e ganho definido.

Funções Principais :

ler_sensor_cor: Lê os valores RGB e a clareza (intensidade de luz) capturados pelo sensor.

captura_cor(r, g, b, c): Processa e identifica a cor.

ajustar_matriz_leds: Ajusta a matriz de LEDs para reproduzir a cor detectada.

exibir_cor_oled: Exibe os valores RGB no display OLED.

loop_principal: Loop contínuo que realiza a leitura dos valores, normaliza os dados e os exibe tanto na matriz de LEDs quanto no OLED.

Dicionario de cores predefinidas do RGB primários : para garantir que a cor exibida seja precisa, os valores RGB são ajustadas com base na clareza capturada pelo sensor (analisando os valores de R, G e B pelo valor de C).

Loop Infinito : O programa funciona em um loop infinito, capturando e exibindo as cores continuamente.

## Referência Bibliográfica

https://www.youtube.com/watch?v=GF4DfSiGFNE

https://www.afixgraf.com.br/blog/o-que-significa-rgb/


## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.
