# Projeto 1 - Explorando a Química e a Matemática com a BitDogLab - IE323A

## Autores

Eduardo Matheo Sausen - 289674

Victor Anthony Teixeira dos Santos - 206467

## Introdução
  Este projeto desenvolve um sistema embarcado educativo que utiliza um Display OLED e uma Matriz RGB da BitDogLab para facilitar o ensino de matemática e química. O Display OLED exibe formas geométricas e fórmulas matemáticas, enquanto a Matriz RGB simula átomos e o compartilhamento de elétrons. A interface é interativa, permitindo a navegação entre tópicos através de botões, proporcionando uma experiência de aprendizado dinâmica e personalizada.

## Objetivos
1. **Uso do Display OLED:** Exibir formas geométricas e fórmulas matemáticas para melhorar a compreensão de conceitos.

2. **Simulação Química com Matriz RGB:** Representar átomos e camadas de valência, facilitando o entendimento de química.

3. **Botões de Entrada:** Permitir navegação interativa entre modos e tópicos.

4. **Interface Intuitiva:** Focar no aprendizado enquanto o sistema gerencia a complexidade técnica.

5. **Apoio ao Ensino Cooperativo:** Promover colaboração entre estudantes e professores, facilitando o aprendizado coletivo.

   Este projeto está alinhado com as habilidades específicas da BNCC, como (EF07MA31) Estabelecer expressões de cálculo de área de triângulos e de quadriláteros, (EF08MA19) Resolver e elaborar problemas que envolvam medidas de área de figuras geométricas, utilizando expressões de cálculo de área (quadriláteros, triângulos e círculos), em situações como determinar medida de terrenos e (EF09CI03) Identificar modelos que descrevem a estrutura da matéria (constituição do átomo e composição de moléculas simples) e reconhecer sua evolução histórica.

## Teoria e Aplicação no Ensino de Química e Matemática

**Ensino de Química - Regra do Octeto**

  O projeto utiliza a Matriz RGB para simular átomos e suas camadas de valência, ilustrando conceitos fundamentais como a Regra do Octeto. Elementos como Hidrogênio, Hélio, Carbono e Oxigênio são visualmente representados, mostrando como os átomos compartilham ou recebem elétrons para atingir a estabilidade.

    Hidrogênio (H): Mostra a necessidade de uma ligação química para estabilizar seu único elétron.
    Hélio (He): Demonstra a estabilidade natural com dois elétrons, sem necessidade de ligação.
    Carbono (C): Exibe a necessidade de quatro ligações covalentes para estabilidade.
    Oxigênio (O): Mostra a necessidade de compartilhar dois elétrons para estabilização.

  Os alunos podem interagir com o sistema, selecionando elementos e visualizando suas camadas de valência em tempo real, reforçando o entendimento das ligações químicas.
Ensino de Matemática - Geometria Plana Básica

**Ensino de Matemática**

  O sistema embarcado utiliza o Display OLED para desenhar e interagir com figuras geométricas planas, como quadrados, retângulos, triângulos e círculos, aplicando fórmulas para cálculo de áreas.

    Quadrado: Representa todos os lados iguais, aplicando a fórmula Área = L x L. Onde "L" representa o Lado do quadrado.
    Retângulo: Calcula a área como Área = b x h. Sendo "b" equivalente a base e "h" a altura do retângulo.

  Os alunos podem exercitar os calculos de geometria das figuras, com exemplos pré-carregados na memória do raspberry pi pico embarcado na BitDogLab, usando diretamente no display, o que facilita a compreensão prática dos conceitos matemáticos.

## Funcionamento do Software na BitDogLab e Explicação dos Códigos Python

  Os arquivos base para embarcar na BitDOgLab e aplicação das atividades de química e matemática, os quais estão incluídos na pasta main deste projeto, são respectivamente "rgb-matrix-chemestry.py" e "display-oled-geometry.py".

  Estes códigos em linguagem Python estão organizados da seguinte maneira:
1. **Definição das Classes e Parâmetros Iniciais**:
  Inicialmente, definimos as classes a serem utilizadas no código, como Pin, SoftI2C e SSD1306_I2C.
  Estabelecemos os parâmetros para o display OLED e a matriz RGB, como por exemplo: oled = SSD1306_I2C(128, 64, i2c) e np = neopixel.NeoPixel(machine.Pin(7), 25).

3. **Configuração da Matriz RGB**:
  Definimos a intensidade, as cores e o padrão de cores desejado para a matriz RGB.
  Criamos uma função para a matriz de LED e para passar os valores configurados anteriormente.

4. **Definição das Funções do Projeto**:
  Desenvolvemos as funções que determinam o que será exibido no display de LED e na matriz RGB.
  Estabelecemos as informações que queríamos que fossem mostradas.

5. **Implementação da Lógica de Controle**:
  Criamos a função switch_case_dicionario(value) para definir quais funções serão chamadas com base no valor recebido.
  Utilizamos return cases.get(value, case0)() para buscar e executar as funções descritas anteriormente.

6. **Controle por Botão e Laço de Repetição**:
  Definimos a variável count e utilizamos um laço while para controlar o botão e selecionar as funções de acordo com o valor de count.

Para mais detalhes sobre o funcionamento do arquivos e como utilizá-lo, consulte os próprios códigos fonte que possuem comentários e estão disponíveis neste repositório.

## Getting Started com a BitDogLab

A BitDogLab possui um repositório próprio que pode ser encontrado no link:https://github.com/BitDogLab/BitDogLab/tree/main

A imagem a seguir é uma representação do sistema embarcado da BitDog identificando os recursos de hardware utilizados para interagir com a software. Assim, tem-se a matriz de leds, o display oled e os dois botões.Os botões estão identificados como "A" e "B" e tem função de decremento e incremento para facilitar a navegação do usuário no menu interativo do display OLED.
![bitdoglab_rasc](https://github.com/user-attachments/assets/87e243be-132e-419a-8980-68e973c2fa03)

Para uma primeira experiência com as atividade da regra do octeto e de geometria plana siga os passos a seguir:

1. Energizar a placa da BitDog - Plugue o cabo USB no computador ou utilize uma bateria adequada.
2. Aguarde enquanto a BitDog realiza o seu proceso de inicialização automático.
3. Siga as instruções apresentadas no display OLED
4. Use o botão "B" para avançar nas etapas do menu do Display OLED e use o Botão "A" para voltar a etapa anterior do menu do display OLED.

Conforme você avança nas etapas do menu, novos exercícios são apresentados. 
A primeira matéria estudada é a regra do octeto. A imagem a seguir apresenta um frame da disposição atômica dos elétrons na camada de valência para o elemento Oxigênio. Perceba que os elétrons interagem na camada de valência se movimentando na eletrosfera.
![bitdog-ex-oxigenio](https://github.com/user-attachments/assets/5ee65467-9f25-485b-847f-bb18bb269952)

Após finalizar as atividades de química, você poderá seguir os estudos em matemática com os exemplos de geometria plana.
A imagem abaixo demonstra o exercicio de cálculo da área do quadrado.
![bitdog-ex-quadrado](https://github.com/user-attachments/assets/2af120af-1ffc-424b-9273-4a8cdcc22731)

