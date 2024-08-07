#include <Servo.h>

// Create servo objects for six servos
Servo servoA;
Servo servoB;
Servo servoC;
Servo servoD;
Servo servoE;
Servo servoF;

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  // Attach servos to their respective pins
  servoA.attach(3);  
  servoB.attach(5);  
  servoC.attach(6);  
  servoD.attach(9);  
  servoE.attach(10); 
  servoF.attach(11); 
}

void initialPos() {
  processCommand("motorA(15)");
  processCommand("motorB(10)");
  processCommand("motorC(85)");
  processCommand("motorD(0)");
  processCommand("motorE(0)");  // wrist
  processCommand("motorF(0)");  // claw 0 = open, 90 = closed
  processCommand("motorG(0)");
}


void openGrip() {
  processCommand("motorF(10)")
}


void closeGrip() {

}


void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read incoming command
    processCommand(command);
  }
}

void processCommand(String command) {
  // Example commands: "motorA(30)", "motorB(45)"
  char motor = command.charAt(5);  // Get motor identifier (A, B, C, D, E, F)
  int start = command.indexOf('(') + 1;
  int end = command.indexOf(')');
  int angle = command.substring(start, end).toInt();  // Get angle value

  switch (motor) {
    case 'A':
      servoA.write(angle);
      break;
    case 'B':
      servoB.write(angle);
      break;
    case 'C':
      servoC.write(angle);
      break;
    case 'D':
      servoD.write(angle);
      break;
    case 'E':
      servoE.write(angle);
      break;
    case 'F':
      servoF.write(angle);
      break;
    default:
      Serial.println("Invalid motor identifier");
      break;
  }
}
