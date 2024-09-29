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

**Off-board:**
- Celular
- Módulo bluetooth HC-05
- Robô móvel ([chassi](https://www.tinkercad.com/things/1lvaPDfdjkt-chassi-bitmovel/edit?sharecode=c4YGIVprehL-UuPeUL_7wFy6jiYbiTO2cclIelt4kQc) e [conexões + detalhes](https://docs.google.com/document/d/19eDUn6APOkDckY-d9zxlf_N0l-tGTjby_PLXqS_WKOg/edit?usp=sharing))
- 2 motores DC
- Driver para motor (ponte H TB6612FNG)

## Fluxogramas

### Software na BitDogLab

![Fluxograma do software na BitDogLab](./Img/)

### Aplicativo de celular

![Fluxograma do software no aplicativo de celular](./Img/)

## Instruções de uso do aplicativo + robô

- **Instalação do aplicativo:**

- **Aplicativo:**

- **Conexão Bluetooth:** 

- **Robô:** 