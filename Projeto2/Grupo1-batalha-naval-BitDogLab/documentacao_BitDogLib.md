## ligar_led(x, y, cor)
Essa função liga um led na matriz de leds.
Parâmetros:
- x: qual a coluna do led que você quer ligar pode ser de 0 até 4
- y: qual a linha do led que você quer ligar pode ser de 0 até 4
- cor: [R,G,B] uma lista com os valores de vermelho, verde e azul.
    - cada cor pode ser de 0 até 255.
## apagar_led(x, y)
Essa função apaga um led na matriz de leds.
Parâmetros:
- x: qual a coluna do led que você quer ligar pode ser de 0 até 4
- y: qual a linha do led que você quer ligar pode ser de 0 até 4
## apagar_leds()
Essa função apaga todos os leds da matriz de leds.
## criar_matriz()
Essa função retorna uma matriz apagada do tamanho da matriz de leds
## copiar_matriz(matriz)
Essa função faz uma cópia de uma matriz
Parâmetros:
- matriz: matriz a ser copiada.
## ligar_matriz(matriz)
Essa função liga a matriz passada
Parâmetros:
- matriz: matriz a ser ligada
    - exemplo:
    ```py
    [
     [[r,g,b],[r,g,b]],
     [[r,g,b],[r,g,b]]
    ]
    ```

onde r,g e b são os valores das cores vermelho, verde e azul respectivamente
## carinha_feliz(cor)
Pinta uma carinha feliz na matriz de LEDs
Parâmetros:
- cor: cor da carinha no formato [r,g,b]
onde r,g e b são os valores das cores vermelho, verde e azul respectivamente
## carinha_triste(cor)
Pinta uma carinha triste na matriz de LEDs
Parâmetros:
- cor: cor da carinha no formato [r,g,b]
onde r,g e b são os valores das cores vermelho, verde e azul respectivamente

## escrever_tela(text, x, y)
Essa função adiciona textos que vão aparecer na tela quando usar a função mostrar_tela
- texto: o texto que você quer que apareça
- x: a coluna onde o texto começa
- y: a linha onde o texto começa
## mostrar_tela()
Essa função exibe os textos adicionado na tela
## limpar_tela()
Essa função apaga tudo da tela oled
## explosao_oled()
roda animação de explosão
## agua_oled()
roda animação de agua
## play_pbm(arquivo, duracao_frame=15)
exibe um ou multiplos frames de um arquivo pbm
Parâmetros:
- arquivo: string com o nome do arquivo a ser exibido
- duracao_frame: a duração de cada frame em milissegundos padrão é 15.

## botao_A_pressionado()
Essa função retorna `True` (verdade) uma vez quando o botão for pressionado, e `False` (falso) nos outros casos.
## botao_B_pressionado()
Essa função retorna `True` (verdade) uma vez quando o botão for pressionado, e `False` (falso) nos outros casos.
## valor_botao_A()
Essa função retorna se `True` (verdade) o botão está pressionado e `False` (falso) caso contrário caso contrário.
## valor_botao_B()
Essa função retorna se `True` (verdade) o botão está pressionado e `False` (falso) caso contrário caso contrário.
## botao_A_solto()
Essa função retorna `True` (verdade) no momento que você soltar o botão, e `False` (falso) nos outros casos.
## botao_B_solto()
Essa função retorna `True` (verdade) no momento que você soltar o botão, e `False` (falso) nos outros casos.

## som_morreu()
Essa função toca o som de quando o jogador morre.
## som_explosao()
Essa função toca um som de explosão
## som_agua()
Essa função toca um som de agua

## numero_aleatorio(numero1, numero2)
Essa função retorna um número aleatório maior ou igual ao `numero1` e menor ou igual ao `numero2`.
## loop(func)
Essa função recebe uma função com o que executar em cada loop do jogo.
Parâmetros:
- func: uma função que recebe o valor de micro segundos que passou desde a última vez que a função foi executada.
## ler_arquivo(nome)
Essa função lê um arquivo, se o arquivo não existe ela retorna uma string vazia ''. Caso contrário retorna o que estava escrito no arquivo.
- nome: nome do arquivo
## escrever_arquivo(nome, mensagem)
Essa função salva um texto em um arquivo.
- nome: nome do arquivo
- mensagem: texto a ser salvo
## dormir(segundos)
Essa função dorme a BitDogLab pelos segundos passados no argumento
Parâmetros:
- segundos: tempo em segundos que é para dormir.
## reiniciar()
Essa função reinicia a BitDogLab de forma a apagar os LEDs

## joystick_x()
Essa função retorna se o valor em X é para cima ou para baixo
## joystick_y()
Essa função retorna se o valor em Y é para esquerda ou para direita
## botao_joystick_solto()
Essa função retorna se o botão do joystick foi solto
## botao_joystick_pressionado()
Essa função retorna se o botão do joystick está pressionado apenas uma vez por vez que é pressionado
## valor_botao_joystick()
retorna o valor do botão

## enviar_via_wifi(msg:list)
Essa função envia uma mensagem via wifi
Parâmetros:
- msg: a(s) mensagem(ns) a ser enviada deve estar dentro de uma lista exemplo: ['olá mundo']
## desligar_wifi()
Essa função desliga o WiFi
## esperar_receber()
Espera até receber uma mensagem e retorna ela em formato de lista
## definir_servidor_ou_cliente(grupo:int, is_servidor:bool)
Essa função estabelece uma conexão entre duas BitDogLab
Parâmetros:
- grupo: número de 0 à 255 que define os três primeiros dígitos do IP
- is_servidor: define se é servidor (`True`) ou não (`False`)
## teste_forca_wifi()
Está função retorna qual o valor RSSI da conexão
