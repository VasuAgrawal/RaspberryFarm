import pexpect
from pexpect import fdpexpect
import os

def login(port, user="pi", password="raspberry", baudrate=115200):
    timeout = 5

    # child = pexpect.spawn("screen %s %d" % (port, baudrate))
    child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NONBLOCK |
        os.O_NOCTTY))

    # Needed to start the whole buffering thing, and to be able to see output on
    # the screen
    child.sendline("")

    # We see if we got the bash prompt instead of the login prompt. If we get
    # the bash prompt, we're already logged in.
    try:
        child.expect("%s@raspberrypi" % user, timeout=timeout)
        print "Already logged in, returning!"
        return child
    except:
        pass

    # try to log in 3 times
    for i in range(3):
        try:
            child.expect("raspberrypi login:", timeout=timeout)
            child.sendline(user)
            child.expect("Password:", timeout=timeout)
            child.sendline(password)
            return child
        except:
            print "Failed to log in, trying again ..."
            continue

    raise Exception("Something is probably wrong with the raspberry pi?")

if __name__ == "__main__":
    for i in range(1, 4, 2):
        print "Logging into /dev/ttyUSB%d" % i
        login("/dev/ttyUSB%d" % i).close()
