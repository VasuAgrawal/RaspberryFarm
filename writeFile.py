import sys
import argparse

def main():

    parser = argparse.ArgumentParser("""\
Write a file taken in over std to the file specified via command line
""")

    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("-n", "--size", required=True, type=int)
    args = parser.parse_args()

    out = open(args.output, "w")

    # After the file is opened, we print a "ready" string
    print "Ready"

    out.write(sys.stdin.read(args.size))
    out.close()

if __name__ == "__main__":
    main()
