//arduino uno
#include <Servo.h> 
#include <stdlib.h>



String str;


int LED = 6;
Servo servoX;
Servo servoY;
String ascii_servoX;
String ascii_servoY;


void setup() { 
  Serial.begin(9600);
  servoY.attach(5);
  servoX.write(0);
  servoX.attach(6);
  servoY.write(0);
} 


void serialEvent() {
  String tempModify = Serial.readString();
  
  servoX.write(parseDataX(tempModify));
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

}
