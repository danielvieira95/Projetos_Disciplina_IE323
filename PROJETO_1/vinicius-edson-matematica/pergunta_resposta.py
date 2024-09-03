from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C
import neopixel, time, utime

np = neopixel.NeoPixel(Pin(7), 25)
i2c = SoftI2C(scl=Pin(15), sda=Pin(14)) # configura Display oled no GP14
oled = SSD1306_I2C(128, 64, i2c)

class Question():
    def __init__(self,num_leds=25):
        self.NUM_LEDS = num_leds
        
    def limpa_matriz(self):
        for i in range(self.NUM_LEDS):
            np[i] = (0, 0, 0)
            np.write()

    def apagar_linha(self,linha):
        oled.fill_rect(0, linha, 128, 10, 0)  # Preenche um retângulo de 10 pixels de altura na linha especificada
        oled.show()
        
    def tempo(self):
        cont = 10 # Tempo de 10 segundos para o usuário ler e responder a pergunta (apenas para testes de projeto)
        while cont > 0:
            self.apagar_linha(50)
            oled.text("Tempo: {}".format(cont), 0, 50)
            oled.show()
            cont -= 1
            time.sleep(1) 
        oled.fill(0)  # Limpar display ao final do tempo
        oled.show()
        
    def pergunta01(self):
        # Suponha que a matriz de LED seja um gráfico com coordenadas (x,y), qual é o tipo de função apresentada? 
        self.limpa_matriz()
            #led.text("6543210987654321", 0, 70) #referencia 16 caracteres
        question01 = [24, 16, 12, 8, 0]

        for i in question01:
            np[i] = (2, 2, 2)
            np.write()
            
        oled.fill(0)
        oled.text("Qual e o tipo de",0,0)
        oled.text("funcao mostrada?",0,10)
        oled.show()
        self.tempo()
    
    def pergunta02(self):
        # Qual é a probabilidade de escolher um LED com a cor vermelha entre todas as cores apresentadas na matriz de LED?
        self.limpa_matriz()

        red = [0,2,5,7,8,12]
        green = [1,3,4,6,9,15,18,19,20,21]
        blue = [10,11,13,14,16,17,22,23,24]
        
        for i in red:
            np[i] = (2, 0, 0)
            np.write()
        for i in green:
            np[i] = (0, 2, 0)
            np.write()
        for i in blue:
            np[i] = (0, 0, 2)
            np.write()
            
        oled.fill(0)
        oled.text("Qual e a proba-",0,0)
        oled.text("bilidade de es-",0,10)
        oled.text("colher um LED",0,20)
        oled.text("vermelho na ma-",0,30)
        oled.text("triz de LEDs?",0,40)
        oled.show()
        self.tempo()
                
    def pergunta03(self):
        # Qual é a área e o perimetro do quadrado mostrado na matriz de leds?
        self.limpa_matriz()
    
        quadrado = [0,1,2,3,6,13,16,17,18,19,10,9,8,7,12,11]
        
        for i in quadrado:
            np[i] = (2, 2, 2)
            np.write()
        
        oled.fill(0)
        oled.text("Qual e a area",0,0)
        oled.text("e o perimetro do quadrado?",0,10)
        oled.text("do quadrado na",0,20)
        oled.text("matriz de LEDs?",0,30)
        oled.show()
        self.tempo()
 
    def pergunta04(self):
        #Qual é a distancia euclidiana ente os dois pontos mostrados na matriz de LEDs?
        self.limpa_matriz()
        
        np[0] = (2,2,2)
        np[24] = (2,2,2)
        np.write()
        
        oled.fill(0)
        oled.text("Qual e a distan-",0,0)
        oled.text("cia entre os ",0,10)
        oled.text("dois pontos na ",0,20)
        oled.text("matriz de LEDs?",0,30)
        oled.show()
        self.tempo() 
        
    def pergunta05(self):
        # Considerando que cada led verde é x e que cada led azul é y, qual é a expressão algébrica formada pela matriz de leds?
        self.limpa_matriz()
        
        azul = [0,1,2,4,5,8,10,15,22,23]
        verde = [3,6,7,9,11,12,13,14,16,17,18,19,20,21,24]
        
        for i in azul:
            np[i] = (0, 0, 2)
        for i in verde:
            np[i] = (0, 2, 0)
            
        np.write()
        
        oled.fill(0)
        oled.text("Se cada led ver-",0,0)
        oled.text("de eh x e cada",0,10)
        oled.text("led azul eh y. A",0,20)
        oled.text("expressao alge-",0,30)
        oled.text("brica formada e?",0,40)
        oled.show()
        self.tempo()

    def opcoes_oled(self, questao_selecionada, alternativa): # Função de resposta onde as opções serão exibidas no display oled

        if questao_selecionada ==0:
            if alternativa == 0:
                oled.fill(0)
                oled.text("Alternativa (A)",0,0)
                oled.text("Linear",0,10)
                oled.show()    
            elif alternativa == 1:
                oled.fill(0)
                oled.text("Alternativa (B)",0,0)
                oled.text("Exponencial",0,10)
                oled.show()   
            elif alternativa == 2:
                oled.fill(0)
                oled.text("Alternativa (C)",0,0)
                oled.text("Quadratica",0,10)
                oled.show()   
            elif alternativa == 3:
                oled.fill(0)
                oled.text("Alternativa (D)",0,0)
                oled.text("Logaritmica",0,10)
                oled.show()   
            elif alternativa == 4:
                oled.fill(0)
                oled.text("Alternativa (E)",0,0)
                oled.text("Modular",0,10)
                oled.show()   
        elif questao_selecionada ==1:
            if alternativa == 0:
                oled.fill(0)
                oled.text("Alternativa (A)",0,0)
                oled.text("1/5",0,10)
                oled.show()    
            elif alternativa == 1:
                oled.fill(0)
                oled.text("Alternativa (B)",0,0)
                oled.text("4/25",0,10)
                oled.show()   
            elif alternativa == 2:
                oled.fill(0)
                oled.text("Alternativa (C)",0,0)
                oled.text("6/25",0,10)
                oled.show()   
            elif alternativa == 3:
                oled.fill(0)
                oled.text("Alternativa (D)",0,0)
                oled.text("19/25",0,10)
                oled.show()   
            elif alternativa == 4:
                oled.fill(0)
                oled.text("Alternativa (E)",0,0)
                oled.text("1/25",0,10)
                oled.show()       
        elif questao_selecionada ==2:
            if alternativa == 0:
                oled.fill(0)
                oled.text("Alternativa (A)",0,0)
                oled.text("16 e 8",0,10)
                oled.show()    
            elif alternativa == 1:
                oled.fill(0)
                oled.text("Alternativa (B)",0,0)
                oled.text("16 e 16",0,10)
                oled.show()   
            elif alternativa == 2:
                oled.fill(0)
                oled.text("Alternativa (C)",0,0)
                oled.text("20 e 16",0,10)
                oled.show()   
            elif alternativa == 3:
                oled.fill(0)
                oled.text("Alternativa (D)",0,0)
                oled.text("4 e 16",0,10)
                oled.show()   
            elif alternativa == 4:
                oled.fill(0)
                oled.text("Alternativa (E)",0,0)
                oled.text("8 e 8",0,10)
                oled.show()         
        elif questao_selecionada ==3:
            if alternativa == 0:
                oled.fill(0)
                oled.text("Alternativa (A)",0,0)
                oled.text("4",0,10)
                oled.show()    
            elif alternativa == 1:
                oled.fill(0)
                oled.text("Alternativa (B)",0,0)
                oled.text("raiz(20)",0,10)
                oled.show()   
            elif alternativa == 2:
                oled.fill(0)
                oled.text("Alternativa (C)",0,0)
                oled.text("8",0,10)
                oled.show()   
            elif alternativa == 3:
                oled.fill(0)
                oled.text("Alternativa (D)",0,0)
                oled.text("16",0,10)
                oled.show()   
            elif alternativa == 4:
                oled.fill(0)
                oled.text("Alternativa (E)",0,0)
                oled.text("raiz(32)",0,10)
                oled.show()      
        elif questao_selecionada ==4:
            if alternativa == 0:
                oled.fill(0)
                oled.text("Alternativa (A)",0,0)
                oled.text("12x + 6y",0,10)
                oled.show()    
            elif alternativa == 1:
                oled.fill(0)
                oled.text("Alternativa (B)",0,0)
                oled.text("8x + 5y",0,10)
                oled.show()   
            elif alternativa == 2:
                oled.fill(0)
                oled.text("Alternativa (C)",0,0)
                oled.text("2x + 10y",0,10)
                oled.show()   
            elif alternativa == 3:
                oled.fill(0)
                oled.text("Alternativa (D)",0,0)
                oled.text("10y + 15x",0,10)
                oled.show()   
            elif alternativa == 4:
                oled.fill(0)
                oled.text("Alternativa (E)",0,0)
                oled.text("14y + 6x",0,10)
                oled.show()  
