String input = "";
bool isBooted = false;

#define Knop1 53  // Persen
#define Knop2 47  // Programmeren
#define Knop3 41  // Graveren
#define Knop4 40  // Controle
#define Knop5 42  // Verpakken
#define relay1 23
#define relay2 25
String currentSerial = "";

bool lastButtonState1 = HIGH;
bool lastButtonState2 = HIGH;
bool lastButtonState3 = HIGH;
bool lastButtonState4 = HIGH;
bool lastButtonState5 = HIGH;

unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;
unsigned long lastDebounceTime4 = 0;
unsigned long lastDebounceTime5 = 0;

unsigned long debounceDelay = 50;

// 1 bool per knop voor debounce-detectie
bool gemeld1 = HIGH;
bool gemeld2 = HIGH;
bool gemeld3 = HIGH;
bool gemeld4 = HIGH;
bool gemeld5 = HIGH;

String currentProduct = "";

String getStepNameForPin(int pin) {
  if (currentProduct == "Diver") {
    if (pin == Knop1) return "Persen";
    if (pin == Knop2) return "Programmeren";
    if (pin == Knop3) return "Graveren";
    if (pin == Knop4) return "Controle";
    if (pin == Knop5) return "Verpakken";
  } else if (currentProduct == "CTD") {
    if (pin == Knop1) return "Graveren";
    if (pin == Knop2) return "Controle";
    if (pin == Knop3) return "Verpakken";
  }
}


void setup() {
  pinMode(Knop1, INPUT_PULLUP);
  pinMode(Knop2, INPUT_PULLUP);
  pinMode(Knop3, INPUT_PULLUP);
  pinMode(Knop4, INPUT_PULLUP);
  pinMode(Knop5, INPUT_PULLUP);

  pinMode(LED_BUILTIN, OUTPUT);
digitalWrite(relay1, HIGH);  // relay UIT
digitalWrite(relay2, HIGH);  // relay UIT
pinMode(relay1, OUTPUT);
pinMode(relay2, OUTPUT);
  Serial.begin(9600);
}

void checkButton(int pin, bool &lastState, unsigned long &lastTime, bool &gemeld) {
  bool currentState = digitalRead(pin);
  unsigned long currentMillis = millis();

  if (currentState != lastState) {
    lastTime = currentMillis;
  }

  if ((currentMillis - lastTime) > debounceDelay) {
    if (currentState != gemeld) {
      gemeld = currentState;

      if (currentState == HIGH) {
        String stap = getStepNameForPin(pin);
        Serial.println("ARDUINO_" + stap + "_OK:" + currentSerial);

        if (stap == "Persen") {
          digitalWrite(relay1, HIGH);
        }
      } else {
        if (getStepNameForPin(pin) == "Persen") {
          digitalWrite(relay1, LOW);
        }
      }
    }
  }

  lastState = currentState;
}


void loop() {
  // Lees seriële input
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();
  }

  // Boot handshake
  if (!isBooted) {
    // digitalWrite(relay1, LOW);
    if (input == "Python_Booted") {
      Serial.println("ARDUINO_BOOTED");
      isBooted = true;
      input = "";
    }
    return;
  }

checkButton(Knop1, lastButtonState1, lastDebounceTime1, gemeld1);
checkButton(Knop2, lastButtonState2, lastDebounceTime2, gemeld2);
checkButton(Knop3, lastButtonState3, lastDebounceTime3, gemeld3);
checkButton(Knop4, lastButtonState4, lastDebounceTime4, gemeld4);
checkButton(Knop5, lastButtonState5, lastDebounceTime5, gemeld5);

  // Verwerk seriële input
  if (input.length() > 0) {
    if (input.startsWith("PYTHON_SAYS:")) {
      String cmd = input.substring(12);

      if (cmd.startsWith("SERIAL:")) {
        currentSerial = cmd.substring(7);
        Serial.println("ARDUINO_SERIAL_ACK:" + currentSerial);
      }
      else if (cmd == "PYTHON_PROGRAMMING_DONE") {
        // evt. extra acties
      }
      else if (cmd.startsWith("PRODUCT:")) {
        currentProduct = cmd.substring(8);  // haal DIVER of CTD eruit
        Serial.println("ARDUINO_PRODUCT_ACK:" + currentProduct);
        if (currentProduct == "Diver"){
          digitalWrite(relay2, HIGH);
        }
}

      else if (cmd == "LED AAN") {
        digitalWrite(LED_BUILTIN, HIGH);
        Serial.println("AAN");
      }
      else if (cmd == "LED UIT") {
        digitalWrite(LED_BUILTIN, LOW);
        Serial.println("UIT");
      }

      Serial.println("ARDUINO_ACK:" + cmd);
      Serial.println("ARDUINO_DONE");
      input = "";
    }
  }
}
