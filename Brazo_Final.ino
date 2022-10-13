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
 
int pin=3;
int pin2=5;
int pin3=6;
int pin4=9;
int pulsoMinimo = 580;  // Duración en microsegundos del pulso para girar 0º
int pulsoMaximo = 2500; // Duración en microsegundos del pulso para girar 180º
int angulo = 0; // Variable para guardar el angulo que deseamos de giro
boolean e =false;
int mssg,posServox,posServoy;
String cad="",cad2="",color="";
int pos;
 
void setup()
{
  //Inicializamos el servo y el Serial:
  servo1.attach(pin); //Servo base
  servo2.attach(pin2); //Servp codo derecho 
  servo3.attach(pin3); //Servo codo izquierdo
  servo4.attach(pin4); //Servo pinza
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  servo3.write(140); // codo izquierdo arriba
  delay(2000);
  servo4.write(180); //abre pinza
  delay(2000);
}
 
void loop()
{
  if(entradaCompleta) {
   

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
  recoger();
  for (int i = 90 ; i>40;i--){
    servo1.write(i); //Movemos el servo de base a angulo 0 lado Derecho
     delay(10);
   }
  soltar();
  Serial.print(c);
}
void moverVerde(String c){
  recoger();
  for (int i = 90 ; i>20;i--){
    servo1.write(i); //Movemos el servo de base a angulo 0 lado Derecho
     delay(10);
   }
  soltar();
  Serial.print(c);
}
void moverAzul(String c){
  recoger();
  for (int i = 90 ; i>0;i--){
    servo1.write(i); //Movemos el servo de base a angulo 0 lado Derecho
     delay(10);
   }
  soltar();
  Serial.print(c);}

void recoger(){
  servo1.write(posServox / 4);
   delay(2000);
   servo2.write(posServoy / 3);
   delay(2000);
  ///////////////////MOVIMIENTO PREDETERMINADO///////////////////////

   ////////////////////////////////////////////////////
   for (int i=140;i>100;i--){ //codo izquierdo abajo
    servo3.write(i);
    delay(15);
   }
   delay(3000);
   ////////////////////////////////////////////////////
   servo4.write(155); // cierra pinza
   delay(1000);
   ///////////////////////////////////////////////////
   for (int i=100;i<=140;i++){ //codo izquierdo arriba
    servo3.write(i);
    delay(15);
   }
   delay(2000);
}


void soltar(){
   delay(3000);
   ///////////////////////////////////////////////////
   for (int i=140;i>100;i--){ //codo izquierdo abajo
    servo3.write(i);
    delay(15);
   }
   delay(2000);
   //////////////////////////////////////////////////
   servo4.write(180); //abre pinza
   delay(2000);
   //////////////////////////////////////////////////
   for (int i=100;i<=140;i++){ //codo izquierdo arriba
    servo3.write(i);
    delay(15);
   }
   delay(2000);
   ////////////////////////////////////////////////////
   for (int i=0;i<=90;i++){ //vuelve a la posicion inicial
    servo1.write(i);
    delay(15);
   }
   delay(1000);
}
