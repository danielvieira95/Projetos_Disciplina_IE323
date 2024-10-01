# Autores

Vinicius Emanoel Ares, RA: 083028  
Edson Costa Oliveira, RA: 188405 

# BitMóvel Seguidor de Linha

BitMóvel Seguidor de Linha é um projeto educacional de robô seguidor de linha para a placa [BitDogLab](https://github.com/BitDogLab/BitDogLab). O projeto foi desenvolvido como projeto 2 da disciplina da FEEC/Unicamp IE323 - Sistemas Embarcados para ensino com abordagem STEM
<details>
  <summary>Clique para saber mais sobre a disciplina.</summary>
  Sistemas Embarcados para ensino com abordagem STEM é uma disciplina da pós-graduação da FEEC-UNICAMP ofertada pelo professor Fabiano Fruett com auxílio do professor Daniel Vieira. O objetivo da matéria é desenvolver projetos que envolva IoT, eletrônica e IA com o intuito de levar ferramentas para os alunos do ensino fundamental e médio utilizando a abordagem STEM (Science, Technology, Engineering and Mathematics). [BitDogLab](https://cpg.fee.unicamp.br/lista/caderno_horario_show.php?id=1932).
</details>
O objetivo do projeto 2 da disciplina é usar a placa BitDogLab conectada a dispositívos externos.<br><br>

O BitMóvel Seguidor de Linha é um robô diferencial com 2 rodas motrizes e uma esfera de apoio na frente, formando um tripé ou triciclo. O robô usa sensores reflexivos infravermelhos TCRT5000 para detectar uma linha escura no chão. O chassis e suporte dos sensores é fabricado por impressão 3D em PLA. Além da função seguidor de linha, os botões A e B são programados para comandar o robô para ativo ou desativado, respectivamente. O robô inicia no modo desativado, então quando o botão A é pressionado o robô está em modo de movimento ativo para frente seguindo a linha embaixo do chassis. Quando o botão B é pressionado o robô fica parado até que se pressione o botão A novamente.
Este projeto usa:
- 1 Placa BitDogLab
- 2 motores DC 3-6V com Caixa de Redução e Eixo Duplo + Roda 68mm
- 1 Driver ponte H modelo HW-166
- 1 bateria 2s1p 7,6V 550mAh
- 4 sensores TCRT5000
- 1 Chassis impresso conforme arquivo (desenhos_mecanicos_3d/chassis_com_detalhes.STL)
- 1 Suporte de sensores conforme arquivo (desenhos_mecanicos_3d/suporte_sensores_avulsos.STL)
- 1 esfera para apoio
- 10 jumpers macho-fêmea
- 4 jumpers fêmea-fêmea
- fita isolante
- fita dupla-face
<br><br>
O fluxograma abaixo ilustra o funcionamento do programa:

<div align="center">
<img src="./fluxograma.png" alt="Description of the image" width="500"/>
</div>
  
Além do robô físico, foi desenvolvido um robô virtual no simulador de robótica CoppeliaSim.  
  
Para mais informações, é possível acessar o relatório do projeto disponibilizado no [link](https://docs.google.com/document/d/1Ikr_fQ6nfiymL5znAn5tAetg0D3t27z1).

## Como instalar e operar o robô físico?

1. Instale a IDE Arduino.
2. Conecte a placa BitDogLab ao computador através de um cabo micro-USB.
3. Para utilizar a Raspberry Pi Pico, é necessário instalar instale o gerenciador de porta Raspberry Pi Pico RP2040 
4. Baixe os códigos `projeto02.ino` neste repositório.
5. Na IDE Arduino, acesse `Arquivo > Abrir` e localize o arquivo `projeto02.ino` (por exemplo, na pasta Downloads).
6. Pressione o botão de verificar o código para certificar-se que não há erro, caso esteja tudo certo:
7. Pressione o botão "carregar" (setinha) para carregar o código para a placa, esta operação salva e executa o código em uma única etapa.
8. Pronto, você pode desconectar a BitDogLab e o programa pode ser executado (ou reiniciado) apertando o botão próximo à bateria.

## Como criar o robô virtual no simulador?
1. Instale o CoppeliaSim através do [link](https://www.coppeliarobotics.com/)
2. Siga os vídeos tutoriais 1 a 6 (total 40min) nos links do youtube abaixo:
   1. Parte 1/6 [link](https://youtu.be/lg1HlHTUYXg)
   2. Parte 2/6 [link](https://youtu.be/nZWR1QXElUE)
   3. Parte 3/6 [link](https://youtu.be/mu0NJf-Q52E)
   4. Parte 4/6 [link](https://youtu.be/frFhMvI1_uE)
   5. Parte 5/6 [link](https://youtu.be/FozVGTvBlqc)
   6. Parte 6/6 [link](https://youtu.be/4l1JGo2Js-c)

