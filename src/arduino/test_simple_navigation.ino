// NewPing - Version: Latest 
#include <NewPing.h>


// SENSORS
#define TRIGGER_PIN  7  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     8  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // Creating the NewPing Object.


//ACTUATORS
//L293D
//Motor A
const int motorPin1  = 5;  // Pin 14 of L293
const int motorPin2  = 6;  // Pin 10 of L293
//Motor B
const int motorPin3  = 10; // Pin  7 of L293
const int motorPin4  = 11;  // Pin  2 of L293

void setup() {
  Serial.begin(9600); // Begin serial com. at 115200 baud rate.
  
  //Set pins as outputs
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
}

void loop() {
  
  unsigned int uS = sonar.ping(); // Send ping, get ping time in microseconds (uS). Pings every 500ms, as per the delay set in the loop below. 29ms should be the shortest ping delay.
  Serial.print("Ping: ");
  unsigned int distance_cm = uS / US_ROUNDTRIP_CM; // Convert ping time to distance in cm and print result (0 = outside set distance range)
  Serial.print(distance_cm); // Convert ping time to distance in cm and print result (0 = outside set distance range)
  Serial.println("cm"); //If you would like ping in inches, remove "US_ROUNDTRIP_CM" and the backslash, don't forget to rename "cm" to "inches"
  
  // If there is an obstacle ahead, turn left for half a second
  if 0 < distance_cm < 25:
  
    // Turn left
    Serial.print("Turning left for 500ms.")
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
    digitalWrite(motorPin3, LOW);
    digitalWrite(motorPin4, HIGH);
    delay(500);
  
  else:
  
    // Drive forward
    Serial.print("Driving forward for 500ms.")
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
    digitalWrite(motorPin3, HIGH);
    digitalWrite(motorPin4, LOW);
    delay(500);

}


