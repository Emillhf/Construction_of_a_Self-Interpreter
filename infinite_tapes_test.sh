#!/bin/bash

# Find the required files in the inner folder
URTM=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "URTM.txt")
rev_URTM=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "rev_URTM.txt")
right_t1_left_t3=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "move_right_t1_left_t3.txt")
left_t1_right_t3=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "move_left_t1_right_t3.txt")

tape_BinInc=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "BinInc.txt")
tape_BinDec=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "BinDec.txt")


# echo "normal_normal:"
# dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$right_t1_left_t3$" 1 161 1

# echo "time_spent_normal_rev:"
# dotnet run --project Interpreter_1Tape_FSharp "$URTM" "$tape_BinDec" 1 21167 1

# echo "time_spent_rev_normal:"
# dotnet run --project Interpreter_1Tape_FSharp "$rev_URTM" "$tape_BinInc" 21167 1 1

# echo "time_spent_rev_rev:"
# dotnet run --project Interpreter_1Tape_FSharp "$rev_URTM" "$tape_BinDec" 21167 1 1

case1=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case1.txt")
case1_rev=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case1_rev.txt")
case2=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case2.txt")
case2_rev=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case2_rev.txt")
case3=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case3.txt")
case3_rev=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case3_rev.txt")
case4=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case4.txt")
case4_rev=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case4_rev.txt")
case5=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case5.txt")
case5_rev=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_case5_rev.txt")
onelong=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_one_long.txt")
oneblanklong=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_one_blank_long.txt")
twolong=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_two_long.txt")
twoblanklong=$(find "Tapes_1Tape_RTM" -maxdepth 1 -type f -name "infinite_two_blank_long.txt")



case1_out=$(dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$case1" 1 161 4)
file_content_case1=$(cat "$case1_rev")
if [[ "$case1_out" == "$file_content_case1" ]]; then
    echo "Success: case 1"
else
    echo "Failure: case 1"
fi

case1_rev_out=$(dotnet run --project Interpreter_1Tape_FSharp "$left_t1_right_t3" "$case1_rev" 1 161 4)
file_content_case1_rev=$(cat "$case1")
if [[ "$case1_rev_out" == "$file_content_case1_rev" ]]; then
    echo "Success: case 1 inversed"
else
    echo "Failure: case 1 inversed"
fi

case2_out=$(dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$case2" 1 161 3)
file_content_case2=$(cat "$case2_rev")
if [[ "$case2_out" == "$file_content_case2" ]]; then
    echo "Success: case 2"
else
    echo "Failure: case 2"
fi

case2_rev_out=$(dotnet run --project Interpreter_1Tape_FSharp "$left_t1_right_t3" "$case2_rev" 1 161 4)
file_content_case2_rev=$(cat "$case2")
if [[ "$case2_rev_out" == "$file_content_case2_rev" ]]; then
    echo "Success: case 2 inversed"
else
    echo "Failure: case 2 inversed"
fi

case3_out=$(dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$case3" 1 161 2)
file_content_case3=$(cat "$case3_rev")
if [[ "$case3_out" == "$file_content_case3" ]]; then
    echo "Success: case 3"
else
    echo "Failure: case 3"
fi

case3_rev_out=$(dotnet run --project Interpreter_1Tape_FSharp "$left_t1_right_t3" "$case3_rev" 1 161 3)
file_content_case3_rev=$(cat "$case3")
if [[ "$case3_rev_out" == "$file_content_case3_rev" ]]; then
    echo "Success: case 3 inversed"
else
    echo "Failure: case 3 inversed"
fi

case4_out=$(dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$case4" 1 161 2)
file_content_case4=$(cat "$case4_rev")
if [[ "$case4_out" == "$file_content_case4" ]]; then
    echo "Success: case 4"
else
    echo "Failure: case 4"
fi

case4_rev_out=$(dotnet run --project Interpreter_1Tape_FSharp "$left_t1_right_t3" "$case4_rev" 1 161 3)
file_content_case4_rev=$(cat "$case4")
if [[ "$case4_rev_out" == "$file_content_case4_rev" ]]; then
    echo "Success: case 4 inversed"
else
    echo "Failure: case 4 inversed"
fi

case5_out=$(dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$case5" 1 161 4)
file_content_case5=$(cat "$case5_rev")
if [[ "$case5_out" == "$file_content_case5" ]]; then
    echo "Success: case 5"
else
    echo "Failure: case 5"
fi

case5_rev_out=$(dotnet run --project Interpreter_1Tape_FSharp "$left_t1_right_t3" "$case5_rev" 1 161 5)
file_content_case5_rev=$(cat "$case5")
if [[ "$case5_rev_out" == "$file_content_case5_rev" ]]; then
    echo "Success: case 5 inversed"
else
    echo "Failure: case 5 inversed"
fi

onelong_out=$(dotnet run --project Interpreter_1Tape_FSharp "$left_t1_right_t3" "$onelong" 1 161 3)
file_content_two_long=$(cat "$twolong")
if [[ "$onelong_out" == "$file_content_two_long" ]]; then
    echo "Success: one long"
else
    echo "Failure: one long"
fi

onelong_out=$(dotnet run --project Interpreter_1Tape_FSharp "$right_t1_left_t3" "$twolong" 1 161 2)
file_content_one_long=$(cat "$onelong")
if [[ "$onelong_out" == "$file_content_one_long" ]]; then
    echo "Success: two long"
else
    echo "Failure: two long"
fi