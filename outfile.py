# Take in a file and spit it out to a serial port

import sys
import argparse
import os
from pexpect import fdpexpect

def main():

    parser = argparse.ArgumentParser("""\
Write a file taken in over std to the file specified via command line
""")

    parser.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    child = fdpexpect.fdspawn(os.open("/dev/ttyUSB1", os.O_RDWR | os.O_NONBLOCK
        | os.O_NOCTTY))

    # child.sendline("python ~/Documents/RaspberryFarm/writeFile.py -o ~/Documents/RaspberryFarm/testish -s 1262")
    # child.expect("Ready", timeout=None)

    val = open(args.input, "r").read()
    for line in val.splitlines():
        child.sendline(line)

    child.close()

main()
