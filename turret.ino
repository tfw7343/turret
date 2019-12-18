//arduino uno
#include <Servo.h> 
#include <stdlib.h>



String str;


int LED = 6;
int Laser = 5;
Servo servoX;
Servo servoY;
String ascii_servoX;
String ascii_servoY;


void setup() { 
  pinMode(Laser, OUTPUT);
  Serial.begin(9600);
  servoY.attach(5);
  servoX.write(0);
  servoX.attach(6);
  servoY.write(0);
} 


void serialEvent() {
  String tempModify = Serial.readString();
    
  if (tempModify == "laser_on") {
    digitalWrite(Laser, 255);
  } else {
    if (tempModify == "laser_off")
      digitalWrite(Laser, 0);
  }
  servoX.write(parseDataX(tempModify));
  servoY.write(parseDataY(tempModifu));
  Serial.println(parseDataX(tempModify));
}


int parseDataX(String data){
  data.remove(data.indexOf(":"));
  data.remove(data.indexOf("("));
  data.remove(data.indexOf(")"));
  data.remove(data.indexOf("X"), 2);

  return data.toInt();
}

int parseDataY(String data){
  data.remove(0,data.indexOf(":") + 1);
  data.remove(data.indexOf("Y"), 1);
  data.remove(data.indexOf("("));
  data.remove(data.indexOf(")"));
  return data.toInt();
  
}


void loop() {
//u w0t m8!?!?!!
}
