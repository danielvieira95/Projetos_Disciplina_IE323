# Autores

Vinicius Emanoel Ares, RA: 083028  
Edson Costa Oliveira, RA: 188405 

# BitMóvel Seguidor de Linha, versao com monitoramento de bateria

O fluxograma abaixo ilustra o funcionamento do programa embarcado no microcontrolador da BitDogLab:

<div align="center">
<img src="./Fluxograma_rp2040.png" alt="Description of the image" width="500"/>
</div>


O fluxograma abaixo ilustra o funcionamento do aplicativo de celular:

<div align="center">
<img src="./Fluxograma_app_celular.png" alt="Description of the image" width="500"/>
</div>

## Como instalar e operar o robô físico?

1. Instale a IDE Arduino.
2. Conecte a placa BitDogLab ao computador através de um cabo micro-USB.
3. Para utilizar a Raspberry Pi Pico, é necessário instalar o gerenciador de porta Raspberry Pi Pico RP2040. Vá em `File > Preferências` e copie `https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json` em `Additional Boards manager URL's`. Em seguida, vá em `Tools > Board > Board manager`e instale `Raspberry Pi Pico/RP2040 by Earlephilhower`.
4. Baixe os códigos `Projeto_Seguidor_de_Linha.ino` neste repositório.
5. Na IDE Arduino, acesse `Arquivo > Abrir` e localize o arquivo `Projeto_Seguidor_de_Linha.ino` (por exemplo, na pasta Downloads).
6. Pressione o botão de verificar o código para certificar-se que não há erro, caso esteja tudo certo:
7. Pressione o botão "carregar" (setinha) para carregar o código para a placa, esta operação salva e executa o código em uma única etapa.
8. Pronto, você pode desconectar a BitDogLab e o programa pode ser executado (ou reiniciado) apertando o botão próximo à bateria.

## Como conectar o Bluetooth do App com o carrinho? 

1. Instale o app BitMovel.apk
2. Clique em "BitDogMovel Bluetooth".
3. Certifique-se de que o Bluetooth do celular está ativado.
4. Clique em Dispositivos.
5. Procure na lista "HC-05" e clique. O status do carrinho exibirá "conectado".
6. Caso ocorra algum erro de conexão, repita o processo a partir do 4.
