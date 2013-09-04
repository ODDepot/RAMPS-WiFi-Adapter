// This sketch restores the RN171 on the RAMPS WiFi Adapter to factory defaults. Try this if the
// RN171 becomes unresponsive, then use debug.ino. Make sure the Reset and Default pin jumpers
// are in place! See the RN171-EK datasheet for "factory reset" sequence
// (http://www.rovingnetworks.com/resources/download/147/RN_171_EK_Data_Sheet).


int RST = 23;
int DFLT = 25;


void setup() {
  pinMode(RST, OUTPUT);
  pinMode(DFLT, OUTPUT);

  // The following write sequence restores the RN171 to factory defaults
  // Make sure the Reset and Default pin jumpers are in place!
  digitalWrite(DFLT, HIGH);
  delay(1000);
  digitalWrite(RST, LOW);
  delay(1000);
  digitalWrite(RST, HIGH);
  delay(1000);
  digitalWrite(DFLT, LOW);
  delay(1000);
  digitalWrite(DFLT, HIGH);
  delay(1000);
  digitalWrite(DFLT, LOW);
  delay(1000);
  digitalWrite(DFLT, HIGH);
  delay(1000);
  digitalWrite(DFLT, LOW);
  delay(1000);
  digitalWrite(DFLT, HIGH);
  delay(1000);
  digitalWrite(DFLT, LOW);
  delay(1000);
  digitalWrite(DFLT, HIGH);
  delay(1000);
  digitalWrite(DFLT, LOW);
  delay(1000);
  digitalWrite(DFLT, HIGH);
  delay(1000);
  digitalWrite(DFLT, LOW);
}

void loop() {
}
