#define knop1 53
#define knop2 51
#define knop3 31
#define knop4 8
#define knop5 29

#define relay 40
#define relay1 38
#define relay2 53

#define noodstop 2

String input = "";
String currentProduct = "";
String currentSerial = "";
bool isBooted = false;
volatile bool noodGeactiveerd = false;

const unsigned long debounceDelay = 50;
const unsigned long debounceDelay2 = 500;
unsigned long lastDebounceTime_knop1 = 0;
unsigned long lastDebounceTime_knop2 = 0;
unsigned long lastDebounceTime_knop3 = 0;
unsigned long lastDebounceTime_knop4 = 0;
unsigned long lastDebounceTime_knop5 = 0;
unsigned long lastDebounceTime_nood = 0;

bool lastButtonState_knop1 = HIGH;
bool lastButtonState_knop2 = HIGH;
bool lastButtonState_knop3 = HIGH;
bool lastButtonState_knop4 = HIGH;
bool lastButtonState_knop5 = HIGH;


bool lastButtonState_nood = HIGH;
bool buttonState_knop1 = HIGH;
bool buttonState_knop2 = HIGH;
bool buttonState_knop3 = HIGH;
bool buttonState_knop4 = HIGH;
bool buttonState_knop5 = HIGH;

void setup() {
  pinMode(knop1, INPUT_PULLUP);
  pinMode(knop2, INPUT_PULLUP);
  pinMode(knop3, INPUT_PULLUP);
  pinMode(knop4, INPUT_PULLUP);
  pinMode(knop5, INPUT_PULLUP);

  pinMode(relay, OUTPUT);
  pinMode(relay1, OUTPUT);
  pinMode(relay1, OUTPUT);


  pinMode(noodstop, INPUT);
  attachInterrupt(digitalPinToInterrupt(noodstop), nood, FALLING);
//  digitalWrite(relay, HIGH); // Relay off by default
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}


void nood(){
    unsigned long huidigetijd = millis();


  if ((huidigetijd - lastDebounceTime_nood) > debounceDelay2) {
    lastDebounceTime_nood = huidigetijd;
   noodGeactiveerd = true;
}
}
void loop() {

  if (noodGeactiveerd){
    Serial.println("nood stop ingedrukt");
     noodGeactiveerd = false;
  }
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();
  }

  // Boot handshake
  if (!isBooted) {
    if (input == "Python_Booted") {
      Serial.println("ARDUINO_BOOTED");
      isBooted = true;
      input = "";
    }
    return;
  }

  if (input.length() > 0) {

    if (input == "on"){
      digitalWrite(relay, HIGH);
      digitalWrite(relay1,HIGH);
      digitalWrite(relay2,HIGH);

      Serial.println("Relay aan");
      input = "";
    }

    if (input == "off"){
      digitalWrite(relay, LOW);
      digitalWrite(relay1, LOW);
      digitalWrite(relay2, LOW);
      Serial.println("Relay uit");
      input = "";
    }
    if (input.startsWith("PYTHON_SAYS:")) {
      String cmd = input.substring(12);
      if (cmd.startsWith("SERIAL:")) {
        currentSerial = cmd.substring(7);
        Serial.println("ARDUINO_SERIAL_ACK:" + currentSerial);
              input = "";
      } else if (cmd.startsWith("PRODUCT:")) {
        currentProduct = cmd.substring(8);
        Serial.println("ARDUINO_PRODUCT_ACK:" + currentProduct);
              input = "";
      }
      Serial.println("ARDUINO_ACK:" + cmd);
      Serial.println("ARDUINO_DONE");
    }
  }

  // === Knop 1 === (EDGE DETECTION)
  bool reading_knop1 = digitalRead(knop1);
  
  if (reading_knop1 != lastButtonState_knop1) {
    lastDebounceTime_knop1 = millis();
  }
  
  if ((millis() - lastDebounceTime_knop1) > debounceDelay) {
    if (reading_knop1 != buttonState_knop1) {
      buttonState_knop1 = reading_knop1;
      
      // Stuur bericht alleen bij falling edge (knop wordt ingedrukt)
      if (buttonState_knop1 == LOW) {
        Serial.println("ARDUINO_Persen:" + currentSerial);
      }
    }
  }
  
  lastButtonState_knop1 = reading_knop1;

  // === Knop 2 (LED) ===
  bool reading_knop2 = digitalRead(knop2);
  
  if (reading_knop2 != lastButtonState_knop2) {
    lastDebounceTime_knop2 = millis();
  }
  
  if ((millis() - lastDebounceTime_knop2) > debounceDelay) {
    if (reading_knop2 != buttonState_knop2) {
      buttonState_knop2 = reading_knop2;
      
      // Stuur bericht alleen bij falling edge (knop wordt ingedrukt)
      if (buttonState_knop2 == HIGH) {
        Serial.println("ARDUINO_Programmeren:" + currentSerial);
      }
    }
  }
  
  lastButtonState_knop2 = reading_knop2;

  // === Knop 3 === (EDGE DETECTION)
  bool reading_knop3 = digitalRead(knop3);
  
  if (reading_knop3 != lastButtonState_knop3) {
    lastDebounceTime_knop3 = millis();
  }
  
  if ((millis() - lastDebounceTime_knop3) > debounceDelay) {
    if (reading_knop3 != buttonState_knop3) {
      buttonState_knop3 = reading_knop3;
      
      // Stuur bericht alleen bij falling edge (knop wordt ingedrukt)
      if (buttonState_knop3 == LOW) {
        Serial.println("ARDUINO_Graveren:"+ currentSerial);
      }
    }
  }
  
  lastButtonState_knop3 = reading_knop3;


bool reading_knop4 = digitalRead(knop4);
  
  if (reading_knop4 != lastButtonState_knop4) {
    lastDebounceTime_knop4 = millis();
  }
  
  if ((millis() - lastDebounceTime_knop4) > debounceDelay) {
    if (reading_knop4 != buttonState_knop4) {
      buttonState_knop4 = reading_knop4;
      
      // Stuur bericht alleen bij falling edge (knop wordt ingedrukt)
      if (buttonState_knop4 == LOW) {
        Serial.println("ARDUINO_Controle:"+ currentSerial);
      }
    }
  }
    lastButtonState_knop4 = reading_knop4;
bool reading_knop5 = digitalRead(knop5);
  
  if (reading_knop5 != lastButtonState_knop5) {
    lastDebounceTime_knop5 = millis();
  }
  
  if ((millis() - lastDebounceTime_knop5) > debounceDelay) {
    if (reading_knop5 != buttonState_knop5) {
      buttonState_knop5 = reading_knop5;
      
      // Stuur bericht alleen bij falling edge (knop wordt ingedrukt)
      if (buttonState_knop5 == LOW) {
        Serial.println("ARDUINO_Verpakken:"+ currentSerial);
      }
    }
  }
  
  lastButtonState_knop5 = reading_knop5;
}