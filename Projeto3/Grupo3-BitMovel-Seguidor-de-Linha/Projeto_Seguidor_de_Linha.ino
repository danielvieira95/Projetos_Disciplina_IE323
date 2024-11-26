/* 
Projeto educacional desenvolvido na disciplina IE323A - Tópicos em Eletrônica I
Equipe: 
Edson Costa Oliveira 
Vinicius Emanoel Ares

Professor: Dr. Fabiano Fruett
PED da disciplina: Me. Daniel Filipe Vieira

*/ 

/*
Nesse projeto foram utilizados os módulos INA226, HC-05 e ADS1115, além da matriz de LED. As bibliotecas necessárias
para o desenvolvido do código podem ser vistas abaixo.
*/

#include "SoftwareSerial.h"
#include <Wire.h>
#include <INA226_WE.h>
#include<ADS1115_WE.h>
#include <Adafruit_NeoPixel.h>

#define I2C_ADDRESS 0x40 // Endereço do módulo INA226
#define I2C_ADDRESS01 0x48 // Endereço do módulo ADS115
#define PIN 7             // Pino conectado a matriz de LED
#define NUM_LEDS 25       // Número total de LEDs (5x5 matriz)

Adafruit_NeoPixel np(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800); 
INA226_WE ina226 = INA226_WE(I2C_ADDRESS);
ADS1115_WE adc(I2C_ADDRESS01);
SoftwareSerial bluetooth(0, 1); //TX, RX (Bluetooth)

// DEFINIÇÃO DOS PINOS UTILIZADOS
const int buttonA = 5; // Pino do Botão A
const int buttonB = 6; // Pino do Botão B
const int STBY = 20;  // Standby do motor
const int IN1_A = 4;  // Canal A - direção
const int IN2_A = 9;  // Canal A - direção
const int PWM_A_PIN = 10; // Canal A - controle de velocidade
const int IN1_B = 18; // Canal B - direção
const int IN2_B = 19; // Canal B - direção
const int PWM_B_PIN = 16; // Canal B - controle de velocidade

// DECLARAÇÃO DE VARIÁVEIS
int switch_car = 0;
int velocidade = 256; // Velocidade máxima do motor
int kp=35,ki=0,kd=35; // Constantes do controle PID
int vel_A = 80, vel_B = 80; // Velocidade de cada motor
int I = 0, P = 0, D = 0, PID = 0; // Parcelas integrativas, proporcional e derivativa
int velesq = 0, veldir = 0; // Atualização de velocidade dos motores
int erro = 0, erro_anterior = 0; // erro de controle

int sensor[4] = {0,0,0,0}; // Definição de lista para sensores

float shuntVoltage_mV = 0.0;
float loadVoltage_V = 0.0;
float busVoltage_V = 0.0;
float current_mA = 0.0;
float power_mW = 0.0;

// Função para definir a velocidade da roda esquerda
void motor_forward_e(int vel) {
    digitalWrite(IN1_A, HIGH);
    digitalWrite(IN2_A, LOW);
    analogWrite(PWM_A_PIN, vel); 
}

// função para definir a velocidade da roda direita
void motor_forward_d(int vel) {
    digitalWrite(IN1_B, LOW);
    digitalWrite(IN2_B, HIGH);
    analogWrite(PWM_B_PIN, vel);
}

// Função para definir para parar os motores
void motor_stop() {
    analogWrite(PWM_A_PIN, 0);
    analogWrite(PWM_B_PIN, 0);
}

// Função para calcular o erro do controle PID
void calcula_erro() {
    if (sensor[0]==0 && sensor [1] == 1 && sensor[2]==1 && sensor[3]==0){erro=0;}
    else if (sensor[0]==0 && sensor [1] == 0 && sensor[2]==0 && sensor[3]==1){erro=2;}
    else if (sensor[0]==0 && sensor [1] == 0 && sensor[2]==1 && sensor[3]==0){erro=1;}
    else if (sensor[0]==0 && sensor [1] == 1 && sensor[2]==0 && sensor[3]==0){erro=-1;}
    else if (sensor[0]==1 && sensor [1] == 0 && sensor[2]==0 && sensor[3]==0){erro=-2;}
}

// Função para calcular o PID
void calculo_pid(){
    if(erro == 0){
      I= 0;
    }
    P = erro;
    I = I+erro;
    if (I>255){
      I==255;
    }
    else if (I<-255){
      I==-255;
    }
    D = erro - erro_anterior;
    PID = (kp*P) + (ki*I) + (kd*D);
    erro_anterior = erro; 
}

//Função para ajustar a velocidade dos motores do carrinho 
void controle(){
  if(PID>0){
velesq = vel_B;
veldir = vel_A - PID;
  }
  else {
    velesq = vel_B + PID;
    veldir = vel_A;
  }
 motor_forward_e(velesq);
 motor_forward_d(veldir); 
}

/*
Os vetores advance01, advance02, advance03 e stop01 representam os LEDs que serão acesos na matriz de LEDs
na execução do código.
*/

int advance01[] = {
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 1, 0, 0
};

int advance02[] = {
    0, 0, 0, 0, 0,
    0, 0, 0, 0, 0,
    0, 0, 1, 0, 0,
    0, 1, 1, 1, 0,
    1, 1, 1, 1, 1
};

int advance03[] = {
    0, 0, 1, 0, 0,
    0, 1, 1, 1, 0,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1
};

int stop01[] = {
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1,
    1, 1, 1, 1, 1
};

// As funções display_follow ligam os LEDs na matriz de LEDs
void display_follow(int state[]) {
    for (int i = 0; i < NUM_LEDS; i++) {
        if (state[i]) {
            np.setPixelColor(i, np.Color(0, 100, 0));  // Definindo a cor verde quando o carrinho estiver em movimento
        } else {
            np.setPixelColor(i, np.Color(0, 0, 0));   // Define a cor para apagado
        }
    }
    np.show();            // Atualiza a matriz com as novas cores
}

void display_stop(int state[]){
      for (int i = 0; i < NUM_LEDS; i++) {
        if (state[i]) {
            np.setPixelColor(i, np.Color(100, 0, 0));  // Definindo a cor vermelha para quando o carrinho estiver parado
        } else {
            np.setPixelColor(i, np.Color(0, 0, 0));   // Define a cor para apagado
        }
    }
    np.show();            // Atualiza a matriz com as novas cores
}

void setup() {
  Wire1.setSDA(2); // Definindo SDA do I2C1
  Wire1.setSCL(3); // Definindo SCL do I2C1
  Wire1.begin();
  Serial.begin(9600); // Taxa de comunicação serial
  bluetooth.begin(9600); // Taxa de comunicação serial

  // Definição dos pinos
  pinMode(buttonA, INPUT_PULLUP);
  pinMode(buttonB, INPUT_PULLUP);
  pinMode(STBY, OUTPUT);
  pinMode(IN1_A, OUTPUT);
  pinMode(IN2_A, OUTPUT);
  pinMode(IN1_B, OUTPUT);
  pinMode(IN2_B, OUTPUT);
  digitalWrite(STBY, HIGH); 

    if(!adc.init())
  {
    Serial.println("ADS1115 nao conectado!");
  }

  // Configurações iniciais do módulo ADS1115  
  adc.setVoltageRange_mV(ADS1115_RANGE_4096);
  adc.setCompareChannels(ADS1115_COMP_3_GND);
  adc.setMeasureMode(ADS1115_CONTINUOUS);

  // Configurações iniciais do módulo INA226
  ina226.init();
  ina226.setResistorRange(0.1, 1.3); // choose resistor 0.1 Ohm and gain range up to 1.3A
  ina226.setCorrectionFactor(0.93);
 
}

void loop() {

  if (loadVoltage_V > 7.25 && current_mA < 300){

  float voltages[4];

  // Checa se há algum byte recebido do bluetooth 
  if (bluetooth.available()) {
      //Ler e salva o byte na variável switch_car
      switch_car = bluetooth.read();
  }
    // Verifica se o botão A ou B foi pressionado
    if (digitalRead(buttonA) == LOW) {
        switch_car = 1;
    } else if (digitalRead(buttonB) == LOW) {
        switch_car = 0;
    }

// Lê os canais e armazena os valores em voltages 
    for (int i = 0; i < 4; i++) {
      switch (i) {
        case 0:
            voltages[i] = readChannel(ADS1115_COMP_0_GND);
            break;
        case 1:
            voltages[i] = readChannel(ADS1115_COMP_1_GND);
            break;
        case 2:
            voltages[i] = readChannel(ADS1115_COMP_2_GND);
            break;
        case 3:
            voltages[i] = readChannel(ADS1115_COMP_3_GND);
            break;
    }
    sensor[i] = (voltages[i] < 2.9) ? 0 : 1;
    }

    /* O switch_car, que pode ser alterado pelos botões ou por um comando via Bluetooth, contra o funcionamento do carrinho.
    Caso seja igual 1, o carrinho funciona, caso contrário, não funciona.
    */
    if (switch_car == 1) {
        calcula_erro();
        calculo_pid();
        controle();
    } 
    else {
        motor_stop();
    }
  }
  else {
    motor_stop();
  }
  // Salva os dados da bateria em uma variável externa
  ina226.readAndClearFlags();
  shuntVoltage_mV = ina226.getShuntVoltage_mV();
  busVoltage_V = ina226.getBusVoltage_V();
  current_mA = ina226.getCurrent_mA();
  power_mW = ina226.getBusPower();
  loadVoltage_V = busVoltage_V + (shuntVoltage_mV / 1000);

}

void setup1() {
    np.begin();           // Inicializa a matriz de LEDs
    np.show();            // LEDs estão apagados no início
}

void loop1(){

if (switch_car == 1){
    display_follow(advance01);
    delay(200);               
    display_follow(advance02);
    delay(200);               
    display_follow(advance03);
    delay(200);               
}

else {
  display_stop(stop01);
}

// Enviar dados formatados para o Bluetooth
    bluetooth.print(current_mA);
    bluetooth.print("|");
    bluetooth.print(power_mW);
    bluetooth.print("|");
    bluetooth.println(loadVoltage_V);

  delay(200);

}

float readChannel(ADS1115_MUX channel) 
{
  float voltage = 0.0;
  adc.setCompareChannels(channel);
  voltage = adc.getResult_V(); // alternative: getResult_mV for Millivolt
  return voltage;
}