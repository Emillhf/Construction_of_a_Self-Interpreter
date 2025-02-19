import sys
import os
import Expander
import StateTransitioner

if len(sys.argv) < 2:
    print("Please give a filename as an argument")
    exit(1)

input_filename = sys.argv[1]

if not os.path.isfile(input_filename):
    print(f"File '{input_filename}' not found.")
    exit(1)

output_filename = f"Expanded_{input_filename}"

file = open(input_filename, 'r')
lines = file.readlines()
start = lines[0].strip()
final = lines[1].strip()
lines_expanded = Expander.expand_rules(lines[2:], Expander.alfa, Expander.beta)
lines_stateTransitioned = StateTransitioner.StateTransition(lines_expanded, start, final)
outfile = open(output_filename, 'w+')
outfile.writelines(lines_stateTransitioned)
