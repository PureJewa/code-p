#include <Arduino.h>
#include <Wire.h>


//Onderste rij relais van links naar rechts
#define RelayProgrammeer 53
#define RelayInit 51
#define RelayStart 49
#define RelayHervat 47
#define RelayPauze 45
#define RelayBarcode 43
#define RelayTD 41
#define RelayCTD 39

//Bovenste rij relais van links naar rechts
#define Relay9 37
#define Relay10 35
#define Relay11 33
#define RelayRoodLicht 31
#define RelayGeelLicht 29
#define RelayGroenLicht 27
#define AANRELAY 25
#define UITRELAY 23

//Input pins sensoren
#define programeurPin2 24
#define barcodescannerPin 26
#define programeurPin 28

//Input pins UR10
#define UR10InputPin1 30
#define UR10InputPin2 32
#define UR10InputPin3 34
#define UR10InputPin4 36

//Input pins UR3
#define UR3InputPin1 38
#define UR3InputPin2 40
#define UR3InputPin3 42
#define UR3InputPin4 44

//Pin voor noodstop
#define noodpin 52

int UR10Divers;
int UR3Divers;

//Bools for communicatie met RPI
bool sentBarcode = false;
bool sentProgrameer = false;
bool sentReady = false;
bool waitingForCopy = false;
bool afkeurDiver = false;

void setup() {
  Serial.begin(9600);

  // Pin-modes instellen

  pinMode(RelayProgrammeer, OUTPUT);
  pinMode(RelayInit, OUTPUT);
  pinMode(RelayStart, OUTPUT);
  pinMode(RelayHervat, OUTPUT);
  pinMode(RelayPauze, OUTPUT);
  pinMode(RelayBarcode, OUTPUT);
  pinMode(RelayTD, OUTPUT);
  pinMode(RelayCTD, OUTPUT);
  pinMode(Relay9, OUTPUT);
  pinMode(Relay10, OUTPUT);
  pinMode(Relay_NOOD, OUTPUT);
  pinMode(RelayRoodLicht, OUTPUT);
  pinMode(RelayGeelLicht, OUTPUT);
  pinMode(RelayGroenLicht, OUTPUT);
  pinMode(AANRELAY, OUTPUT);
  pinMode(UITRELAY, OUTPUT);

  pinMode(noodpin, INPUT_PULLUP);
  pinMode(programeurPin2, INPUT_PULLUP);
  pinMode(programeurPin, INPUT_PULLUP);
  pinMode(barcodescannerPin, INPUT_PULLUP);

  pinMode(UR10InputPin1, INPUT_PULLUP);
  pinMode(UR10InputPin2, INPUT_PULLUP);
  pinMode(UR10InputPin3, INPUT_PULLUP);
  pinMode(UR10InputPin4, INPUT_PULLUP);

  pinMode(UR3InputPin1, INPUT_PULLUP);
  pinMode(UR3InputPin2, INPUT_PULLUP);
  pinMode(UR3InputPin3, INPUT_PULLUP);
  pinMode(UR3InputPin4, INPUT_PULLUP);
  // Beginstatus instellen
  digitalWrite(UITRELAY, HIGH);
  digitalWrite(RelayProgrammeer, HIGH);
  digitalWrite(RelayInit, HIGH);
  digitalWrite(RelayStart, HIGH);
  digitalWrite(RelayHervat, HIGH);
  digitalWrite(RelayBarcode, HIGH);
  digitalWrite(RelayTD, HIGH);
  digitalWrite(RelayCTD, HIGH);
  digitalWrite(Relay9, HIGH);
  digitalWrite(Relay10, HIGH);
  digitalWrite(RelayRoodLicht, HIGH);
  digitalWrite(RelayGeelLicht, HIGH);
  digitalWrite(RelayGroenLicht, HIGH);
  digitalWrite(RelayPauze, HIGH);
  digitalWrite(AANRELAY, HIGH);
  attachInterrupt(digitalPinToInterrupt(noodpin), INTER, CHANGE);
}

void loop() {
  // Controleer of "Copy" is ontvangen
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // Verwijder overbodige spaties of newline-karakters

    if (input == "Copy") {
      waitingForCopy = false; // Stop met verzenden
      sentBarcode = false;
      sentProgrameer = false;
      sentReady = false;
      delay(500);
    }
    if (input == "Diver"){
      digitalWrite(RelayCTD, HIGH);
       digitalWrite(RelayTD, LOW);
    }
    if (input == "CTD-Diver"){
      digitalWrite(RelayTD, HIGH);
      digitalWrite(RelayCTD, LOW);
    }
    if (input == "DekTech"){
      digitalWrite(RelayTD, LOW);
      digitalWrite(RelayCTD, LOW);
    }
    if (input == "Aan"){
        //Om de cobots aan te zetten
      digitalWrite(AANRELAY, LOW);
      delay(400);
      digitalWrite(AANRELAY, HIGH);

    }
    
    if (input == "Afkeur"){
      //digitalWrite(RelayAfkeur, LOW);
      afkeurDiver = true;
    }
    if (input == "Ready"){
      digitalWrite(RelayGroenLicht, LOW);
      digitalWrite(RelayInit, LOW);
      delay(500);
      digitalWrite(RelayGroenLicht, HIGH);
      digitalWrite(RelayInit, HIGH);
    }
    if (input == "Start"){
      digitalWrite(RelayStart, LOW);
      digitalWrite(RelayGroenLicht, LOW);
    }
    if (input == "Pauze"){
      digitalWrite(RelayPauze, LOW);
      digitalWrite(RelayHervat, HIGH);
    }
    if (input == "Hervat"){
      digitalWrite(RelayPauze, HIGH);
      digitalWrite(RelayHervat, LOW);
    }
    if (input == "BarcodeOK"){
      digitalWrite(RelayBarcode, HIGH);
      
    }
  }


  if (digitalRead(UR10InputPin3) == LOW && afkeurDiver == true){
    //digitalWrite(RelayAfkeur, HIGH);
    afkeurDiver = false;
  }
  /*
  // Barcode verzenden totdat "Copy" is ontvangen
  if (digitalRead(barcodescannerPin) == LOW && !sentBarcode && !waitingForCopy) {
    digitalWrite(RelayBarcode, LOW);
    Serial.println("Barcode");
    sentBarcode = true;
    waitingForCopy = true;
    delay(500); // Vertraging om te voorkomen dat het te vaak verzendt
  }

if (digitalRead(programeurPin2) == LOW){
  digitalWrite(RelayRoodLicht, HIGH);
  delay(200);
  digitalWrite(RelayGeelLicht, LOW);
  delay(200);
}
if (digitalRead(programeurPin2) == HIGH){
  digitalWrite(RelayGeelLicht, HIGH);
  delay(200);
  digitalWrite(RelayRoodLicht, LOW);
  delay(200);
}*//*
  // Programeer verzenden totdat "Copy" is ontvangen
  if ((digitalRead(programeurPin) == LOW || digitalRead(programeurPin2) == HIGH)){// && !sentProgrameer && /*digitalRead(UR3InputPin1) == LOW && !waitingForCopy) {
    Serial.println("Programeer");
    digitalWrite(RelayProgrammeer, LOW);
    sentProgrameer = true;
    waitingForCopy = true;
   // delay(500);
  }*/
  if (digitalRead(programeurPin) == LOW || digitalRead(programeurPin2) == LOW){
    digitalWrite(RelayProgrammeer, LOW);
  }
  // Herstel de relais als programeurPin wordt losgelaten
  if (digitalRead(programeurPin) == HIGH) {
    digitalWrite(RelayProgrammeer, HIGH);
    sentProgrameer = false;
  }
/*
  if (digitalRead(UR10InputPin4) == LOW && digitalRead(UR3InputPin4) == LOW &&!sentReady &&!waitingForCopy) {
    Serial.println("CobotReady");
    digitalWrite(RelayInit, LOW);
    sentReady = true;
    waitingForCopy = true;
    
  }/*
  if (digitalRead(UR10InputPin2) == LOW &&!waitingForCopy){
    Serial.print("UR10Divers");
    waitingForCopy = true;
  }
  if (digitalRead(UR3InputPin2) == LOW &&!waitingForCopy){
    Serial.print("UR3Divers");
    waitingForCopy = true;
  }*/
}
// Interrupt Service Routine
void INTER() {
  // Handeling voor noodstop
  if (digitalRead(noodpin) == LOW) {
    digitalWrite(Relay_NOOD, HIGH);
    digitalWrite(RelayRoodLicht, HIGH);
  } else {
    digitalWrite(Relay_NOOD, LOW);
    digitalWrite(RelayRoodLicht, LOW);
  }
}
