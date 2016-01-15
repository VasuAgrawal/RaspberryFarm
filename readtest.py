import pexpect
from pexpect import fdpexpect
import os

from threading import Thread

def sleepTest(port):

    child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NONBLOCK |
        os.O_NOCTTY))

    child.sendline("")
    child.expect("pi@raspberrypi")

    child.sendline("python ~/Documents/outputGenerator.py")
    while (True):
        out = child.expect(["pi@raspberrypi", "Output:"])
        print port, child.before.rstrip()
        if (out == 0):
            break

    child.close()

for port in ["/dev/ttyUSB1", "/dev/ttyUSB3"]:
    Thread(target=sleepTest, args=(port,)).start()
