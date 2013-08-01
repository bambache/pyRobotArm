#include <Servo.h> 

const int NMB = 5;
Servo servos[NMB];
//Servo myclaw;
//Servo myelbow;
//Servo mywrist;
// create servo object to control a servo 
// a maximum of eight servo objects can be created            

const int INC = 5; // angle increment in degrees
const int CONSTRAINTS[NMB][2] = { {20, 120}, {30, 180}, {0, 180}, {0, 180}, {0, 180} };
const int PINS[NMB] = {3, 5, 6, 9 ,10};
//const int CLAW[]  = {20, 120};
//const int ELBOW[] = {30, 180};
//const int WRIST[] = {0,  180};

void printState()
{
  for (int i=0; i < NMB; ++i) {
    Serial.print(servos[i].read());
    if (i != NMB-1) Serial.print(',');
  }
  
  //Serial.print(myclaw.read());  Serial.print(',');
  //Serial.print(mywrist.read()); Serial.print(',');
  //Serial.print(myelbow.read());
  Serial.println();
}

void allHome()
{
  // set servos to mid-point
  for (int i=0; i < NMB; ++i) {
    servos[i].writeMicroseconds(1500);
  }
  //myclaw.writeMicroseconds(1500);
  //mywrist.writeMicroseconds(1500);
  //myelbow.writeMicroseconds(1500);
}

void moveServo(int ac_ServoIdx, int ac_Inc) 
{
  if (ac_ServoIdx < 0 || ac_ServoIdx >= NMB)
    return;
  //int pos = servos[ac_ServoIdx].read();
  int pos = constrain( /*pos +*/ ac_Inc, CONSTRAINTS[ac_ServoIdx][0], CONSTRAINTS[ac_ServoIdx][1] );
  servos[ac_ServoIdx].write(pos);
  delay(15);
}

void setup() 
{ 
  //open serial
  Serial.begin(9600);
  for (int i=0; i < NMB; ++i) {
    servos[i].attach(PINS[i]);
  }
  //myclaw.attach(3);  // attaches the servo on pin 3 to the servo object 
  //mywrist.attach(5);  // attaches the servo on pin 6 to the servo object 
  //myelbow.attach(6);  // attaches the servo on pin 6 to the servo object 

  allHome();
} 

void loop() 
{   
  
  // if there's any serial available, read it:
  while (Serial.available() > 0) {
    int values[NMB];
    // look for the next valid integer in the incoming serial stream:
    for (int i = 0; i < NMB; ++i) {
      values[i] = Serial.parseInt(); 
    }
    
    // look for the newline. That's the end of your
    // sentence:
    if (Serial.read() == '\n') {
      
      Serial.print('<');
      for (int i = 0; i < NMB; ++i) {
        Serial.print(values[i]);
        if (i != NMB-1) Serial.print(',');
        
        moveServo(i, values[i]);
      }
      Serial.println('>');   
          
      printState();
    }
  }

//    if (Serial.available() > 0) {     
//     int inByte = Serial.read();
//     switch (inByte) {
//      case 'A':    
//        moveServo(myclaw, INC, CLAW);
//        break;
//      case 'a':    
//        moveServo(myclaw, -INC, CLAW);
//        break;
//      case 'S':    
//        moveServo(mywrist, INC, WRIST);
//        break;
//      case 's':    
//        moveServo(mywrist, -INC, WRIST);
//        break;
//      case 'D':    
//        moveServo(myelbow, INC, ELBOW);
//        break;
//      case 'd':    
//        moveServo(myelbow, -INC, ELBOW);
//        break;
//      
//      default:
//        allHome();
//
//      } 
} 
