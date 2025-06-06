#!/bin/bash

# Find the required files in the inner folder
URTM=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "URTM.txt")
rev_URTM=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "rev_URTM.txt")
right_t1_left_t3=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "move_right_t1_left_t3.txt")
rev_right_t1_left_t3=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "rev_move_right_t1_left_t3.txt")
left_t1_right_t3=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "move_left_t1_right_t3.txt")
rev_left_t1_right_t3=$(find "1_Tape_Programs" -maxdepth 1 -type f -name "rev_move_left_t1_right_t3.txt")



# echo "normal_normal:"
# dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$right_t1_left_t3$" 1 161 1

# echo "time_spent_normal_rev:"
# dotnet run --project Interpreter_1_tape "$URTM" "$tape_BinDec" 1 21167 1

# echo "time_spent_rev_normal:"
# dotnet run --project Interpreter_1_tape "$rev_URTM" "$tape_BinInc" 21167 1 1

# echo "time_spent_rev_rev:"
# dotnet run --project Interpreter_1_tape "$rev_URTM" "$tape_BinDec" 21167 1 1

case1=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case1.txt")
case1_rev=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case1_rev.txt")
case2=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case2.txt")
case2_rev=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case2_rev.txt")
case3=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case3.txt")
case3_rev=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case3_rev.txt")
case4=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case4.txt")
case4_rev=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case4_rev.txt")
case5=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case5.txt")
case5_rev=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_case5_rev.txt")
onelong=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_one_long.txt")
oneblanklong=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_one_blank_long.txt")
twolong=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_two_long.txt")
twoblanklong=$(find "1_Tape_tapes" -maxdepth 1 -type f -name "infinite_two_blank_long.txt")



case1_out=$(dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$case1" 1 161 4)
file_content_case1=$(cat "$case1_rev")
if [[ "$case1_out" == "$file_content_case1" ]]; then
    echo "Success: case 1 right"
else
    echo "Failure: case 1  right"
fi

rev_case1_out=$(dotnet run --project Interpreter_1_tape "$rev_right_t1_left_t3" "$case1_rev" 161 1 4)
rev_file_content_case1=$(cat "$case1")
if [[ "$rev_case1_out" == "$rev_file_content_case1" ]]; then
    echo "Success: rev case 1 right"
else
    echo "Failure: rev case 1 right"
fi

case1_left_out=$(dotnet run --project Interpreter_1_tape "$left_t1_right_t3" "$case1_rev" 1 161 4)
file_content_case1_left=$(cat "$case1")
if [[ "$case1_left_out" == "$file_content_case1_left" ]]; then
    echo "Success: case 1 left"
else
    echo "Failure: case 1 left"
fi

rev_case1_left_out=$(dotnet run --project Interpreter_1_tape "$rev_left_t1_right_t3" "$case1" 161 1 4)
file_content_case1_left_rev=$(cat "$case1_rev")
if [[ "$rev_case1_left_out" == "$file_content_case1_left_rev" ]]; then
    echo "Success: rev case 1 left"
else
    echo "Failure: rev case 1 left"
fi

case2_out=$(dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$case2" 1 161 3)
file_content_case2=$(cat "$case2_rev")
if [[ "$case2_out" == "$file_content_case2" ]]; then
    echo "Success: case 2 right"
else
    echo "Failure: case 2 right"
fi

case2_rev_out=$(dotnet run --project Interpreter_1_tape "$rev_right_t1_left_t3" "$case2_rev" 161 1 4)
file_content_case2_rev=$(cat "$case2")
if [[ "$case2_rev_out" == "$file_content_case2_rev" ]]; then
    echo "Success: rev case 2 right"
else
    echo "Failure: rev case 2 right"
fi

case2_left_out=$(dotnet run --project Interpreter_1_tape "$left_t1_right_t3" "$case2_rev" 1 161 4)
file_content_case2_left=$(cat "$case2")
if [[ "$case2_left_out" == "$file_content_case2_left" ]]; then
    echo "Success: case 2 left"
else
    echo "Failure: case 2 left"
fi

case2_left_rev_out=$(dotnet run --project Interpreter_1_tape "$rev_left_t1_right_t3" "$case2" 161 1 3)
file_content_case2_left_rev=$(cat "$case2_rev")
if [[ "$case2_left_rev_out" == "$file_content_case2_left_rev" ]]; then
    echo "Success: rev case 2 left"
else
    echo "Failure: rev case 2 left"
fi

case3_out=$(dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$case3" 1 161 2)
file_content_case3=$(cat "$case3_rev")
if [[ "$case3_out" == "$file_content_case3" ]]; then
    echo "Success: case 3 right"
else
    echo "Failure: case 3 right"
fi

case3_rev_right_out=$(dotnet run --project Interpreter_1_tape "$rev_right_t1_left_t3" "$case3_rev" 161 1 3)
file_content_case3_right_rev=$(cat "$case3")
if [[ "$case3_rev_right_out" == "$file_content_case3_right_rev" ]]; then
    echo "Success: rev case 3 right"
else
    echo "Failure: rev case 3 right"
fi

case3_left_out=$(dotnet run --project Interpreter_1_tape "$left_t1_right_t3" "$case3_rev" 1 161 3)
file_content_case3_left=$(cat "$case3")
if [[ "$case3_left_out" == "$file_content_case3_left" ]]; then
    echo "Success: case 3 left"
else
    echo "Failure: case 3 left"
fi

case3_left_rev_out=$(dotnet run --project Interpreter_1_tape "$rev_left_t1_right_t3" "$case3" 161 1 2)
file_content_case3_left_rev=$(cat "$case3_rev")
if [[ "$case3_left_rev_out" == "$file_content_case3_left_rev" ]]; then
    echo "Success: rev case 3 left"
else
    echo "Failure: rev case 3 left"
fi

case4_out_right=$(dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$case4" 1 161 2)
file_content_case4_right=$(cat "$case4_rev")
if [[ "$case4_out_right" == "$file_content_case4_right" ]]; then
    echo "Success: case 4 right"
else
    echo "Failure: case 4 right"
fi

case4_out_right_rev=$(dotnet run --project Interpreter_1_tape "$rev_right_t1_left_t3" "$case4_rev" 161 1 3)
file_content_case4_right_rev=$(cat "$case4")
if [[ "$case4_out_right_rev" == "$file_content_case4_right_rev" ]]; then
    echo "Success: rev case 4 right"
else
    echo "Failure: rev case 4 right"
fi

case4_left_out=$(dotnet run --project Interpreter_1_tape "$left_t1_right_t3" "$case4_rev" 1 161 3)
file_content_case4_left=$(cat "$case4")
if [[ "$case4_left_out" == "$file_content_case4_left" ]]; then
    echo "Success: case 4 left"
else
    echo "Failure: case 4 left"
fi

case4_left_rev_out=$(dotnet run --project Interpreter_1_tape "$rev_left_t1_right_t3" "$case4" 161 1 2)
file_content_case4_left_rev=$(cat "$case4_rev")
if [[ "$case4_left_rev_out" == "$file_content_case4_left_rev" ]]; then
    echo "Success: rev case 4 left"
else
    echo "Failure: rev case 4 left"
fi

case5_out_right=$(dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$case5" 1 161 4)
file_content_case5=$(cat "$case5_rev")
if [[ "$case5_out_right" == "$file_content_case5" ]]; then
    echo "Success: case 5 right"
else
    echo "Failure: case 5 right"
fi

case5_out_right_rev=$(dotnet run --project Interpreter_1_tape "$rev_right_t1_left_t3" "$case5_rev" 161 1 5)
file_content_case5_rev=$(cat "$case5")
if [[ "$case5_out_right_rev" == "$file_content_case5_rev" ]]; then
    echo "Success: rev case 5 right"
else
    echo "Failure: rev case 5 right"
fi

case5_left_out=$(dotnet run --project Interpreter_1_tape "$left_t1_right_t3" "$case5_rev" 1 161 5)
file_content_case5_left=$(cat "$case5")
if [[ "$case5_left_out" == "$file_content_case5_left" ]]; then
    echo "Success: case 5 left"
else
    echo "Failure: case 5 left"
fi

case5_left_out_rev=$(dotnet run --project Interpreter_1_tape "$rev_left_t1_right_t3" "$case5" 161 1 4)
file_content_case5_left_rev=$(cat "$case5_rev")
if [[ "$case5_left_out_rev" == "$file_content_case5_left_rev" ]]; then
    echo "Success: rev case 5 left"
else
    echo "Failure: rev case 5 left"
fi

onelong_out=$(dotnet run --project Interpreter_1_tape "$left_t1_right_t3" "$onelong" 1 161 3)
file_content_two_long=$(cat "$twolong")
if [[ "$onelong_out" == "$file_content_two_long" ]]; then
    echo "Success: one long"
else
    echo "Failure: one long"
fi

onelong_out=$(dotnet run --project Interpreter_1_tape "$right_t1_left_t3" "$twolong" 1 161 2)
file_content_one_long=$(cat "$onelong")
if [[ "$onelong_out" == "$file_content_one_long" ]]; then
    echo "Success: two long"
else
    echo "Failure: two long"
fi