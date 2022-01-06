#include <Servo.h>

// create servo objects to control the servos
Servo servoleft; // left servo
Servo servoright; // right servo

const int numChars = 8;
char c[numChars]; // an array to store the received data
String cc, c1, c2; //strings to save the received data
double n1 = 90; //initial position of left servo
double n2 = 90; //initial position of right servo
boolean newData = false;

void setup() {

  Serial.begin(9600);

  // Attaches servos to digital pins 11 and 12(verticle axis) on the BotBoarduino
  servoleft.attach(11);
  servoright.attach(12);
  // pass the recieved data to servos
  servoleft.write(n1);
  servoright.write(n2);

  //Serial.println("<Servos are ready!>");
}

void loop() {
  servopos();
  cc = String(c);
  c1 = cc.substring(0, 3);
  c2 = cc.substring(4, 7);
  n1 = c1.toDouble();
  n2 = c2.toDouble();
  Serial.print("n1 is ");
  Serial.println(n1);
  Serial.print("n2 is ");
  Serial.println(n2);
  if (n1 > 0 && n1 < 180) {
    servoleft.write(n1);
  }
  else{
    Serial.println("Warning! Input exceeds the left servo working space!");
  }
  if (n2 > 0 && n2 < 180) {
    servoright.write(n2);
  }
  else{
    Serial.println("Warning! Input exceeds the right servo working space!");
  }
  showservopos();
  delay(10);
}

void servopos() { //get the recieved data

  int nd = 0;
  char posEnd = '\n'; //mark the end of input
  char rc; //a character to store the recieved data

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read(); //recieve data

    if (rc != posEnd) {
      c[nd] = rc;
      nd++;
      if (nd >= numChars) {
        nd = numChars - 1;
      }
    }
    else {
      c[nd] = '\0'; // terminate the string
      nd = 0;
      newData = true;
    }
  }
}

void showservopos() {
  if (newData == true) {
    Serial.println(c);
    newData = false;
  }
}
