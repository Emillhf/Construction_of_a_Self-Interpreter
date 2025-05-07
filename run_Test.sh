#!/bin/bash

# Check if a directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <test_cases_directory>"
    exit 1
fi

test_cases_dir="$1"

# Initialize counters for test results
success_count=0
fail_count=0

# Function to process inner folders
process_inner_folder() {
    local inner_folder="$1"
    # Find the required files in the inner folder
    program=$(find "$inner_folder" -maxdepth 1 -type f -name "program.txt")
    tape_file=$(find "$inner_folder" -maxdepth 1 -type f -name "tape.txt")

    if [[ -n "$program" ]]; then
        folder_name=$"$inner_folder"
        output_file="${inner_folder}/Expanded_program.txt"
        python3 Compiler/Compile_to_rules.py "$program" "$output_file"
        python_exit_code=$?
    fi

    if [ "$python_exit_code" -ne 0 ]; then
        echo "An error occoured in python" > "${inner_folder}/result.txt"
    fi

    expanded_file=$(find "$inner_folder" -maxdepth 1 -type f -name "Expanded_program.txt")

    if [[ -n "$expanded_file" && -n "$tape_file" && "$python_exit_code" -eq 0 ]]; then
        dotnet run --project Interpreter_FSharp "$expanded_file" "$tape_file" "test"
        exit_code=$?
    fi
    
    if [ "$exit_code" -ne 0 ]; then
        echo "An error occoured in the interpreter" > "${inner_folder}/result.txt"
    fi
    # Find result and expected files in the same folder
    result_file=$(find "$inner_folder" -maxdepth 1 -type f -name "result.txt")
    expected_file=$(find "$inner_folder" -maxdepth 1 -type f -name "expected.txt")
    if [[ -n "$result_file" && -n "$expected_file" ]]; then
        if cmp -s "$result_file" "$expected_file"; then
            echo "Successful test: $inner_folder"
            success_count=$((success_count + 1))
        else
            echo "Failed test: $inner_folder"
            fail_count=$((fail_count + 1))
        fi
    fi
}

# Find all immediate subdirectories and process them
while IFS= read -r folder; do
    process_inner_folder "$folder"
done < <(find "$test_cases_dir" -mindepth 1 -maxdepth 1 -type d)

echo "------------------------"
echo "Test Summary:"
echo "Successful tests: $success_count"
echo "Failed tests: $fail_count"
