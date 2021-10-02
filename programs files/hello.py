import os
import sys
name2 = os.popen("set USERNAME").read().split("=")[1]
if len(sys.argv) > 1:
    name2 = sys.argv[1]
print("hello >> " + name2)
print("its very nice to see u!!\n"
      "BYE BYE")
