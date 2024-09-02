# Básico BitDogLab

- **Botão**: Um interruptor que, quando pressionado, faz algo acontecer, como acender uma luz.
- **Buzzer**: Um pequeno dispositivo que emite som quando ligado, como um alarme.
- **Tela OLED**: Uma tela pequena e fina que pode mostrar textos ou imagens, usada em dispositivos como alguns celulares.
- **LED**: Uma luz pequena que acende quando eletricidade passa por ela, usada para indicar coisas como se um aparelho está ligado.

# Explicação de Programação em Python
## `def`

A palavra `def` é usada para criar uma "função". Pense numa função como uma receita de bolo. Quando você usa `def`, você está escrevendo uma receita que pode ser seguida sempre que precisar.

Exemplo:

```py
def dizer_ola(nome):
    print("Olá, " + nome + "!")
```

Aqui, dizer_ola é a nossa receita. Quando você seguir essa receita e colocar um nome, vai ver a mensagem "Olá, nome!"

## Lógica Booleana

A lógica booleana usa operadores para fazer comparações e decisões. Os operadores principais são:

    Igual a (==): Verifica se dois valores são iguais.
    Não igual a (!=): Verifica se dois valores são diferentes.
    Maior que (>): Verifica se um valor é maior que outro.
    Menor que (<): Verifica se um valor é menor que outro.
    E (and): Verifica se ambas as condições são verdadeiras.
    Ou (or): Verifica se pelo menos uma das condições é verdadeira.
    Não (not): Inverte o valor lógico.

Exemplo:
```py
idade = 10
if idade >= 18:
    print("Você é adulto.")
else:
    print("Você é menor de idade.")
```

### Operadores Lógicos

`and`: O operador `and` retorna `True` se ambas as condições forem verdadeiras. Se qualquer uma das condições for falsa, o resultado será `False`.

Exemplo:
```py
a = 10
b = 20

resultado = (a > 5) and (b < 25)  # Ambas as condições são verdadeiras
print(resultado)  # Imprime True

resultado = (a > 15) and (b < 25)  # A primeira condição é falsa
print(resultado)  # Imprime False
```

`or`: O operador `or` retorna `True` se pelo menos uma das condições for verdadeira. O resultado é `False` apenas se todas as condições forem falsas.

Exemplo:
```py
a = 10
b = 20

resultado = (a > 5) or (b < 15)  # A primeira condição é verdadeira
print(resultado)  # Imprime True

resultado = (a > 15) or (b < 15)  # Ambas as condições são falsas
print(resultado)  # Imprime False
```

`not`: O operador `not` inverte o valor lógico de uma condição. Se a condição for `True`, `not` a torna False, e vice-versa.

Exemplo:
```py
a = 10

resultado = not (a > 5)  # A condição (a > 5) é verdadeira, então not a torna falsa
print(resultado)  # Imprime False

resultado = not (a > 15)  # A condição (a > 15) é falsa, então not a torna verdadeira
print(resultado)  # Imprime True
```

Combinações de `and`, `or`, e `not`

Você pode combinar esses operadores para construir expressões lógicas mais complexas.

Exemplo de combinação:
```py
a = 10
b = 20
c = 5

resultado = (a > 5) and (b < 25) or (c > 10)  # Primeiro, avalia (a > 5) e (b < 25) que são True, então or é True
print(resultado)  # Imprime True

resultado = not ((a > 5) and (b > 25))  # (a > 5) é True, (b > 25) é False, então and é False, not inverte para True
print(resultado)  # Imprime True

resultado = (a > 5) or not (b < 15)  # (a > 5) é True, not (b < 15) é not False, então or é True
print(resultado)  # Imprime True
```

Comparações Comuns

Aqui estão algumas comparações comuns e como os operadores lógicos funcionam com elas:

Verificação de Idade e Licença de Condução:
```py
idade = 17
tem_licenca = False

pode_dirigir = (idade >= 18) and tem_licenca
print(pode_dirigir)  # Imprime False (idade é menor que 18)
```

Verificação de acesso a um site baseado em idade ou assinatura:
```py
idade = 21
assinante = True

acesso = (idade >= 18) or assinante
print(acesso)  # Imprime True (idade é maior ou igual a 18)
```

Verificação se um número não está em um intervalo:
```py
numero = 15

fora_do_intervalo = not (10 <= numero <= 20)
print(fora_do_intervalo)  # Imprime False (número está dentro do intervalo)
```

## `if`

A palavra `if` é usada para fazer decisões. É como quando você pergunta se pode brincar se tiver terminado a lição de casa.

Exemplo:
```py
idade = 10
if idade >= 10:
    print("Você pode entrar no jogo!")
else:
    print("Você é muito jovem para esse jogo.")
```

Aqui, `if` verifica se a idade é maior ou igual a 10. Se for, ele mostra "Você pode entrar no jogo!" caso contrário, ele mostra "Você é muito jovem para esse jogo."

## `while`

A palavra `while` é usada para fazer algo repetidamente enquanto uma condição for verdadeira. É como se você estivesse jogando um jogo e continua jogando enquanto você não perdeu.

Exemplo:
```py
contador = 0
while contador < 5:
    print("Número:", contador)
    contador = contador + 1
```

Aqui, `while` faz o código dentro dele rodar enquanto contador for menor que 5. Então, ele mostra números de 0 a 4.

## Variáveis

Em Python, uma variável é como uma caixa onde você pode guardar um valor. Por exemplo, você pode ter uma variável chamada idade que guarda um número.

Exemplo:
```py
idade = 10
nome = "Ana"
```

## Tipos de Dados

Python tem vários tipos de dados. Aqui estão alguns dos mais comuns:

    Inteiros (int): Números sem ponto decimal. Exemplo: 5
    Flutuantes (float): Números com ponto decimal. Exemplo: 3.14
    Strings (str): Sequências de caracteres. Exemplo: "Olá"
    Booleanos (bool): Representam True (verdadeiro) ou False (falso). Exemplo: True

Exemplo:
```py
idade = 10        # int
altura = 1.75     # float
nome = "Ana"      # str
estudante = True  # bool
```

Para converter de um tipo ao outro existem varias funções como:
### `int`
converte uma `string` (texto) em `int` (inteiro)

Exemplo:
```py
a = "5" # str

# não se pode fazer contas com texto, a linha abaixo da erro
b = a + 4 # errado :(

# para fazer contas precisamos primeiro transformar o texto em número
numero_a = int(a) # transforma o texto "5" em número 5
b = numero_a + 4 # agora podemos fazer contas com o número :)
```

### `str`
converte uma `int` (inteiro) em `string` (texto)

Exemplo:
```py
a = 5 # int

# não se pode salvar números em arquivos de texto
escrever_arquivo(a) # da erro :(

# primeiro precisamos transformar o número em texto
texto_a = str(a) # transforma o número 5 em texto "5"
escrever_arquivo(texto_a) # agora podemos fazer escrever em arquivos :)
```

## Listas

Uma lista é uma coleção de itens que podem ser de diferentes tipos de dados. Você pode acessar, adicionar, e remover itens das listas.

Exemplo:

```py
frutas = ["maçã", "banana", "laranja"]

# Acessando um item
print(frutas[1])  # Imprime 'banana'

# Adicionando um item
frutas.append("uva")

# Removendo um item
frutas.remove("banana")

# Percorrendo a lista
for fruta in frutas:
    print(fruta)
```

## Variáveis Locais vs. Globais

    Variáveis Locais: Definidas dentro de uma função e só podem ser usadas dentro dessa função.
    Variáveis Globais: Definidas fora de qualquer função e podem ser usadas em qualquer lugar no código.

### Usando a Palavra-chave global

Quando você precisa modificar uma variável global dentro de uma função, você deve usar a palavra-chave global para dizer ao Python que está se referindo à variável global, não a uma nova variável local.

Exemplo sem global:
```py

numero = 10  # Variável global

def mudar_numero_para_um():
    numero = 1  # Isso cria uma nova variável local chamada `numero`
    print("Número dentro da função:", numero)

mudar_numero_para_um()
print("Número fora da função:", numero)  # Isso ainda será 10

```

Neste exemplo, numero dentro da função é uma nova variável local, não afeta a variável global numero.

Exemplo com global:
```py

numero = 10  # Variável global

def mudar_numero_para_um():
    global numero  # Diz ao Python que queremos usar a variável global `numero`
    numero = 1  # Modifica a variável global
    print("Número dentro da função:", numero)

mudar_numero_para_um()
print("Número fora da função:", numero)  # Isso será 1

```

Neste exemplo, ao usar global, a função `mudar_numero_para_um` modifica a variável global numero, e a mudança é refletida fora da função também.

