import pexpect
from pexpect import fdpexpect
import fuckit
import os
import serial
import time

def login(port, user="pi", password="raspberry", baudrate=115200):
    timeout = 5

    # child = pexpect.spawn("screen %s %d" % (port, baudrate))
    #child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NONBLOCK | os.O_NOCTTY))
    
    ser = serial.Serial(port, 115200)
    #ser.reset_input_buffer()
    #ser.reset_output_buffer()
    child = fdpexpect.fdspawn(ser.fileno())

    # Needed to start the whole buffering thing, and to be able to see output on
    # the screen
    child.sendline("")

    # We see if we got the bash prompt instead of the login prompt. If we get
    # the bash prompt, we're already logged in.
    with fuckit:
        child.expect("%s@raspberrypi" % user, timeout=timeout)
        print "Already logged in, returning!"
        return child
    
    

    # try to log in 3 times
    for i in range(3):
        try:
            ser.flushInput()
            ser.flushOutput()
            ser.write("\n")
            ser.flush()
            time.sleep(1)
            print ser.inWaiting()
            ser.write("pi\n");
            ser.flush();
            time.sleep(1);
            ser.write("raspberry\n");
            ser.flush();
            time.sleep(1);
            return child
        except:
            print "Failed to log in, trying again ..."
            continue

    raise Exception("Something is probably wrong with the raspberry pi?")

if __name__ == "__main__":
    print "Logging into ..."
    login("/dev/tty.usbserial-FTXRNUKVB")
    for i in range(1, 4, 2):
        print "Logging into /dev/ttyUSB%d" % i
    #   login("/dev/ttyUSB%d" % i).close()
