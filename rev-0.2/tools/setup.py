#!/usr/bin/env python


import argparse
import serial
import sys
import threading
import time


def escape_spaces(data):
    return "$".join(data.split(" "))


def send(command):
    if command.split(" ")[0] == "set":
        conn.write(command + "\r\n")
        time.sleep(3)
        response = conn.read(1024)
        if response != command + '\r\r\nAOK\r\n<4.00> \n':
            print "ERROR: %s" % response
            sys.exit(1)
    else:
        conn.write(command + "\r\n")
        time.sleep(3)
        response = conn.read(1024)
    return response


class CustomHelpFormatter(argparse.HelpFormatter):
    # Is this really the only way to set these values???  Dumb if it is...
    def __init__(self, prog):
        argparse.HelpFormatter.__init__(self, prog, max_help_position=60, width=120)


parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
parser.add_argument("-d", "--device", help="set device location, e.g. \"/dev/ttyUSB0\"")
parser.add_argument("-b", "--baudrate", help="set baudrate, e.g. \"115200\"")
parser.add_argument("-f", "--flush", choices=["input", "output", "both"], help="flush (input, output, both) buffer(s) upon startup")
args = parser.parse_args()


if not args.device:
    args.device = "/dev/ttyACM0"
if not args.baudrate:
    args.baudrate = '9600'

print "Starting..."

conn = serial.Serial(args.device, args.baudrate, timeout=0)
conn.write("$$$")
time.sleep(3)
response = conn.read(1024)
if response == "CMD\r\n":
    #print "Entering command mode\n"
    pass
elif response == "$$$":
    #print "Already in command mode\n"
    pass
else:
    print "Could not enter command mode\n"
    sys.exit(1)

# A "hiccup" always returns an error for the first commmand after "$$$", so send this and ignore response
send("")

# Scan for local Access Points and parse response
print "Scanning for local Access Points..."
response = send("scan")
access_points = response.split("\r\n")[3:len(response.split("\r\n"))-2]  # Parse scan response and display
if access_points < 1:
    print "No Access Point found"
print
print "Select Access Point:"
for access_point in access_points:
    print access_point

# Get user input
access_point_id = 0
while access_point_id not in range(1, len(access_points) + 1):
    access_point_id = int(input("Choose %s: " % str(range(1, len(access_points) + 1))))
ssid = access_points[access_point_id - 1].split(",").pop()

print
print "Select the WiFi Authentication Mode:\n0 Open\n1 WEP-128\n2 WPA1\n3 Mixed WPA1 and WPA2-PSK\n4 WPA2-PSK"
auth = -1
while auth not in ['0', '1', '2', '3', '4']:
    auth = raw_input("Choose [0, 1, 2, 3, 4, 5]: ")

print
passphrase = raw_input("Enter key/pass phrase: ")

# Configure
print
print "Configuring..."
send("set wlan linkmon 0")  # WiFly de-authenticates and re-authenticates continously with the AP when this is >0, not sure why...
send("set wlan ssid %s" % escape_spaces(ssid))
if auth in ['1']:
    send("set wlan key %s" % escape_spaces(passphrase))
if auth in ['2', '3', '4']:
    send("set wlan phrase %s" % escape_spaces(passphrase))

print "Finished"
