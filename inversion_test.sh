#!/bin/bash

# Find the required files in the inner folder
URTM=$(find "Expanded_RTM_programs" -maxdepth 1 -type f -name "URTM.txt")
rev_URTM=$(find "Expanded_RTM_programs" -maxdepth 1 -type f -name "rev_URTM.txt")
tape_BinInc=$(find "Tapes_RTM" -maxdepth 1 -type f -name "BinInc.txt")
tape_BinDec=$(find "Tapes_RTM" -maxdepth 1 -type f -name "BinDec.txt")

echo "time_spent_normal_normal:"
time dotnet run --project Interpreter_FSharp "$URTM" "$tape_BinInc" 1 0

echo "time_spent_normal_rev:"
time dotnet run --project Interpreter_FSharp "$URTM" "$tape_BinDec" 1 0

echo "time_spent_rev_normal:"
time dotnet run --project Interpreter_FSharp "$rev_URTM" "$tape_BinInc" 0 1

echo "time_spent_rev_rev:"
time dotnet run --project Interpreter_FSharp "$rev_URTM" "$tape_BinDec" 0 1


