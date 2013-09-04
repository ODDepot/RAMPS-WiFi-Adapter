#!/usr/bin/env python

# This script is a simple non-blocking interface for serial communications with the RN171.
# Upload debug.ino before using!


import argparse
import serial
import threading
import time


class CustomHelpFormatter(argparse.HelpFormatter):
    # Is this really the only way to set these values???  Dumb if it is...
    def __init__(self, prog):
        argparse.HelpFormatter.__init__(self, prog, max_help_position=60, width=120)


parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
parser.add_argument("-d", "--device", help="set device location, e.g. \"/dev/ttyACM0\"")
parser.add_argument("-b", "--baudrate", help="set baudrate, e.g. \"9600\"")
parser.add_argument("-f", "--flush", choices=["input", "output", "both"], help="flush (input, output, both) buffer(s) upon startup")
args = parser.parse_args()


class DaemonThread(threading.Thread):
    def  __init__(self, conn):
        threading.Thread.__init__(self)
        self.daemon = True  # Must be set true so thread will exit when main exits
        self.conn = conn

    def run(self):
        while True:
            if self.conn.inWaiting():
                time.sleep(1)
                print "<RECV>" + self.conn.read(1024) + "</RECV>"
                #print "RECV:" + self.conn.read(self.conn.inWaiting())
                print


if not args.device:
    args.device = "/dev/ttyACM0"
if not args.baudrate:
    args.baudrate = "9600"

conn = serial.Serial(args.device, args.baudrate, timeout=0)

if args.flush == "input":
    conn.flushInput()
elif args.flush == "output":
    conn.flushOutput()
elif args.flush == "both":
    conn.flush()

listener = DaemonThread(conn=conn)  # Create a non-blocking thread to listen on the serial port
listener.start()

print "A simple non-blocking interface for serial communications."
print "Connected..."
print "Device: %s" % args.device
print "Baudrate: %s" % args.baudrate
print "Enter 'q' to quit."
print
while True:
    data = raw_input()
    if data == "q":
        break
    else:
        print "<SENT>" + data + '\n' + "</SENT>"
        #print "SENT:" + data + '\n'
        print
        conn.write(data + '\r\n')
