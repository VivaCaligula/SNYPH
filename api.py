#!/usr/bin/python
# Snyph
import sys, random

up = True
alphabet = "abcdefghijklmnopqrstuvwxyz"
defaultheader = "010203040506070809101112131415161718192021222324252" \
                "627282930313233343536373839404142434445464748495051" \
                "525354555657585960"

if len(sys.argv) == 1:
    print "Snyph is a multidimensional cipher!\n" \
          "Use the -h flag to learn more or use this wizard:\n----"

    header = raw_input("Enter a header (empty for default 01-60): ")
    if not header:
        print "Assuming default header (01-60)."
        header = defaultheader
    elif len(header) < 120:
        sys.exit("Header is invalid. Exiting.")
    print "----"
    freq = raw_input("Enter a frequency variable 0-10 (empty for default 0): ")
    if freq:
        try:
            freq = int(freq)
            if freq not in range(11):
                raise
        except:
            sys.exit("Frequency variable is invalid. Exiting.")
    else:
        print "Assuming default frequency variable (0)."
        freq = 0

    print "----"
else:
    if "-h" in sys.argv or "--help" in sys.argv:
        sys.exit("Welcome to Snyph!\n" \
                 "-h, --help \t\t Show this help message\n" \
                 "-H, --header <header> \t Choose the header (if none, " \
                 "uses 01-60)\n" \
                 "-f, --freq <freq> \t Choose the frequency variable 0-10" \
                 " (if none, uses 0)\n" \
                 "-e, --encrypt <string> \t Encrypt a string\n" \
                 "-d, --decrypt <string> \t Decrypt a string\n" \
                 "Example: snyph.py -f 10 -e \"HELLO\"")

    if "-H" in sys.argv or "--header" in sys.argv:
        try:
            headerindex = sys.argv.index("-H")
        except:
            headerindex = sys.argv.index("--header")
        try:
            header = sys.argv[headerindex + 1]
        except:
            sys.exit("Invalid usage. Exiting.")
        if len(header) < 120:
            sys.exit("Header is invalid. Exiting.")
    else:
        header = defaultheader

    if "-f" in sys.argv or "--freq" in sys.argv:
        try:
            freqindex = sys.argv.index("-f")
        except:
            freqindex = sys.argv.index("--freq")
        try:
            freq = sys.argv[freqindex + 1]
        except:
            sys.exit("Invalid usage. Exiting.")
        try:
            freq = int(freq)
            if freq not in range(11):
                raise
        except:
            sys.exit("Frequency variable is invalid. Exiting.")
    else:
        freq = 0

# Function that encrypts a character into a snyph code
def encrypt(char):
    if char in grid:
        location = grid.find(char)
        set = location / 2 % 3 + 1
        sub = location / 12 + 1
        index = (location / 6 % 2) * 2 + location % 6 % 2 + 1
        # 5 random numbers
        junk = [str(random.randint(0, 9)) for i in range(5)]
        # The (sub)th place in the junk is replaced by the index
        junk[sub-1] = str(index)
        out = "{}{}{}".format(set, sub, "".join(junk))
        # Add noise according to the frequency variable
        out += "".join([str(random.randint(0,9)) for i in range(freq)])
        # Randomiser thing that I wasn't supposed to delete
        for i in range(freq):
            if random.randint(0, 1) == 1:
                rin = random.randint(0, len(out))
                out = out[:rin] + random.choice(["|", ";", "[", "]"]) \
                      + out[rin:]
        return out
    return "" #encrypt("%")

# Function that turns a string of characters into a fully encrypted
# string
def stringencrypt(string):
    out = ""
    global up
    for char in string:
        # If the character is the case switch, replace it with something
        # that is not on the snyph grid (cheeky hack)
        if char == "^":
            char = "|"
        # Checks if the case switches
        if (char in alphabet.upper() and not up) \
        or (char in alphabet and up):
            # In which case, insert a case shift (^)
            out += encrypt("^")
            # And change the global up variable
            up = not up
        char = char.upper()
        out += encrypt(char)
    return out

# Function that finds the characters based on the code
def stringdecrypt(string):
    out = ""
    # Remove everything that isn't a number
    string = "".join(filter(lambda x: x in "0123456789", list(string)))
    global up
    if len(string) % (7 + freq) != 0:
       return ""
    else:
        # Divide the string into groups of 7 + frequency variable
        for i in range(len(string) / (7 + freq)):
            # Find the character using the grid
            char = string[(7 + freq) * i:(7 + freq) * i + 7]
            set = int(char[0]) - 1
            sub = int(char[1]) - 1
            index = int(char[2 + sub]) - 1
            char = grid[12*sub + 2*set + 6 * (index > 1) + (index % 2)]
            # Change case if it finds a case switch
            if char == "^":
                up = not up
            else:
                # Change the case according to the global up variable
                if up:
                    out += char
                else:
                    out += char.lower()
    return out

# Making the header into a Python-readable format
try:
    headerlist = [int(header[2*i:2*i+2])-1 for i in range(len(header)/2)]
    headerlist = filter(lambda i: i < 60, headerlist)
# Also checking whether the header is legit
except:
    sys.exit("Header is invalid. Exiting.")

old = "APBQCR1=2(3)DSETFU4[5]6{GVHWIX7%8*9}JYKZL.0\"+-/\\M,N?O!:;'^\n "

# Adjusting the grid using the header
grid = [" " for i in range(60)]
for i in range(60):
    grid[i] = old[headerlist[i]]
grid = "".join(grid)

# Check for encryption or decryption flags, otherwise use a wizard
if "-e" in sys.argv or "--encrypt" in sys.argv:
    try:
        eindex = sys.argv.index("-e")
    except:
        eindex = sys.argv.index("--encrypt")
    try:
        input = sys.argv[eindex + 1]
    except:
        sys.exit("Invalid usage. Exiting.")
    print stringencrypt(input)
elif "-d" in sys.argv or "--decrypt" in sys.argv:
    try:
        dindex = sys.argv.index("-d")
    except:
        dindex = sys.argv.index("--decrypt")
    try:
        input = sys.argv[dindex + 1]
    except:
        sys.exit("Invalid usage. Exiting.")
    print stringdecrypt(input)
else:
    decision = raw_input("Encrypt (e) or decrypt (d): ")
    print "----"
    input = raw_input("Input: ")
    if decision.lower()[0] == "e":
        output = stringencrypt(input)
    elif decision.lower()[0] == "d":
        output = stringdecrypt(input)
    else:
        sys.exit("Sorry.")
    print "Output: " + output
