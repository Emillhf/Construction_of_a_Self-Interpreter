#!/bin/bash

# Find the required files in the inner folder
URTM=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "URTM.txt")
rev_URTM=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "rev_URTM.txt")
tape_BinInc=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "BinInc.txt")
tape_BinDec=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "BinDec.txt")

echo "time_spent_normal_normal:"
time dotnet run --project Interpreter_1Tape_FSharp "$URTM" "$tape_BinInc" 1 21167

echo "time_spent_normal_rev:"
time dotnet run --project Interpreter_1Tape_FSharp "$URTM" "$tape_BinDec" 1 21167

echo "time_spent_rev_normal:"
time dotnet run --project Interpreter_1Tape_FSharp "$rev_URTM" "$tape_BinInc" 21167 1

echo "time_spent_rev_rev:"
time dotnet run --project Interpreter_1Tape_FSharp "$rev_URTM" "$tape_BinDec" 21167 1


