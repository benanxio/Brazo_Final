#include <Servo.h>
#include <LiquidCrystal_I2C.h>

//Crear el objeto lcd  dirección  0x3F y 16 columnas x 2 filas
LiquidCrystal_I2C lcd(0x27,16,2);  //
Servo servo1; // BASE
Servo servo2; // CODO DERECHO MAXIMO ADELANTE 130, ATRAS 40 MINIMO
Servo servo3; // CODO IZQUIERDO 160 MAXIMO ARRIBA, ABAJO 100 MINIMO
Servo servo4; // PINZA ABRE 180, CIERRA 165 
 
String entradaSerial = "";         // String para almacenar entrada
bool entradaCompleta = false;  // Indicar si el String está completo
 
int pin = 3;    // pin de conexión PWM al servo
int pin2 = 5;
int pulsoMinimo = 580;  // Duración en microsegundos del pulso para girar 0º
int pulsoMaximo = 2500; // Duración en microsegundos del pulso para girar 180º
int angulo = 0; // Variable para guardar el angulo que deseamos de giro
boolean e =false;
int mssg,posServox,posServoy;
String cad="",cad2="",color="";
int pos;
 
void setup()
{
  servo1.attach(pin, pulsoMinimo, pulsoMaximo);
  servo2.attach(pin2,pulsoMinimo, pulsoMaximo);
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
}
 
void loop()
{
  if(entradaCompleta) {
  
    posServox = posServox/8;
    posServoy = posServoy/4;
    servo1.write(posServox);
    servo2.write(posServoy);
    lcd.print("X = "+String(posServox)+"Y"+String(posServoy));
    delay(20);
       
    if (cad2 == "movobj\n"){
        //posServo = posServo / 4;
        for(int x=posServox;x<=170;x++){
         servo1.write(x);
         delay(10);
        }
     }
      
    if (cad2 == "ClassColorR\n"){
        color = cad2.substring(10);//Obtengo el color que voy a clasificar
        moverRojo(color);
     }
     if (cad2 == "ClassColorG\n"){
        color = cad2.substring(10);//Obtengo el color que voy a clasificar
        moverVerde(color);
     }
     if(cad2 == "ClassColorB\n"){
        color = cad2.substring(10);//Obtengo el color que voy a clasificar
        moverAzul(color);
     }
    
    entradaSerial = "";
    entradaCompleta = false;
    cad="";
    cad2="";
    color = "";
 }
}
// Función que se activa al recibir algo por
// el puerto serie, Interrupción del Puerto Serie.
void serialEvent(){
  while(Serial.available()>0) {
    // Obtener bytes de entrada:
    char inChar = (char)Serial.read();
    // Agregar al String de entrada:
    entradaSerial += inChar;
    
    // Para saber si el string está completo, se detendrá al recibir
    // el caracter de retorno de línea ENTER \n
    if (inChar == '\n') {
      pos = entradaSerial.indexOf(','); // guardamos la posicion de la coma
      posServox = entradaSerial.substring(0,pos).toInt();
      entradaSerial = entradaSerial.substring(pos+1); // guarda todo despues de la coma :v

      
      pos = entradaSerial.indexOf(',');
      posServoy = entradaSerial.substring(0,pos).toInt();// guarda todo antes de la coma
      cad2 = entradaSerial.substring(pos+1); // guarda todo despues de la coma :v
      entradaCompleta = true; 
    }
  }
}


void moverRojo(String c){
  delay(5000);//En vez de esto van las instrucciones de movimiento
  Serial.print(c);
}
void moverVerde(String c){
  delay(5000);//En vez de esto van las instrucciones de movimiento
  Serial.print(c);
}
void moverAzul(String c){
  delay(5000);//En vez de esto van las instrucciones de movimiento
  Serial.print(c);
}
