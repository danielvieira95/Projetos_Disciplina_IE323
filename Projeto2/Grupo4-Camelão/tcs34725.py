import utime  # Módulo para funções de temporização
import ustruct  # Módulo para manipulação de dados em formato binário

# Definição de constantes usadas para configurar o sensor TCS34725
_COMMAND_BIT = const(0x80)  # Bit de comando, necessário para acessar registros

# Registros do sensor
_REGISTER_ENABLE = const(0x00)  # Registro de habilitação do sensor
_REGISTER_ATIME = const(0x01)  # Tempo de integração de dados
_REGISTER_AILT = const(0x04)  # Limite inferior para interrupções de luz ambiente
_REGISTER_AIHT = const(0x06)  # Limite superior para interrupções de luz ambiente
_REGISTER_ID = const(0x12)  # Registro de identificação do sensor
_REGISTER_APERS = const(0x0c)  # Configuração de persistência da interrupção
_REGISTER_CONTROL = const(0x0f)  # Controle do ganho do sensor
_REGISTER_SENSORID = const(0x12)  # Identificador do sensor
_REGISTER_STATUS = const(0x13)  # Registro de status
_REGISTER_CDATA = const(0x14)  # Dados do canal claro (Clear)
_REGISTER_RDATA = const(0x16)  # Dados do canal vermelho (Red)
_REGISTER_GDATA = const(0x18)  # Dados do canal verde (Green)
_REGISTER_BDATA = const(0x1a)  # Dados do canal azul (Blue)

# Máscaras de bits para habilitar recursos no sensor
_ENABLE_AIEN = const(0x10)  # Habilitar interrupção de luz ambiente
_ENABLE_WEN = const(0x08)  # Habilitar detecção de luz ambiente
_ENABLE_AEN = const(0x02)  # Habilitar o ADC (Conversor Analógico-Digital)
_ENABLE_PON = const(0x01)  # Habilitar o sensor (Power ON)

# Valores de ganho suportados pelo sensor
_GAINS = (1, 4, 16, 60)  # Ganhos possíveis para amplificação dos dados de cor

# Ciclos de persistência para interrupção, usados para controle da frequência de interrupções
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)

# Definição da classe TCS34725, que controla o sensor de cor
class TCS34725:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c  # Objeto de comunicação I2C
        self.address = address  # Endereço padrão do sensor
        self._active = False  # Estado de ativação do sensor
        self.integration_time(2.4)  # Define o tempo de integração padrão para 2.4 ms
        sensor_id = self.sensor_id()  # Obtém o ID do sensor
        # Verifica se o sensor conectado é válido
        if sensor_id not in (0x44, 0x10, 0x4d):
            raise RuntimeError("wrong sensor id 0x{:x}".format(sensor_id))

    # Função para ler ou escrever em um registro de 8 bits
    def _register8(self, register, value=None):
        register |= _COMMAND_BIT  # Adiciona o bit de comando ao endereço do registro
        if value is None:
            # Se nenhum valor for passado, lê o valor do registro
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        # Caso contrário, escreve o valor no registro
        data = ustruct.pack('<B', value)  # Converte o valor em formato de 8 bits
        self.i2c.writeto_mem(self.address, register, data)

    # Função para ler ou escrever em um registro de 16 bits
    def _register16(self, register, value=None):
        register |= _COMMAND_BIT  # Adiciona o bit de comando ao endereço do registro
        if value is None:
            # Se nenhum valor for passado, lê dois bytes do registro
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack('<H', data)[0]  # Desempacota os dados em formato de 16 bits
        # Caso contrário, escreve o valor no registro
        data = ustruct.pack('<H', value)  # Converte o valor em formato de 16 bits
        self.i2c.writeto_mem(self.address, register, data)

    # Ativa ou desativa o sensor
    def active(self, value=None):
        if value is None:
            return self._active  # Retorna o estado atual do sensor
        value = bool(value)  # Converte o valor para booleano
        if self._active == value:
            return  # Se o estado atual já for o desejado, não faz nada
        self._active = value  # Atualiza o estado
        enable = self._register8(_REGISTER_ENABLE)  # Lê o registro de habilitação
        if value:
            # Se o sensor deve ser ativado, habilita o sensor e o ADC
            self._register8(_REGISTER_ENABLE, enable | _ENABLE_PON)
            utime.sleep_ms(3)  # Espera 3 ms
            self._register8(_REGISTER_ENABLE,
                            enable | _ENABLE_PON | _ENABLE_AEN)
        else:
            # Se deve ser desativado, desliga o sensor
            self._register8(_REGISTER_ENABLE,
                            enable & ~(_ENABLE_PON | _ENABLE_AEN))

    # Obtém o ID do sensor
    def sensor_id(self):
        return self._register8(_REGISTER_SENSORID)

    # Define ou obtém o tempo de integração
    def integration_time(self, value=None):
        if value is None:
            return self._integration_time  # Retorna o tempo de integração atual
        # Limita o valor de tempo de integração entre 2.4 e 614.4 ms
        value = min(614.4, max(2.4, value))
        cycles = int(value / 2.4)  # Converte o tempo em ciclos
        self._integration_time = cycles * 2.4  # Armazena o tempo de integração calculado
        return self._register8(_REGISTER_ATIME, 256 - cycles)  # Define o valor no registro ATIME

    # Define ou obtém o ganho do sensor
    def gain(self, value):
        if value is None:
            return _GAINS[self._register8(_REGISTER_CONTROL)]  # Retorna o ganho atual
        if value not in _GAINS:
            raise ValueError("gain must be 1, 4, 16 or 60")  # Verifica se o valor é válido
        return self._register8(_REGISTER_CONTROL, _GAINS.index(value))  # Define o ganho

    # Verifica se os dados são válidos
    def _valid(self):
        return bool(self._register8(_REGISTER_STATUS) & 0x01)

    # Lê os dados de cor do sensor
    def read(self, raw=False):
        was_active = self.active()  # Armazena o estado atual do sensor
        self.active(True)  # Ativa o sensor
        while not self._valid():
            # Aguarda até que os dados estejam disponíveis
            utime.sleep_ms(int(self._integration_time + 0.9))
        # Lê os dados dos canais de cor
        data = tuple(self._register16(register) for register in (
            _REGISTER_RDATA,
            _REGISTER_GDATA,
            _REGISTER_BDATA,
            _REGISTER_CDATA,
        ))
        self.active(was_active)  # Restaura o estado anterior do sensor
        if raw:
            return data  # Retorna os dados crus
        return self._temperature_and_lux(data)  # Calcula e retorna a temperatura de cor e o lux

    # Calcula a temperatura de cor e a luminosidade
    def _temperature_and_lux(self, data):
        r, g, b, c = data  # Desempacota os dados de cor
        # Converte os dados de cor em XYZ (modelo de cor usado para calcular a temperatura de cor)
        x = -0.14282 * r + 1.54924 * g + -0.95641 * b
        y = -0.32466 * r + 1.57837 * g + -0.73191 * b
        z = -0.68202 * r + 0.77073 * g + 0.56332 * b
        d = x + y + z  # Soma dos valores de cor
        # Calcula o valor do nCIE (temperatura de cor correlata)
        n = (x / d - 0.3320) / (0.1858 - y / d)
        # Calcula a temperatura de cor correlata em Kelvin
        cct = 449.0 * n**3 + 3525.0 * n**2 + 6823.3 * n + 5520.33
        return cct, y  # Retorna a temperatura de cor e a luminosidade (lux)

