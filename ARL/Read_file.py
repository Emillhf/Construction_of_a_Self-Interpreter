import sys
import os

def read_file(input_filename):
    file = open(input_filename, 'r')
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def extract_elms_tape(rule):
    rule = rule.replace('(','')
    rule = rule.replace(')','')
    rule = rule.split(',')
    return rule

def write_to_file(output_filename, data):
    outfile = open(output_filename, 'w+')
    for line in data:
        outfile.write(line + "\n")
  
def input_file():      
    if len(sys.argv) < 2:
        print("Please give a filename as an argument")
        exit(1)
    elif (len(sys.argv) ==3):
        output_filename = sys.argv[2]
        return sys.argv[1], output_filename
    return sys.argv[1], sys.argv[1].split('/')[-1]

