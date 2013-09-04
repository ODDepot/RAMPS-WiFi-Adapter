#!/usr/bin/env python

# This script is an alternative to setup.ino for configuration of the RN171.
# Upload debug.ino before using!


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

def get_access_points(max_attempts=5):
    # Scan for local Access Points and parse response
    attempts = 0
    access_points = []
    print "Scanning for local Access Points (this may take a few minutes)..."
    time.sleep(10)  # Wait a bit for the module to intialize
    while True:
        if attempts > max_attempts:
            print "No Access Point found, is your router broadcasting?"
            sys.exit(1)
        response = send("scan")
        access_points = response.split("\r\n")[3:len(response.split("\r\n"))-2]  # Parse scan response and display
        if len(access_points) >= 1:
            break
        else:
            attempts += 1
            time.sleep(3)
    return access_points

def get_address(max_attempts=5):
    attempts = 0
    ip_address = "0.0.0.0"
    port = "2000"
    print "Getting IP Address (this may take a minute or two)..."
    time.sleep(30)
    while True:
        if attempts > max_attempts:
            print "Could not find an IP Address, check settings with comm.py..."
            sys.exit(1)
        response = send("get ip")
        ip_address, port = response.split("\n")[3].split("=")[1].rstrip().split(":")
        if ip_address != "0.0.0.0":
            break
        else:
            attempts += 1
            time.sleep(3)
    return (ip_address, port)

def enter_command_mode():
    time.sleep(5)
    conn.read(1024)  # Flush
    conn.write("$$$")
    time.sleep(5)
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


class CustomHelpFormatter(argparse.HelpFormatter):
    # Is this really the only way to set these values???  Dumb if it is...
    def __init__(self, prog):
        argparse.HelpFormatter.__init__(self, prog, max_help_position=60, width=120)


parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
parser.add_argument("-d", "--device", help="set device location, e.g. \"/dev/ttyACM0\"")
parser.add_argument("-b", "--baudrate", help="set baudrate, e.g. \"9600\"")
parser.add_argument("-f", "--flush", choices=["input", "output", "both"], help="flush (input, output, both) buffer(s) upon startup")
args = parser.parse_args()


if not args.device:
    args.device = "/dev/ttyACM0"
if not args.baudrate:
    args.baudrate = '9600'

print "Starting..."
conn = serial.Serial(args.device, args.baudrate, timeout=0)
enter_command_mode()

# A "hiccup" sometimes returns an error for the first commmand after "$$$", so send this and ignore response
send("")

access_points = get_access_points()
for access_point in access_points:
    print access_point

# Get user input
access_point_id = 0
while access_point_id not in range(1, len(access_points) + 1):
    access_point_id = int(input("Choose %s: " % str(range(1, len(access_points) + 1))))
ssid = access_points[access_point_id - 1].split(",").pop()

print
print "Select the WiFi Authentication Mode:\n0 Open\n1 WEP\n2 WPA2\n3 WPA1\n4 MIXED\n5 ADHOC\n6 PEAP\n7 NONE\n8 WEP64"
auth = -1
while auth not in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
    auth = raw_input("Choose [0, 1, 2, 3, 4, 5, 6, 7, 8]: ")

print
passphrase = raw_input("Enter key/pass phrase: ")

# Configure
print
print "Configuring..."
send("set option device_id %s" % escape_spaces("RAMPS WiFi Adapter"))
send("set wlan ssid %s" % escape_spaces(ssid))
send("set wlan auth %s" % auth)
if auth in ['1']:
    send("set wlan key %s" % escape_spaces(passphrase))
else:
    send("set wlan phrase %s" % escape_spaces(passphrase))
send("set wlan linkmon 0")  # WiFly de-authenticates and re-authenticates continously with the AP when this is >0, not sure why...
send("set wlan join 1")
send("set ip dhcp 1")
#send("run web_app")

print "Saving..."
send("save")

print "Rebooting..."
send("reboot")
time.sleep(30)
enter_command_mode()

ip_address, port_number = get_address()
print "You should now be able to connect to: %s:%s" % (ip_address, port_number)
print "In Pronterface, copy and paste '%s:%s' into the Port bar" % (ip_address, port_number)

print "Finished!"
