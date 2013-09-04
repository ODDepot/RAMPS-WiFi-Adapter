// This sketch resets the RN171 on the RAMPS WiFi Adapter, enters command mode and relays serial
// communications between your host and the RN171. Use this with setup.py for guided configuration
// or comm.py for manual configuration and debugging. Make sure the Reset pin jumper is in place!
// See WiFly datasheet for command reference 
// (http://www.rovingnetworks.com/resources/download/93/WiFly_User_Manual).


int RST = 23;


void setup() {
  pinMode(RST, OUTPUT);

  // Reset the RN171
  // Make sure the Reset pin jumper is in place!
  digitalWrite(RST, LOW);
  delay(1000);
  digitalWrite(RST, HIGH);
  delay(1000);

  Serial.begin(9600);
  Serial2.begin(9600);

  Serial2.write("$$$");
  delay(500);  // Give the module time to enter command mode
}

void loop() {
  while (Serial.available() > 0) {
    Serial2.write(Serial.read());
  }
  while (Serial2.available() > 0) {
    Serial.write(Serial2.read());
  }
}
