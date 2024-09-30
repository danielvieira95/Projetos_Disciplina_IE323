
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

const int sensor01 = 0; // Pino do sensor reflexivo 1
const int sensor02 = 1; // Pino do sensor reflexivo 2
const int sensor03 = 2; // Pino do sensor reflexivo 3
const int sensor04 = 3; // Pino do sensor reflexivo 4

// DECLARAÇÃO DE VARIÁVEIS
int velocidade = 256; // Velocidade máxima do motor
int kp=35,ki=0,kd=35; // Constantes do controle PID
int vel_A = 80, vel_B = 80; // Velocidade de cada motor
int I = 0, P = 0, D = 0, PID = 0; // Parcelas integrativas, proporcional e derivativa
int velesq = 0, veldir = 0; // Atualização de velocidade dos motores
int erro = 0, erro_anterior = 0; // erro de controle

int sensor[4] = {0,0,0,0}; // Definição de lista para sensores

void setup() {
  Serial.begin(250000); // Taxa de comunicação serial
  // Definição dos pinos
  pinMode(buttonA, INPUT_PULLUP);
  pinMode(buttonB, INPUT_PULLUP);
  pinMode(STBY, OUTPUT);
  pinMode(IN1_A, OUTPUT);
  pinMode(IN2_A, OUTPUT);
  pinMode(IN1_B, OUTPUT);
  pinMode(IN2_B, OUTPUT);
  pinMode(sensor01, INPUT);
  pinMode(sensor02, INPUT);
  pinMode(sensor03, INPUT);
  pinMode(sensor04, INPUT);
  digitalWrite(STBY, HIGH); 

    
}

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

void loop() {
    static int var = 0;

    // Verificação de botão pressionado
    if (digitalRead(buttonA) == LOW) {
        var = 1;
    } else if (digitalRead(buttonB) == LOW) {
        var = 0;
    }

    // Leitura dos sensores
    sensor[0] = digitalRead(sensor01);
    sensor[1] = digitalRead(sensor02);
    sensor[2] = digitalRead(sensor03);
    sensor[3] = digitalRead(sensor04);

    // Se o botão A for ativado, então o carrinho segue linha
    if (var == 1) {
        calcula_erro();
        calculo_pid();
        controle();
    } // Caso contrário, ou se o botão B for pressionado, o carrinho para de seguir linha
    else {
        motor_stop();
    }
}
