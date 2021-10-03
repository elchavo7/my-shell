import sys

if len(sys.argv) == 2:
    with open(sys.argv[1], "rb") as file:
        data = file.read()

    decimal_exsp = data.hex()
    print(decimal_exsp)
else:
    print("[-] not enough parameters")
