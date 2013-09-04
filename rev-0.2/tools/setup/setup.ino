// This sketch configures the RN171 on the RAMPS WiFi Adapter. If successfully configured, the
// RN171 will associate with your AP (wireless router). Use the Arduino Serial Monitor to observe
// output (and the IP address to connect to). Modify the following settings for your router.
// Make sure the Reset and Default pin jumpers are in place!

//////////////////////////////////////////////////
// Modify these settings to connect to your router
// Make sure they are exact! Double check!
//////////////////////////////////////////////////

// Type your router name here
String SSID = "My_SSID";

// Type your passphrase here
String Passphrase = "My_Passphrase";

// Uncomment ONE of the following security types...
//int Auth_Type = 0; // Open
int Auth_Type = 2; // WPA2
//int Auth_Type = 3; // WPA1
//int Auth_Type = 4; // Mixed

//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////


String device_id = "RAMPS WiFi Adapter 9";  // If using more than one adapter, each device_id should be unique

int RST = 23;
int DFLT = 25;

const int command_buffer_size = 64;
char command[command_buffer_size];


void establish_comm() {
  Serial.begin(9600);
  Serial2.begin(9600);
}

void send_command(String str_command) {
  str_command.toCharArray(command, command_buffer_size);
  Serial2.write(command);
}

void print_response() {
  delay(1000);
  while (Serial2.available() > 0) {
    Serial.write(Serial2.read());
  }
  Serial.write("\r\n");
}

void clear_receive_buffer() {
  delay(1000);
  while (Serial2.available() > 0) {
    Serial2.read();
  }
}

String escape_space(String string) {

  string.replace(" ", "$");
  return string;
}

void setup() {
  pinMode(RST, OUTPUT);
  pinMode(DFLT, OUTPUT);

  // The following write sequence restores the RN171 to factory defaults
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
  delay(1000);

  // Reset the RN171
  digitalWrite(RST, LOW);
  delay(1000);
  digitalWrite(RST, HIGH);
  delay(1000);

  establish_comm();

  send_command("$$$");
  print_response();

  send_command("\r\n");  // A "hiccup" sometimes returns an error for the first commmand after "$$$", so send this and ignore response
  clear_receive_buffer();

  send_command(String(("set option device_id ") + escape_space(device_id) + "\r\n"));
  print_response();
  
  send_command((String("set wlan ssid ") + escape_space(SSID) + "\r\n"));
  print_response();

  send_command((String("set wlan auth ") + Auth_Type + "\r\n"));
  print_response();

  send_command((String("set wlan phrase ") + escape_space(Passphrase) + "\r\n"));
  print_response();

  send_command("set wlan linkmon 0\r\n");  // WiFly de-authenticates and re-authenticates continously with the AP when this is > 0, not sure why...
  print_response();
  
  send_command("set wlan join 1\r\n");
  print_response();
  
  send_command("set ip dhcp 1\r\n");
  print_response();

  send_command("save\r\n");
  print_response();
  
  // Reset the RN171 again
  digitalWrite(RST, LOW);
  delay(1000);
  digitalWrite(RST, HIGH);
  delay(1000);
}

void loop() {
  delay(1000);
  send_command("$$$");
  clear_receive_buffer();

  delay(1000);
  send_command("\r\n");  // A "hiccup" sometimes returns an error for the first commmand after "$$$", so send this and ignore response
  clear_receive_buffer();

  delay(10000);
  send_command("get ip a\r\n");
  print_response();
}
