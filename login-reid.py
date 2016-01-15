import pexpect
from pexpect import fdpexpect
import fuckit
import os
import serial

def login(port, user="pi", password="raspberry", baudrate=115200):
    timeout = 5

    # child = pexpect.spawn("screen %s %d" % (port, baudrate))
    #child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NOCTTY))
    
    ser = serial.Serial(port, 115200)
    child = fdpexpect.fdspawn(ser)


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
            child.expect([pexpect.EOF, "raspberrypi login:"], timeout=timeout)
            child.sendline(user)
            child.expect([pexpect.EOF, "Password:"], timeout=timeout)
            child.sendline(password)
            return child
        except Exception as e:
            print e
            print "Failed to log in, trying again ..."
            continue

    raise Exception("Something is probably wrong with the raspberry pi?")

ports = ["/dev/tty.usbserial-FTXRNUKVB"]

if __name__ == "__main__":
    #for i in range(1, 4, 2):
    #   print "Logging into /dev/ttyUSB%d" % i
    #   login("/dev/ttyUSB%d" % i).close()
    for port in ports:
        print "Logging into " + port
        login(port)