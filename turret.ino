//arduino uno

#include <Servo.h> 


Servo servoX;

void setup() { 
  Serial.begin(9600); 
  myservo.attach(5);
} 

void serialEvent() {
  cords = Serial.readString();

  servoX.write(parseDataX(cords));


}

void loop() {

}
