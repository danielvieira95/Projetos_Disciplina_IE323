# Autores

Vinicius Emanoel Ares, RA: 083028  
Edson Costa Oliveira, RA: 188405 

# BitMóvel Seguidor de Linha, versao com monitoramento de bateria

BitMóvel Seguidor de Linha é um projeto educacional de robô seguidor de linha para a placa [BitDogLab](https://github.com/BitDogLab/BitDogLab). O projeto foi desenvolvido como projeto 3 da disciplina da FEEC/Unicamp IE323 - Sistemas Embarcados para ensino com abordagem STEM
<details>
  <summary>Clique para saber mais sobre a disciplina.</summary>
  Sistemas Embarcados para ensino com abordagem STEM é uma disciplina da pós-graduação da FEEC-UNICAMP ofertada pelo professor Fabiano Fruett com auxílio do professor Daniel Vieira. O objetivo da matéria é desenvolver projetos que envolva IoT, eletrônica e IA com o intuito de levar ferramentas para os alunos do ensino fundamental e médio utilizando a abordagem STEM (Science, Technology, Engineering and Mathematics). [BitDogLab](https://cpg.fee.unicamp.br/lista/caderno_horario_show.php?id=1932).
</details>
O objetivo do Projeto 3 da disciplina é utilizar a placa BitDogLab conectada a dispositivos externos, com a proposta de preparar o projeto para uso em escolas. Isso inclui o desenvolvimento peças 3D e de placas eletrônicas, por exemplo, para eliminar fios soltos que podem causar mau contato.<br><br>

O BitMóvel Seguidor de Linha é um robô diferencial com 2 rodas motrizes e uma esfera de apoio na frente, formando um tripé ou triciclo. O robô usa sensores reflexivos infravermelhos QRD1114 para detectar uma linha escura no chão. O design do carrinho é fabricado por impressão 3D em PLA. Além da função seguidor de linha, os botões A e B são programados para comandar o robô para ativo ou desativado, respectivamente. O robô inicia no modo desativado, então quando o botão A é pressionado o robô está em modo de movimento ativo para frente seguindo a linha embaixo do chassis. Quando o botão B é pressionado o robô fica parado até que se pressione o botão A novamente. O BitMóvel conta com um aplicativo que permite o monitoramento da bateria. Por meio dele, o usuário pode acessar informações sobre o BitDogLab, controlar o acionamento e desligamento do carrinho, verificar o nível da bateria e obter suporte técnico. Além disso, o código implementado protege o carrinho contra níveis críticos de bateria e situações de sobrecorrente no circuito.

Este projeto usa:
- 1 Placa BitDogLab
- 2 motores DC 3-6V com Caixa de Redução e Eixo Duplo + Roda 68mm
- 1 Driver ponte H modelo HW-166
- 1 bateria 2s1p 7,6V 550mAh
- 1 placa de sensores conforme arquivo (Projeto3/Grupo3-BitMovel-Seguidor-de-Linha/Placas Eletrônicas/placa_de_sensores.kicad_pcb)
- 1 módulo ADS1115
- 1 placa de monitoramento de bateria conforme arquivo (Projeto3/Grupo3-BitMovel-Seguidor-de-Linha/Placas Eletrônicas/monitoramento.kicad_pcb)
- 1 módulo Bluetooth HC-05
- 1 módulo INA-226
- 1 placa expansor I2C conforme arquivo (Projeto3/Grupo3-BitMovel-Seguidor-de-Linha/Placas Eletrônicas/expansão_i2c.kicad_pcb)
- Peças para impressão 3D conforme arquivo (desenhos_mecanicos_3d/suporte_sensores_avulsos.STL)
- 3 parafusos M3 30mm
- 6 porcas m3
- Fita isolante
- fita dupla-face
<br><br>

O fluxograma abaixo ilustra o funcionamento do programa embarcado no microcontrolador da BitDogLab:

<div align="center">
<img src="./Fluxograma_rp2040.png" alt="Description of the image" width="500"/>
</div>


O fluxograma abaixo ilustra o funcionamento do aplicativo de celular:

<div align="center">
<img src="./Fluxograma_app_celular.png" alt="Description of the image" width="500"/>
</div>

Para mais informações, é possível acessar o relatório do projeto disponibilizado no [link]([https://docs.google.com/document/d/1Ikr_fQ6nfiymL5znAn5tAetg0D3t27z1](https://docs.google.com/document/d/1KMj3I93LfhJuYwX31ApxWePKK1TJ1PmV/edit?usp=sharing&ouid=113991507111012118869&rtpof=true&sd=true)).

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
