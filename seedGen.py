import os
import argparse
import binascii

def gen(files=5, bytes=100, number=10):
    for i in range(files):

        first = True
        with open("output%d.hashes" % i, "w") as out:
            for i in range(number):
                if not first:
                    out.write("\n")
                else:
                    first=False
                out.write(binascii.hexlify(os.urandom(bytes)))


def main():
    parser = argparse.ArgumentParser("""\
Spit out n files with x random bytes
""")

    parser.add_argument("-n", "--files", default=5, type=int)
    parser.add_argument("-x", "--bytes", default=100, type=int)
    parser.add_argument("-o", "--number", default=10, type=int)
    args = parser.parse_args()

    gen(args.files, args.bytes, args.number)


if __name__ == "__main__":
    main()
