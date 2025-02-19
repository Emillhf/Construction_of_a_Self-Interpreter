import sys
import os
import Expander

def main():
    # Check if a filename is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    # Get the filename from the command line argument
    input_filename = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(input_filename):
        print(f"File '{input_filename}' not found.")
        sys.exit(1)

    # Create a new filename
    output_filename = f"Expanded_{input_filename}"

    try:
        # Read from the input file
        with open(input_filename, 'r') as infile:
            content = infile.readlines()
            Expanded = Expander.expand_rules(content,Expander.alfa,Expander.beta)
            print(Expanded)
        # Write the content to the new file
        with open(output_filename, 'w') as outfile:
            outfile.writelines(Expanded)

        print(f"Content has been written to '{output_filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
