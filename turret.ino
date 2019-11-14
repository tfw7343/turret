//arduino uno

#include <Servo.h> 

int LED;
Servo servoX;

void setup() { 
  Serial.begin(9600); 
  myservo.attach(5);
} 

void serialEvent() {
  cords = Serial.readString();

  servoX.write(cords);


}

void loop() {

}
