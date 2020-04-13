// NewPing - Version: Latest 
#include <NewPing.h>

// SENSORS
#define TRIGGER_PIN  7  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
int min_safe_dist_cm = 25; // Maximum range needed

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // Creating the NewPing Object.

//ACTUATORS
//L293D
//Motor A
const int motorPin1  = 5;  // Pin 14 of L293
const int motorPin2  = 6;  // Pin 10 of L293
//Motor B
const int motorPin3  = 10; // Pin  7 of L293
const int motorPin4  = 11;  // Pin  2 of L293

char receivedChar;
boolean newData = false;

void setup() {

  Serial.begin(9600);

  //Set pins as outputs
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  
}

void loop() {

  recvInfo();
  Move();
  
}

void recvInfo() {

  if (Serial.available() > 0) {

    receivedChar = Serial.read();
    newData = true;
    Serial.print("You sent: ");
    Serial.println(receivedChar);
    
  }
  
}

void Move() {

  while(newData == true) {

    if (receivedChar == 'F'){
      // Drive forward
      Serial.print("Driving forward for 500ms.");
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, HIGH);
    }
    if (receivedChar == 'R'){
      
      // Turn right
      Serial.print("Turning right for 500ms.");
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, HIGH);
      digitalWrite(motorPin4, LOW);
    }
    if (receivedChar == 'L'){
      
      // Turn right
      Serial.print("Turning left for 500ms.");
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, HIGH);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, HIGH);
    }
    if (receivedChar == 'B'){
      
      // Turn right
      Serial.print("Moving backward for 500ms.");
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, HIGH);
      digitalWrite(motorPin3, HIGH);
      digitalWrite(motorPin4, LOW);
    }
    if (receivedChar == 'S'){
      
      // Turn right
      Serial.print("Stopping.");
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, LOW);
    }
    newData = false;
    delay(500);
    
  }
  
}