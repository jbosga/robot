// NewPing - Version: Latest 
#include <NewPing.h>


// SENSORS
#define TRIGGER_PIN  7  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
int min_safe_dist_cm = 35; // Maximum range needed

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // Creating the NewPing Object.

//ACTUATORS
//L293D
//Motor A
const int motorPin1  = 5;  // Pin 14 of L293
const int motorPin2  = 6;  // Pin 10 of L293
//Motor B
const int motorPin3  = 10; // Pin  7 of L293
const int motorPin4  = 11;  // Pin  2 of L293
//Enable pin (controls both motors)
const int motorEnablePin = 3;


char receivedChar;
char command = 'S';
char lastReceivedCommand = command;
unsigned int speed = 0;
unsigned int distance_cm;
boolean newData = false;


void setup() {

  Serial.begin(9600);

  //Set pins as outputs
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(motorEnablePin, OUTPUT);
}

void loop() {

  getCommand();
  pingSonar();
  Move();
  
}

void pingSonar() {

    unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS). Pings every 500ms, as per the delay set in the loop below. 29ms should be the shortest ping delay.
    // Serial.print("Ping: ");
    distance_cm = uS / US_ROUNDTRIP_CM; // Convert ping time to distance in cm and print result (0 = outside set distance range)
    // Serial.println(distance_cm); // Convert ping time to distance in cm and print result (0 = outside set distance range)
}

void getCommand() {

  if (Serial.available() > 0) {

    receivedChar = Serial.read();
    Serial.print("Received: ");
    Serial.println(receivedChar);
    if ((receivedChar != lastReceivedCommand)&&(receivedChar=='S' || receivedChar=='Q' || receivedChar=='M')){
      command = receivedChar;
      
      lastReceivedCommand = command;
    }
    if (receivedChar=='M'){
      receivedChar = Serial.read();
      Serial.print("Received: ");
      Serial.println(receivedChar);
      speed = receivedChar - '0';
      Serial.println(speed);

      speed = (255 / 10) * speed;
      Serial.println(speed);
    }
  }
  
}

void Move() {

  if(command=='Q'){
      executeMoveSet();
  }
  if(command=='S'){
    Stop();
  }
  if(command=='M'){
      basicMove();
  }
}


void basicMove(){
    // Serial.print("Ping2: ");
    // Serial.println(distance_cm);
    if (distance_cm < min_safe_dist_cm){
        // Turn right
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, HIGH);
        digitalWrite(motorPin4, LOW);
        analogWrite(motorEnablePin, speed);
        }
    else{
        // Drive forward
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, LOW);
        digitalWrite(motorPin4, HIGH);
        analogWrite(motorEnablePin, speed);
        }
}

void Stop(){
  digitalWrite(motorPin1, LOW);
  digitalWrite(motorPin2, LOW);
  digitalWrite(motorPin3, LOW);
  digitalWrite(motorPin4, LOW);
}

void executeMoveSet(){
    ;
}