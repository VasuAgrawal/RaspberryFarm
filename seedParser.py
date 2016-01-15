import hashlib
import argparse
import binascii

def leadingZeros(string):
    count = 0
    while ord(string[0]) == 0:
        count += 1
        string = string[1:]
    return count

def crack(seed):

    start = 0
    while True:
        if leadingZeros(tryHash(seed, start)) >= 2:
            print "Output:", seed, start, binascii.hexlify(tryHash(seed, start))
            # return start
        elif start > 10**5:
            return -1
        start += 1

def tryHash(seed, num):
    toadd = "%x" % num
    if len(toadd) % 2 == 1:
        toadd = "0" + toadd
    seed = seed + toadd.decode("hex")
    return hashlib.sha256(hashlib.sha256(seed).digest()).digest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    with open(args.input, "r") as out:
        for line in out:
            num = crack(line[:-1])

    print "Done searching!"

main()
