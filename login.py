import pexpect

child = pexpect.spawn("screen /dev/ttyUSB1 115200")
child.sendline("pi")
child.sendline("raspberry")
child.interact()
