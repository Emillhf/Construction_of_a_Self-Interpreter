import sys
import Inverter

if len(sys.argv) < 2:
    print("Please give a filename as an argument")
    exit(1)

    

name = sys.argv[1]
file = open("Compiler/macros/" + name, 'r')
lines = file.readlines()
lines = [line.strip() for line in lines]
inverted = Inverter.Invert(lines)
outfile = open("Compiler/macros/" + "rev_" + name,'w+')
for elm in inverted:
    outfile.write(elm + "\n")