# Robô controlado por aplicativo via Bluetooth

Esse repositório contém o Projeto 2 do Grupo 5 da matéria de IE323 - Tópicos em Eletrônica.

O trabalho, como projeto educacional, busca apresentar para estudantes uma ideia para criação de robôs através da união conceitos como comunicação via Bluetooth, sinais modulados por largura de pulso (PWM) para controle de motores, lógica para movimentação de robôs e criação de um aplicativo de celular. O projeto é uma sugestão de atividade didática, contendo exposição teórica em slides e também um exemplo prático utilizando a placa [BitDogLab](https://github.com/BitDogLab/BitDogLab/tree/main) e periféricos listados a seguir.

Os alunos irão interagir com o robô através de um **aplicativo de celular** que controla a movimentação do agente robótico por meio do movimento do aparelho. Para isso, é utilizado o **acelerômetro**, um sensor interno que serve como fonte de dados da movimentação que está sendo realizada. Ao identificar a direção de deslocamento através da análise desses dados, é enviado um comando à BitDogLab via **Bluetooth**, que será interpretado e executado pela placa.

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

## Fluxogramas

### Software na BitDogLab

![Fluxograma do software na BitDogLab](./Img/Fluxograma_BitDogLab.png)

### Aplicativo de celular

![Fluxograma do software no aplicativo de celular](./Img/Fluxograma_AppInventor.png)

## Instruções de uso do aplicativo + robô

- **Instalação do aplicativo:** O aplicativo feito no MIT App Inventor é para celulares Android. Sua instalação é simples, basta ler o QR Code abaixo e o usuário será direcionado para o download do arquivo em formato APK. Normalmente, após o download for concluído, aparecerá a opção de abrir o arquivo com a opção do instalador do celular. Caso não, procure pelo arquivo *bitmovel_bluetooth.apk* em sua pasta de Downloads, clique nele e escolha o instalador. É bem provável que você tenha que permitir manualmente a instalação do aplicativo.
<br/><br/>
<img src = "./Img/QRCode_Android.png" height = "300">
<br/><br/>

- **Aplicativo:** Abra o aplicativo recém instalado, procurando por *BitMóvel Bluetooth*. O aplicativo funciona apenas com o celular na horizontal. O símbolo Bluetooth em cinza no canto superior esquerdo indica que ainda não foi feita a conexão com o módulo Bluetooth instalado no veículo, mais detalhes serão explicados no tópico seguinte. O símbolo de uma buzina no canto superior direito é um botão, que fará o robô emitir um som enquanto estiver pressionado. Os retângulos em branco indicam quais os possíveis movimentos a serem enviados ao robô, enquanto o retângulo em azul indica qual é a direção que está sendo enviada nesse momento.    
Existem 5 movimentos padrões, que são avançar, virar para a esquerda, virar para a direita, retroceder e ficar parado, além das combinações avançar para esquerda, avançar para a direita, retroceder para a esquerda e retroceder para a direita.

- **Conexão Bluetooth:** No robô, conecte o fio vermelho que possui uma ponta solta no pino que está disponível no módulo Bluetooth, entre os fios vermelho e preto. O módulo indicará que está energizado piscando rapidamente um LED vermelho.     
Antes de pressionar o botão de Bluetooth no aplicativo, é necessário conectar previamente o celular ao Bluetooth do robô uma primeira vez. Procure por *HC-05* entre os dispositivos disponíveis em seu celular e conecte-se utilizando a senha *1234*.    
Voltando para o aplicativo, ao pressionar o botão de Bluetooth será aberta uma lista de dispositivos que você já se conectou previamente, basta selecionar o HC-05. É normal que ocorra uma pequena demora, então será aberta a tela inicial novamente, mas agora o símbolo do Bluetooth estará azul, indicando a tentativa de conexão Bluetooth com o robô. O módulo HC-05 irá piscar seu LED vermelho lentamente quando a conexão for bem sucedida. Caso a conexão falhe ou seja perdida por alguma razão, feche o aplicativo e tente conectar novamente clicando no botão do Bluetooth (agora em cinza).

- **Robô:** Confira se as rodas estão bem encaixadas e que não estão em contato com o parafuso, podendo causar travamento das rodas. Caso esteja tudo bem, basta apertar o botão *LIGA/DESLIGA* na placa BitDogLab, que está no canto esquerdo superior, olhando para o robô com as rodas voltadas para baixo. Para desligar o veículo, basta apertar duas vezes o mesmo botão.

## Projeto do aplicativo feito no MIT App Inventor

O arquivo *bluetooth_car.aia* disponibilizado nesse repositório contém o projeto do aplicativo de celular desenvolvido. É possível fazer o download desse projeto e importar para o MIT App Inventor, sendo possível realizar edições.
