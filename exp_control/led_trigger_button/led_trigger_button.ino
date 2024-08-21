const int ledPin = 8;       // Pin for the LED
const int buttonPin = 13;   // Pin for the button

void setup() {
  pinMode(ledPin, OUTPUT);  // Set the LED pin as output
  pinMode(buttonPin, INPUT_PULLUP);  // Set the button pin as input with internal pull-up resistor
}

void loop() {
  int buttonState = digitalRead(buttonPin);  // Read the state of the button

  // Invert the logic to match the desired behavior
  if (buttonState == HIGH) {  // Button is not pressed (HIGH due to pull-up resistor)
    digitalWrite(ledPin, HIGH);  // Turn the LED off (TTL signal LOW)
  } else {  // Button is pressed (LOW)
    digitalWrite(ledPin, LOW);  // Turn the LED on (TTL signal HIGH)
  }
}
