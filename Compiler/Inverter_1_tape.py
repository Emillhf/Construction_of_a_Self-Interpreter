import Inverter

name = input()
file = open("1_Tape_programs/" + name, 'r')
lines = file.readlines()
lines = [line.strip() for line in lines]
inverted = Inverter.Invert1Tape(lines)
outfile = open("1_Tape_programs/" + "rev_" + name,'w+')
for elm in inverted:
    outfile.write(elm + "\n")