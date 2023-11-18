import argparse
import os
import struct
import filecmp
import difflib
from helper import *

def returnFullPath(filename):
    cwd = os.path.dirname(__file__)
    file_found, file_fullpath = False, None
    if filename in os.listdir(cwd):
        file_found = True
        file_fullpath = os.path.join(cwd, filename)
    
    if not file_found and 'data' in os.listdir(cwd):
        data_path = os.path.join(cwd, 'data')
        if filename in os.listdir(data_path):
            file_found = True
            file_fullpath = os.path.join(data_path, filename)
    
    if file_found:
        return file_fullpath
    else:
        return f'file not found + {filename}'


def bin_encode(input_file, encoding_width="int8"):
    with open(input_file, 'r', newline='') as f:
        # Read integers from the input CSV file
        integers = [int(line.strip()) for line in f]

    # Create the output file name with the encoding acronym and width
    tmp = os.path.basename(input_file) + '.bin'
    output_file = os.path.join(make_output_dir('encoded_files'), tmp) 

    bits = calculate_max_bit_length(input_file)
    encoding_width = choose_encoding_width(bits)

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

def bin_decode(input_file, decoding_width):
    original_filename = os.path.basename(input_file).rsplit(".")[0] + ".csv"
    original_filepath = returnFullPath(original_filename)

    bits = calculate_max_bit_length(original_filepath)
    decoding_width = choose_encoding_width(bits)

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
    # output_file = os.path.join("output/",os.path.basename(input_file).rsplit(".", 1)[0] + ".bin.csv")

    # Print the decoded integers to the output file in the specified folder
    # with open(output_file, 'w') as f:
    for value in decoded_integers:
        print(value)