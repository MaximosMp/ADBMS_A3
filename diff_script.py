import csv
import numpy as np
from helper import *

def dif_controller_encode(datatype, filename):
    output_dir_path = make_output_dir('encoded_files')
    file = os.path.basename(filename) + '.dif'
    encoded_file = os.path.join(output_dir_path, file)

    if datatype == 'int8':
        encoded_file = differential_encoding_int8(filename, encoded_file)
    elif datatype == 'int16':
        encoded_file = differential_encoding_int16(filename, encoded_file)
    elif datatype == 'int32':
        encoded_file = differential_encoding_int32(filename, encoded_file)
    elif datatype == 'int64':
        encoded_file = differential_encoding_int64(filename, encoded_file)


def dif_controller_decode(datatype, file):
    if datatype == 'int8':
        differential_decoding_int8(file)
    elif datatype == 'int16':
        differential_decoding_int16(file)
    elif datatype == 'int32':
        differential_decoding_int32(file)
    elif datatype == 'int64':
        differential_decoding_int64(file)


def differential_encoding_int8(input_file, output_file):
    running_value = 0  
    count = 0
    escape_code = int(-128).to_bytes(length=1, byteorder='big',signed=True)  # Special escape code for differences that can't be represented in 8 bits

    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())

            if count == 0:
                #running_value = current_value
                binary_out.write(current_value.to_bytes(length=1, byteorder='big', signed=False)) ## write value in 16 bits
            else:
                diff = current_value - running_value

                if -127 <= diff <= 127:
                    binary_out.write(diff.to_bytes(length=1, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=1, byteorder='big', signed=False))


            running_value = current_value
            count+=1

def differential_decoding_int8(input_file):
    running_value = 0
    escape = 1

    with open(input_file, 'rb') as binary_in:
        while True:
            if escape == 1:
                chunk = binary_in.read(1)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                
                print(f"{current_value}")
                running_value = current_value
                escape = 0
            else:
                chunk = binary_in.read(1)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)

                if -127 <= current_value <= 127:
                    running_value += current_value
                    print(f"{running_value}")
                else:
                    escape = 1
                
            
                
            
def differential_encoding_int16(input_file, output_file):
    running_value = 0  
    count = 0
    escape_code = int(-128).to_bytes(length=1, byteorder='big',signed=True)  # Special escape code for differences that can't be represented in 8 bits

    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())

            if count == 0:
                #running_value = current_value
                binary_out.write(current_value.to_bytes(length=2, byteorder='big', signed=False)) ## write value in 16 bits
            else:
                diff = current_value - running_value

                if -127 <= diff <= 127:
                    binary_out.write(diff.to_bytes(length=1, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=2, byteorder='big', signed=False))


            running_value = current_value
            count+=1
                    
                
                    
def differential_decoding_int16(input_file):
    running_value = 0
    escape = 1

    with open(input_file, 'rb') as binary_in:
        while True:
            if escape == 1:
                chunk = binary_in.read(2)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                
                print(f"{current_value}")
                running_value = current_value
                escape = 0
            else:
                chunk = binary_in.read(1)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)

                if -127 <= current_value <= 127:
                    running_value += current_value
                    print(f"{running_value}")
                else:
                    escape = 1
                
            
                
def differential_encoding_int32(input_file, output_file):
    
    #first we read the first 201 lines to get 200 differences
    sample = []
    sample_count = 0
    sample_prev = 0
    
    with open(input_file, 'r') as text_in:
        for line in text_in:
            current_value = int(line.strip())
    
            if sample_count > 0:
                sample_diff = current_value - sample_prev
                sample.append(sample_diff)
            
            sample_count+=1
            sample_prev = current_value
    
            if len(sample) == 200:
                break

    if -128 <= np.quantile(sample, 0.9) <= 127:
        escape_length = 1
    else:
        escape_length = 2
        
    running_value = 0  
    count = 0
    escape_code = int(-2**((8*escape_length)-1)).to_bytes(length=escape_length, byteorder='big',signed=True)  # Special escape code for differences
    min_diff = -2**((8*escape_length)-1)+1
    max_diff = abs(min_diff)

    
    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())

            if count == 0:
                #running_value = current_value
                binary_out.write(escape_length.to_bytes(length=1, byteorder='big', signed=True)) ## write escape code
                binary_out.write(current_value.to_bytes(length=3, byteorder='big', signed=False)) ## write value in 32 bits
            else:
                diff = current_value - running_value

                if min_diff <= diff <= max_diff:
                    binary_out.write(diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=3, byteorder='big', signed=False))


            running_value = current_value
            count+=1
                    
                
                    
                
def differential_decoding_int32(input_file):
    running_value = 0
    escape = 1
    first_row = True
    
    with open(input_file, 'rb') as binary_in:
        while True:
            if first_row:
                chunk = binary_in.read(1)
                if not chunk:
                    break

                escape_length = int.from_bytes(chunk, byteorder='big', signed = True)
                min_diff = -2**((8*escape_length)-1)+1
                max_diff = abs(min_diff)

                first_row = False
            else:
                if escape == 1:
                    chunk = binary_in.read(3)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                    
                    print(f"{current_value}")
                    running_value = current_value
                    escape = 0
                else:
                    chunk = binary_in.read(escape_length)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if min_diff <= current_value <= max_diff:
                        running_value += current_value
                        print(f"{running_value}")
                    else:
                        escape = 1
                    
            
                    
            
def differential_encoding_int64(input_file, output_file):
    
    #first we read the first 201 lines to get 200 differences
    sample = []
    sample_count = 0
    sample_prev = 0
    
    with open(input_file, 'r') as text_in:
        for line in text_in:
            current_value = int(line.strip())
    
            if sample_count > 0:
                sample_diff = current_value - sample_prev
                sample.append(sample_diff)
            
            sample_count+=1
            sample_prev = current_value
    
            if len(sample) == 200:
                break

    if -128 <= np.quantile(sample, 0.9) <= 127:
        escape_length = 1
    elif -32768 <= np.quantile(sample, 0.9) <= 32767:
        escape_length = 2
    else:
        escape_length = 3
        
    running_value = 0  
    count = 0
    escape_code = int(-2**((8*escape_length)-1)).to_bytes(length=escape_length, byteorder='big',signed=True)  # Special escape code for differences
    min_diff = -2**((8*escape_length)-1)+1
    max_diff = abs(min_diff)

    
    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())

            if count == 0:
                #running_value = current_value
                binary_out.write(escape_length.to_bytes(length=1, byteorder='big', signed=True)) ## write escape code
                binary_out.write(current_value.to_bytes(length=4, byteorder='big', signed=False)) ## write value in 64 bits
            else:
                diff = current_value - running_value

                if min_diff <= diff <= max_diff:
                    binary_out.write(diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=4, byteorder='big', signed=False))


            running_value = current_value
            count+=1

def differential_decoding_int64(input_file):
    running_value = 0
    escape = 1
    first_row = True
    
    with open(input_file, 'rb') as binary_in:
        while True:
            if first_row:
                chunk = binary_in.read(1)
                if not chunk:
                    break

                escape_length = int.from_bytes(chunk, byteorder='big', signed = True)
                min_diff = -2**((8*escape_length)-1)+1
                max_diff = abs(min_diff)

                first_row = False
            else:
                if escape == 1:
                    chunk = binary_in.read(4)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                    
                    print(f"{current_value}")
                    running_value = current_value
                    escape = 0
                else:
                    chunk = binary_in.read(escape_length)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if min_diff <= current_value <= max_diff:
                        running_value += current_value
                        print(f"{running_value}")
                    else:
                        escape = 1
                    
            
                    