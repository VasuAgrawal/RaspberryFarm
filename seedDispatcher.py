import os
import login
import seedGen
import outfile
from threading import Thread
from pexpect import fdpexpect
from Tkinter import *
import Queue

def prepare(raspis):
    # First, we log in to all of the machines
    map(login.login, raspis)
    print "Logged in to all the rapis"

    # Then, we generate a fresh set of seeds for the rapis to each crack
    seedGen.gen(len(raspis), bytes=80, number=2)

    # Then, we need to send it to all of the rapis
    for i, port in enumerate(raspis):
        outfile.send("output%d.hashes" % i, port)
        # outfile.send("seedParser.py", port)

def analyze(port, filename):
    print "Analyzing port %s" % port
    child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NONBLOCK |
        os.O_NOCTTY))

    child.sendline("")
    child.expect("pi@raspberrypi")

    child.sendline("python ~/Documents/RaspberryFarm/seedParser.py -i %s" %
            filename)

    try:
        first = True
        while (True):
            out = child.expect(["Done searching!", "Output:"], timeout=120)

            # The first print will be crap, so we'll skip it
            if not first:
                print port, child.before.rstrip()
            else:
                first = False

            if (out == 0):
                break
    except:
        # send CTRL + C if we get an error
        child.sendline("\x03")

    child.close()

raspis = ["/dev/ttyUSB1", "/dev/ttyUSB3"]

def main():

    prepare(raspis)

    threads = [Thread(target=analyze, args=(raspi[1], "output%d.hashes" %
               raspi[0])) for raspi in enumerate(raspis)]

    map(Thread.start, threads)
    map(Thread.join, threads)

if __name__ == "__main__":
    main()

