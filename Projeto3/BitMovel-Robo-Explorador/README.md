# Robô explorador

Esse repositório contém o Projeto 3 do Grupo 5 da matéria de IE323 - Tópicos em Eletrônica.

O trabalho, como projeto educacional, busca apresentar para estudantes uma ideia para criação de robôs através da união conceitos como comunicação sem fio, utilizando Bluetooth e Wi-Fi, sinais modulados por largura de pulso (PWM) para controle de motores, lógica para movimentação de robôs, uso de sensores para exploração e percepção do ambiente, como câmera, sensor de temperatura e sensor ultrassônico, movimentação e criação de um aplicativo de celular. O projeto é uma sugestão de atividade didática, contendo exposição teórica em slides e também um exemplo prático utilizando a placa [BitDogLab](https://github.com/BitDogLab/BitDogLab/tree/main) e periféricos listados a seguir.

Os alunos irão interagir com o robô através de um **aplicativo de celular** que controla a movimentação do agente robótico por meio do movimento do aparelho. Para isso, é utilizado o **acelerômetro**, um sensor interno que serve como fonte de dados da movimentação que está sendo realizada. Ao identificar a direção de deslocamento através da análise desses dados, é enviado um comando à BitDogLab via **Bluetooth**, que será interpretado e executado pela placa. Ainda, o aplicativo apresenta, em tempo real, imagens que estão sendo enviadas por **wi-fi** para um servidor web por uma câmera disposta no agente robótico. Caso o robô esteja muito próximo de um obstáculo, o sensor ultrassônico irá detectar e impedir a possível colisão.

TODO: sensor de temperatura e servos motor

### Autores

Carlos Julián Muñoz Quiroga, RA: 204200  
Patric Moreto, RA: 223083

## Recursos de hardware utilizados da BitDogLab

**On-board:**
- Buzzer
- Matriz de LEDs 5 x 5
- Periférico para comunicação UART/I2C (canal 0)

**Off-board:**
- Celular
- Módulo bluetooth HC-05
- Robô móvel ([chassi](https://www.tinkercad.com/things/1lvaPDfdjkt-chassi-bitmovel/edit?sharecode=c4YGIVprehL-UuPeUL_7wFy6jiYbiTO2cclIelt4kQc) e [conexões + detalhes](https://docs.google.com/document/d/19eDUn6APOkDckY-d9zxlf_N0l-tGTjby_PLXqS_WKOg/edit?usp=sharing))
- 2 motores DC
- Driver para motor (ponte H TB6612FNG)
- ESP32-CAM + OV2640
- Módulo conversor USB / TTL
- Sensor ultrassônico HC-SR04
- Sensor de temperatura AHT10
- Placa de circuito impresso

## Placa de circuito impresso

Foi criada uma PCI que possibilita o carregamento de programas na ESP32-CAM sem a necessidade de remover o módulo do BitMóvel, sendo apenas necessário inserir um jumper e realimentar a placa. O projeto da placa foi feito no Kicad está disponível na pasta PCI, sendo possível visualizar sua prévia abaixo.

![Placa de circuito impresso](./Img/PCI.png)

Caso deseja-se realizar as ligações da ESP32-CAM com o conversor USB / TTL sem utilizar a PCI, as ligações e o esquemático a seguir devem ser seguidos.

| ESP32-CAM | USB / TTL |
|-----------|-----------|
| 5V        | 5V        |
| GND       | GND       |
| U0T       | RX (RXC)  |
| U0R       | TX (TXD)  |

![Placa de circuito impresso](./Img/esp32cam-usbttl.png)

## Fluxogramas

### Software na BitDogLab

![Fluxograma do software na BitDogLab](./Img/Fluxograma_BitDogLab.png)

### Software na ESP32-CAM

![Fluxograma do software na ESP32-CAM](./Img/Fluxograma_ESP32CAM.png)

### Aplicativo de celular

![Fluxograma do software no aplicativo de celular](./Img/Fluxograma_AppInventor.png)

## Instruções de uso do aplicativo + robô

- **Instalação do aplicativo:** O aplicativo feito no MIT App Inventor é para celulares Android. Sua instalação é simples, basta ler o QR Code abaixo e o usuário será direcionado para o download do arquivo em formato APK. Normalmente, após o download for concluído, aparecerá a opção de abrir o arquivo com a opção do instalador do celular. Caso não, procure pelo arquivo *bitmovel_explorador.apk* em sua pasta de Downloads, clique nele e escolha o instalador. É bem provável que você tenha que permitir manualmente a instalação do aplicativo.
<br/><br/>
<img src = "./Img/QRCode_Android.png" height = "300">
<br/><br/>

- **Aplicativo:** Abra o aplicativo recém instalado, procurando por *BitMóvel Explorador*. O aplicativo funciona apenas com o celular na horizontal. O símbolo Bluetooth em cinza no canto superior esquerdo indica que ainda não foi feita a conexão com o módulo Bluetooth instalado no veículo, mais detalhes serão explicados no tópico seguinte. O símbolo de uma buzina no canto superior direito é um botão, que fará o robô emitir um som enquanto estiver pressionado. Os retângulos em branco indicam quais os possíveis movimentos a serem enviados ao robô, enquanto o retângulo em azul indica qual é a direção que está sendo enviada nesse momento. Caso todos os retângulos estejam em branco, está sendo executado o comando de ficar parado.    
Existem 5 movimentos padrões, que são avançar, virar para a esquerda, virar para a direita, retroceder e ficar parado, além das combinações avançar para esquerda, avançar para a direita, retroceder para a esquerda e retroceder para a direita.    
No centro da tela, caso o celular esteja conectado no wi-fi do robô, são exibidas as imagens capturadas pela câmera da ESP32-CAM. É possível dar zoom na imagem fazendo o movimento de pinça com os dedos.

- **Conexão Bluetooth:** No robô, conecte o fio vermelho que possui uma ponta solta no pino que está disponível no módulo Bluetooth, entre os fios vermelho e preto. O módulo indicará que está energizado piscando rapidamente um LED vermelho.     
Antes de pressionar o botão de Bluetooth no aplicativo, é necessário conectar previamente o celular ao Bluetooth do robô uma primeira vez. Procure por *HC-05* entre os dispositivos disponíveis em seu celular e conecte-se utilizando a senha *1234*.    
Voltando para o aplicativo, ao pressionar o botão de Bluetooth será aberta uma lista de dispositivos que você já se conectou previamente, basta selecionar o HC-05. É normal que ocorra uma pequena demora, então será aberta a tela inicial novamente, mas agora o símbolo do Bluetooth estará azul, indicando a tentativa de conexão Bluetooth com o robô. O módulo HC-05 irá piscar seu LED vermelho lentamente quando a conexão for bem sucedida. Caso a conexão falhe ou seja perdida por alguma razão, feche o aplicativo e tente conectar novamente clicando no botão do Bluetooth (agora em cinza).

- **Conexão Wi-Fi:** Ao ligar o robô, a placa ESP32-CAM será energizada e iniciar seu access point. Basta conectar o celular à rede wi-fi *BitMovel-WiFi* e as imagens da câmera estarão disponíveis no aplicativo.

- **Robô:** Confira se as rodas estão bem encaixadas e que não estão em contato com o parafuso, podendo causar travamento das rodas. Caso esteja tudo bem, basta apertar o botão *LIGA/DESLIGA* na placa BitDogLab, que está no canto esquerdo superior, olhando para o robô com as rodas voltadas para baixo. Para desligar o veículo, basta apertar duas vezes o mesmo botão.

## Projeto do aplicativo feito no MIT App Inventor

O arquivo *bluetooth_explorador.aia* disponibilizado nesse repositório contém o projeto do aplicativo de celular desenvolvido. É possível fazer o download desse projeto e importar para o MIT App Inventor, sendo possível realizar edições.