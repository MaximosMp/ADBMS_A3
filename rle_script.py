import os
import numpy as np
import pickle
from helper import choose_encoding_width, calculate_max_bit_length

def rle_encode(data_type, input_file):

    # Function to read data from a CSV file
    def read_csv(file_name):
        data = []
        with open(file_name, 'r') as file:
            for line in file:
                value = line.strip()
                data.append(value)
        return data

    # Read data from the CSV file and based on the data type
    if data_type.startswith("int"):
        data = [int(value) for value in read_csv(input_file)]
        max_bits = calculate_max_bit_length(input_file)
        data_type = choose_encoding_width(max_bits)
    else:
        data = read_csv(input_file)

    # RLE encoding
    encoded_data = []
    current_value = data[0]
    count = 1

    for i in range(1, len(data)):
        if data[i] == current_value:
            count += 1
        else:
            encoded_data.append((current_value, count))
            current_value = data[i]
            count = 1

    encoded_data.append((current_value, count))
    
    if data_type == 'int8':
        encoded_data = np.array(encoded_data, dtype=np.int8)
    elif data_type == 'int16':
        encoded_data = np.array(encoded_data, dtype=np.int16)
    elif data_type == 'int32':
        encoded_data = np.array(encoded_data, dtype=np.int32)
    elif data_type == 'int64':
        encoded_data = np.array(encoded_data, dtype=np.int64)

    # write encoded data to a new binary file
    encoded_file = os.path.join('encoded_files/',os.path.basename(input_file) + '.rle')
    with open(encoded_file, 'wb') as file:
        pickle.dump(encoded_data, file)
        
    return encoded_data


# Function to perform RLE decoding for any data type
# original data is the original csv file before encoding
def rle_decode(encoded_file):
    
    with open(encoded_file, 'rb') as file:
        encoded_data = pickle.load(file)

    decoded_data = []

    for value, count in encoded_data:
        decoded_data.extend([value] * count)

    # write decoded data to a new CSV file
    decoded_file = os.path.join("decoded_files", os.path.basename(encoded_file) + '.csv')
    with open(decoded_file, 'w') as file:
        for value in decoded_data:
            file.write(f"{value}\n")

    # # Validate the decoding
    # def validate_decoding(original_data, decoded_file):

    #     mismatch_positions = []

    #     for i in range(len(original_data)):
    #         if original_data[i] != decoded_file[i]:
    #             mismatch_positions.append(i)
    #             return False, mismatch_positions  # Mismatch found

    #     return True, mismatch_positions  # Data matches, decoding is successful
    
    # is_valid, mismatch_positions = validate_decoding(original_data, decoded_file)

    # if is_valid:
    #     print("Decoding is successful. Original and decoded data match.")
    # else:
    #     print("Decoding is not successful. There is a mismatch between original and decoded data. The mismatch positions are:", mismatch_positions)

    return decoded_data
