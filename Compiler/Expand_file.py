import sys
import os
import Expander

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
Expanded = Expander.expand_rules(lines, Expander.alfa, Expander.beta)
outfile = open(output_filename, 'w+')
outfile.writelines(Expanded)
