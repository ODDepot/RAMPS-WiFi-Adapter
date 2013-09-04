The RAMPS WiFi Adapter provides wireless networking for RepRap's RAMPS (Arduino Mega Pololu Shield) controller.

### News

#### 9/4/2013
Version 0.2 has been tested and is functional. Further work on setup.ino and setup.py is needed for a friendly configuration process. Higher baudrates may be achieved but have not been fully tested.

#### 6/19/2013
Version 0.2 is ready to be ordered and tested. The LM358DMR2G is replacing the TLV2452CDGKR and voltage dividers are being added along with a pullup and pulldown resistor. The first version has some errors. Overdriving the TLV2452CDGKR inputs at 5V with 3.3V supply is not possible. Replacing it with a LM358DMR2G works, however, a pullup resistor for RESET and a pulldown resistor for GPIO9 on the RN-171 is needed whenever jumpers are not connected. Besides these issues, Version 0.1 is able to connect and send data. The antenna appears very capable.

#### 5/13/2013
Boards for the first version have been ordered and testing will begin soon.

### Setup

#### Using Marlin firmware and Pronterface host software
Make sure the RAMPS WiFi Adapter is installed correctly on RAMPS and the Reset and Default pin jumpers are in place. Upload setup.ino to the Arduino Mega with your custom settings. Observe output from the RN171 (WiFi module onboard the adapter) with the Arduino IDE Serial Monitor. If the RN171 successful assoicates with your wireless network, the RN171 should provide an IP Address and the only LED blinking should be green. Verify this by checking your router. Also, you may want to configure your router for Static DHCP so that it always leases the same IP Address for the same MAC Address (on the RN171).

In Configuration.h of Marlin, change '#define SERIAL_PORT 0' to '#define SERIAL_PORT 2' and change '#define BAUDRATE 250000' to '#define BAUDRATE 9600', then upload. Remove the Reset and Default pin jumpers and reset RAMPS. Wait a few seconds. In Pronterface, type [IP Address]:2000 into the 'Port' bar (for example, 192.168.1.100:2000), then connect.
