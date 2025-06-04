import Inverter
import Read_file

filename, name = Read_file.input_file()
lines = Read_file.read_file(filename)
inverted = Inverter.Invert1Tape(lines)
if name.find("/") == -1:
    Read_file.write_to_file(filename.replace(name,'') + 'rev_' + name, inverted)
else:
    outfile = open(name, 'w+')