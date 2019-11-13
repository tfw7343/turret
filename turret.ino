//arduino uno

#include <Servo.h> 


Servo servoX;
servo servoY;

void setup() { 
  myservo.attach(5);
} 

void serialEvent() {
  cords = Serial.readString();

  servoX.write(parseDataX(cords));


}

void loop() {

}
