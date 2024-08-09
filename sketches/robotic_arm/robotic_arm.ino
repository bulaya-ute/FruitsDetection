
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
  processCommand("motorA(0)");  // BASE
  processCommand("motorB(60)");
  processCommand("motorC(160)");
  processCommand("motorD(20)");
  processCommand("motorE(120)");  // wrist
  openGrip();                     // claw 30 = open, 85 = closed
  processCommand("motorG(10)");
}


void openGrip() {
  processCommand("motorF(30)");
}


void closeGrip() {
  processCommand("motorF(85)");
}


void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read incoming command
    processCommand(command);
  }
}

void processCommand(String command) {
  String response;
  if (command == "openGrip") {
    openGrip();
    response = "Grip opened.";
  } else if (command == "closeGrip") {
    closeGrip();
    response = "Grip closed.";
  } else {
    // Example commands: "motorA(30)", "motorB(45)"
    char motor = command.charAt(5);  // Get motor identifier (A, B, C, D, E, F)
    int start = command.indexOf('(') + 1;
    int end = command.indexOf(')');
    int angle = command.substring(start, end).toInt();  // Get angle value
    response = "Motor " + motor + String(angle) + " degrees.";
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
        response = ("Invalid command: " + command);
        break;
    }
  }

  delay(2000);
  Serial.println(response);
}