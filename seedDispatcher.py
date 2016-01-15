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
    children = map(login.login, raspis)
    print children
    print "Logged in to all the rapis"

    # Then, we generate a fresh set of seeds for the rapis to each crack
    seedGen.gen(len(raspis), bytes=80, number=2)

    # Then, we need to send it to all of the rapis
    for i, port in enumerate(children):
        outfile.send("output%d.hashes" % i, port)
        # outfile.send("seedParser.py", port)

    return children

def analyze(port, filename):
    print "Analyzing port %s" % port
        #child = fdpexpect.fdspawn(os.open(port, os.O_RDWR | os.O_NONBLOCK | os.O_NOCTTY))

    child = port
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
                q.put((port, child.before.rstrip()))
            else:
                first = False

            if (out == 0):
                break
    except:
        # send CTRL + C if we get an error
        child.sendline("\x03")

    child.close()

q = Queue.Queue()
root = Tk()
canvas = Canvas(root, width=500, height=500)
canvas.pack()

left=20
right=20

def update():
    try:
        port, data = q.get_nowait()
        parts = data.split()

        # TODO: Find a better way of matching to generic number of raspis
        print "Port:", port
        if port == raspis[0]:
            print "first?"
            canvas.create_text((50, left), text=parts[-2])
            left += 20
        elif port == raspis[1]:
            print "second?"
            canvas.create_text((200, right), text=parts[-2])
            right += 20
    except:
        pass
    root.after(100, update)

#raspis = ["/dev/ttyUSB1", "/dev/ttyUSB3"]
raspis = ["/dev/tty.usbserial-FTXR2FSNB", "/dev/tty.usbserial-FTXRNUKVB"]

def main():

    children = prepare(raspis)

    threads = [Thread(target=analyze, args=(raspi[1], "output%d.hashes" %
               raspi[0])) for raspi in enumerate(children)]

    map(Thread.start, threads)

    root.after(100, update)
    root.mainloop()
    # map(Thread.join, threads)

if __name__ == "__main__":
    main()

