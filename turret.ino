//arduino uno
#include <Servo.h> 
#include <stdlib.h>


String str;

int LED = 6;
Servo servoX;
String ascii_servoX;
String ascii_servoY;


void setup() { 
  Serial.begin(9600);
  servoX.attach(5);
  servoX.write(0);
} 

void serialEvent() {

  String num1 = Serial.readString();
  int num = num1.toInt();
  
  if (num1 == "420") {
    analogWrite(LED, 0);
    }
  if (num1 == "69") {
    analogWrite(LED, 255);
    }
  if (num1 == "666") {
    
    }
  Serial.println(num1);
  
  servoX.write(num);
  
}
