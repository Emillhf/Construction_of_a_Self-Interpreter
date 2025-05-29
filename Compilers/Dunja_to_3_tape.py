import sys
import os
import Expander
import StateTransitioner
import Macros
import Read_file

input_filename,output_filename = Read_file.input_file()

file = open(input_filename, 'r')
lines = file.readlines()
start = lines[0].strip()
final = lines[1].strip()
lines = [line.strip() for line in lines]
lines_macroed = Macros.Expand_macros(lines[2:])
lines_expanded = Expander.expand_rules(lines_macroed, Expander.alfa, Expander.beta)
lines_stateTransitioned = StateTransitioner.StateTransition(lines_expanded, start, final)
outfile = open("3_Tape_programs/" + output_filename, 'w+')
outfile.writelines(lines_stateTransitioned)
