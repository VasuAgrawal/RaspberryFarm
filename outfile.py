# Take in a file and spit it out to a serial port

import sys
import argparse
import os
from pexpect import fdpexpect
import serial
import time

def send(input, port):
    #child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NONBLOCK | os.O_NOCTTY))
    #ser = serial.Serial(port, 115200)
    #child = fdpexpect.fdspawn(ser.fileno())
    child = port
    print child.isalive()
    child.sendline("python ~/Documents/RaspberryFarm/writeFile.py -o %s -n %d" %
            (input, os.path.getsize(input)))
    child.expect("Ready", timeout = 10)
    #time.sleep(10)
    print "sending file %s to %s" % (input, port)

    val = open(input, "r").read()
    for line in val.splitlines():
        child.sendline(line)

    #child.close()



def main():

    parser = argparse.ArgumentParser("""\
Write a file taken in over std to the file specified via command line
""")

    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-p", "--port", required=True)
    args = parser.parse_args()

    send(args.input, args.port)

if __name__ == "__main__":
    main()
