import argparse
import os
import struct
import filecmp
import difflib
from helper import calculate_max_bit_length, choose_encoding_width


def bin_encode(input_file, encoding_width="int8"):
    with open(input_file, 'r', newline='') as f:
        # Read integers from the input CSV file
        integers = [int(line.strip()) for line in f]

    # Create the output file name with the encoding acronym and width
    output_file = os.path.join("encoded_files/",os.path.basename(input_file).rsplit(".", 1)[0] + ".csv.bin")

    mean_bits = calculate_max_bit_length(input_file)
    encoding_width = choose_encoding_width(mean_bits)

    # Determine the format string based on the encoding width
    if encoding_width == "int8":
        format_string = 'b'
    elif encoding_width == "int16":
        format_string = 'h'
    elif encoding_width == "int32":
        format_string = 'i'
    elif encoding_width == "int64":
        format_string = 'q'
    else:
        raise ValueError("Unsupported encoding width")

    with open(output_file, 'wb') as f:
        for value in integers:
            # Encode and write integers with the specified width
            f.write(struct.pack(format_string, value))

    return output_file

def bin_decode(input_file, original_csv_file, decoding_width="int8"):


    def compare_files_and_report(file1, file2):
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        # Perform a line-by-line comparison
        d = difflib.Differ()
        diff = list(d.compare(lines1, lines2))

        # Check if the files match
        files_match = all(line.startswith('  ') for line in diff)

        return files_match, diff


    mean_bits = calculate_max_bit_length(original_csv_file)
    decoding_width = choose_encoding_width(mean_bits) 

    # Define the format string based on the decoding width
    if decoding_width == "int8":
        format_string = 'b'
    elif decoding_width =="int16":
        format_string = 'h'
    elif decoding_width == "int32":
        format_string = 'i'
    elif decoding_width == "int64":
        format_string = 'q'
    else:
        raise ValueError("Unsupported decoding width")

    # Read binary data in chunks and decode as integers
    decoded_integers = []
    with open(input_file, 'rb') as f:
        chunk_size = struct.calcsize(format_string)
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            value = struct.unpack(format_string, data)[0]
            decoded_integers.append(value)

    # Create the output file path with the encoding acronym and width
    output_file = os.path.join("output/",os.path.basename(input_file).rsplit(".", 1)[0] + ".bin.csv")

    # Print the decoded integers to the output file in the specified folder
    with open(output_file, 'w') as f:
        for value in decoded_integers:
            f.write(str(value) + '\n')

    # Compare the output CSV file with the original CSV file
    files_match, differences = compare_files_and_report(output_file, original_csv_file)

    if files_match:
        print("The files match. No differences found.")
    else:
        print("The files do not match. Differences found.")
        print("Differences:")
        for line in differences:
            if line.startswith('  '):
                continue
            elif line.startswith('- '):
                print("Line removed:", line[2:])
            elif line.startswith('+ '):
                print("Line added:", line[2:])




