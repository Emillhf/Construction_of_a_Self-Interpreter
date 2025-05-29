# Construction of a RTM Self-Interpreter

This is the repository for all the code used in constructing a RTM Self-Interpreter

## Requirements

  - Python version 3.11  
  - Dotnet version 8.0

## Compiling and interpreting Dünja program
The prerequisites is:
  - Dünja program  
  - 3 Tape file  

Note: 
  - Start state is always 1 
  - Final state is always 0 
  - These are flipped when the program is inverted

The following is a demonstration of how to compile and interpret a Dünja program and the according 3 tape file:
```bash
python3 Compilers/Dunja_to_3_tape.py Dunja_programs/< program >
dotnet run --project Interpreter_3_tape 3_Tape_programs/< program > 3_Tape_tapes/< tape > < start_state > < final_state >
```
Example with the URTM.txt written in Dünja and the 3 tape file for BinInc
```bash
python3 Compilers/Dunja_to_3_tape.py Dunja_programs/URTM.txt
dotnet run --project Interpreter_3_Tape 3_Tape_programs/URTM.txt 3_Tape_tapes/BinInc.txt 1 0
```

## Compiling and interpreting 1-Tape programs
The prerequisites for compiling and interpreting 1-Tape programs and tapes:
  - 3-tape program 
  - 1 tape file

Note: 
  - Start state is always 1 
  - Final state is shown when compiling 3-tape to 1-tape
  - These are flipped when the program is inverted

Demonstration of compiling a 3-tape program to 1-tape program and interpreting the 1-tape program
```bash
python3 Compilers/3_tape_to_1.py 3_Tape_programs/< program >
dotnet run --project Interpreter_1_tape 1_Tape_programs/< program > 1_Tape_tapes/< tape > < start_state > < final_state >
```

Example with the URTM.txt written in Dünja and the 3 tape file for BinInc
```bash
python3 Compilers/3_tape_to_1_tape.py 3_Tape_programs/URTM.txt
dotnet run --project Interpreter_1_tape 1_Tape_programs/URTM.txt 1_Tape_tapes/BinInc.txt 1 21167
```

## Inverting 3-tape program
```bash
python3 Compilers/Inverter_3_tape.py 3_Tape_programs/< program >
```
Example
```bash
python3 Compilers/Inverter_3_tape.py 3_Tape_programs/URTM.txt
```

## Inverting 1-tape program
```bash
python3 Compilers/Inverter_1_tape.py 1_Tape_programs/< program >
```
Example
```bash
python3 Compilers/Inverter_1_tape.py 1_Tape_programs/URTM.txt
```

## Testing
We have used bash script for testing our code.
The testing scripts are the following:
  - run_Test.sh <directory>  
  - infinite_tapes_test.sh  
  - inversion_test.sh  

Possible directories for run_Test.sh are <Test_suite, Test_suite_reverse, Test_interpreter>.

