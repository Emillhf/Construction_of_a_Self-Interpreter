#!/bin/bash

# Find the required files in the inner folder
URTM=$(find "3_Tape_programs" -maxdepth 1 -type f -name "URTM.txt")
rev_URTM=$(find "3_Tape_programs" -maxdepth 1 -type f -name "rev_URTM.txt")
tape_BinInc=$(find "3_Tape_tapes" -maxdepth 1 -type f -name "BinInc.txt")
tape_BinDec=$(find "3_Tape_tapes" -maxdepth 1 -type f -name "BinDec.txt")
echo "------- 3 tape interpreter -------"
echo "running: normal_normal:"
normal_normal=$(dotnet run --project Interpreter_3_tape "$URTM" "$tape_BinInc" 1 0)

echo "running: normal_rev:"
normal_rev=$(dotnet run --project Interpreter_3_tape "$URTM" "$tape_BinDec" 1 0)

echo "running: rev_normal:"
rev_normal=$(dotnet run --project Interpreter_3_tape "$rev_URTM" "$tape_BinInc" 0 1)

echo "running: rev_rev:"
rev_rev=$(dotnet run --project Interpreter_3_tape "$rev_URTM" "$tape_BinDec" 0 1)

echo ""

if [[ "${normal_normal[@]:0:5}" == "${rev_rev[@]:0:5}" ]]; then
    echo "Success: normal_normal equals rev_rev"
else
    echo "Failure: normal_normal does not equals rev_rev"
fi

if [[ "${normal_rev[@]:0:5}" == "${rev_normal[@]:0:5}" ]]; then
    echo "Success: normal_rev equals rev_normal"
else
    echo "Failure: normal_rev does not equals rev_normal"
fi

echo ""
echo "------- 1 tape interpreter -------"
echo ""

# Find the required files in the inner folder
URTM_1tape=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "URTM.txt")
rev_URTM_1tape=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "rev_URTM.txt")
tape_BinInc_1tape=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "BinInc.txt")
tape_BinDec_1tape=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "BinDec.txt")

echo "running: normal_normal_1tape:"
normal_normal_1tape=$(dotnet run --project Interpreter_1_tape "$URTM_1tape" "$tape_BinInc_1tape" 1 21167 1)

echo "running: normal_rev_1tape:"
normal_rev_1tape=$(dotnet run --project Interpreter_1_tape "$URTM_1tape" "$tape_BinDec_1tape" 1 21167 1)

echo "running: rev_normal_1tape:"
rev_normal_1tape=$(dotnet run --project Interpreter_1_tape "$rev_URTM_1tape" "$tape_BinInc_1tape" 21167 1 1)

echo "running: rev_rev_1tape:"
rev_rev_1tape=$(dotnet run --project Interpreter_1_tape "$rev_URTM_1tape" "$tape_BinDec_1tape" 21167 1 1)

echo ""

if [[ "${normal_normal_1tape[@]:0:5}" == "${rev_rev_1tape[@]:0:5}" ]]; then
    echo "Success: normal_normal_1tape equals rev_rev_1tape"
else
    echo "Failure: normal_normal_1tape does not equals rev_rev_1tape"
fi

if [[ "${normal_rev_1tape[@]:0:5}" == "${rev_normal_1tape[@]:0:5}" ]]; then
    echo "Success: normal_rev_1tape equals rev_normal_1tape"
else
    echo "Failure: normal_rev_1tape does not equals rev_normal_1tape"
fi




