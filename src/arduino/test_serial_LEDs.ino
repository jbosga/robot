char receivedChar;
boolean newData = false;

void setup() {

  Serial.begin(9600);

  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  
}

void loop() {

  recvInfo();
  lightLED();
  
}

void recvInfo() {

  if (Serial.available() > 0) {

    receivedChar = Serial.read();
    newData = true;
    Serial.print("You sent: ");
    Serial.println(receivedChar);
  }
  
}

void lightLED() {

  int led = (receivedChar - '0');

  while(newData == true) {

    digitalWrite(led, HIGH);
    delay(2000);
    digitalWrite(led, LOW);

    newData = false;
    
  }
  
}