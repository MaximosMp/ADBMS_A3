import csv
import numpy as np
import os
from helper import *

def for_controller_encode(datatype, file):
    output_dir_path = make_output_dir('encoded_files')
    filename = os.path.basename(file) + '.for'
    encoded_file = os.path.join(output_dir_path, filename)
    
    if datatype == 'int8':       
        encoded_file = FrameOfReference_encoding_int8(file, encoded_file)
    elif datatype == 'int16':
        encoded_file = FrameOfReference_encoding_int16(file, encoded_file)
    elif datatype == 'int32':
        encoded_file = FrameOfReference_encoding_int32(file, encoded_file)
    elif datatype == 'int64':
        encoded_file = FrameOfReference_encoding_int64(file, encoded_file)


def for_controller_decode(datatype, file):
    if datatype == 'int8':
        FrameOfReference_decoding_int8(file)
    elif datatype == 'int16':
        FrameOfReference_decoding_int16(file)
    elif datatype == 'int32':
        FrameOfReference_decoding_int32(file)
    elif datatype == 'int64':
        FrameOfReference_decoding_int64(file)


def FrameOfReference_encoding_int8(input_file, output_file):
    #first we read the first 200 lines
    sample = []
    
    with open(input_file, 'r') as text_in:
        for line in text_in:
            current_value = int(line.strip())
            sample.append(current_value)
            
            if len(sample) == 200:
                break

    frame = int(np.mean(sample))

    count = 0
    escape_code = int(-128).to_bytes(length=1, byteorder='big',signed=True)  # Special escape code for differences that can't be represented in 8 bits

    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())
            diff = current_value - frame
            
            if count == 0:
                #running_value = current_value
                binary_out.write(frame.to_bytes(length=1, byteorder='big', signed=False))
                
            if -127 <= diff <= 127:
                binary_out.write(diff.to_bytes(length=1, byteorder='big', signed=True))
                #running_value = current_value

            else:
                binary_out.write(escape_code)
                binary_out.write(current_value.to_bytes(length=1, byteorder='big', signed=False))

            count+=1

def FrameOfReference_decoding_int8(input_file):
    first_row = True
    escape = 0

    with open(input_file, 'rb') as binary_in:
        while True:
            if first_row:
                chunk = binary_in.read(1)
                if not chunk:
                    break

                frame = int.from_bytes(chunk, byteorder = 'big', signed = False)

                first_row = False
            else:
                if escape == 1:
                    chunk = binary_in.read(1)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                    
                    print(f"{current_value}")

                    escape = 0
                    
                else:
                    chunk = binary_in.read(1)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if -127 <= current_value <= 127:
                        diff = frame + current_value
                        print(f"{diff}")
                    else:
                        escape = 1

def FrameOfReference_encoding_int16(input_file, output_file):
    #first we read the first 200 lines
    sample = []
    
    with open(input_file, 'r') as text_in:
        for line in text_in:
            current_value = int(line.strip())
            sample.append(current_value)
            
            if len(sample) == 200:
                break

    frame = int(np.mean(sample))

    count = 0
    escape_code = int(-128).to_bytes(length=1, byteorder='big',signed=True)  # Special escape code for differences that can't be represented in 8 bits

    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())
            diff = current_value - frame
            
            if count == 0:
                #running_value = current_value
                binary_out.write(frame.to_bytes(length=2, byteorder='big', signed=False))
                
            if -127 <= diff <= 127:
                binary_out.write(diff.to_bytes(length=1, byteorder='big', signed=True))
                #running_value = current_value

            else:
                binary_out.write(escape_code)
                binary_out.write(current_value.to_bytes(length=2, byteorder='big', signed=False))

            count+=1

def FrameOfReference_decoding_int16(input_file):
    first_row = True
    escape = 0

    with open(input_file, 'rb') as binary_in:
        while True:
            if first_row:
                chunk = binary_in.read(2)
                if not chunk:
                    break

                frame = int.from_bytes(chunk, byteorder = 'big', signed = False)

                first_row = False
            else:
                if escape == 1:
                    chunk = binary_in.read(2)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                    
                    print(f"{current_value}")

                    escape = 0
                    
                else:
                    chunk = binary_in.read(1)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if -127 <= current_value <= 127:
                        diff = frame + current_value
                        print(f"{diff}")
                    else:
                        escape = 1



def FrameOfReference_encoding_int32(input_file, output_file):
    #first we read the first 200 lines
    sample = []
    
    with open(input_file, 'r') as text_in:
        for line in text_in:
            current_value = int(line.strip())
            sample.append(current_value)
            
            if len(sample) == 200:
                break

    frame = int(np.mean(sample))
    

    sample_diff = []
    for i in sample:
        sample_diff.append(i-frame)

    if -128 <= np.quantile(sample_diff, 0.9) <= 127:
        escape_length = 1
    else:
        escape_length = 2

    #print(frame, escape_length)    
    count = 0
    escape_code = int(-2**((8*escape_length)-1)).to_bytes(length=escape_length, byteorder='big',signed=True)  # Special escape code for differences
    min_diff = -2**((8*escape_length)-1)+1
    max_diff = abs(min_diff)
    
    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())
            diff = current_value - frame
            
            if count == 0:
                #running_value = current_value
                binary_out.write(escape_length.to_bytes(length=1, byteorder='big', signed=True)) ## write escape code
                binary_out.write(frame.to_bytes(length=3, byteorder='big', signed=False))

                #print(0, escape_length.to_bytes(length=1, byteorder='big', signed=True))
                #print(1, frame.to_bytes(length=3, byteorder='big', signed=False))
                
            if min_diff <= diff <= max_diff:
                binary_out.write(diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                #print(2, diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                #running_value = current_value

            else:
                binary_out.write(escape_code)
                #print(2, escape_code)
                #print(3, current_value, current_value.to_bytes(length=3, byteorder='big', signed=False))
                binary_out.write(current_value.to_bytes(length=3, byteorder='big', signed=False))

            count+=1


def FrameOfReference_decoding_int32(input_file):
    first_row = True
    escape = 0

    with open(input_file, 'rb') as binary_in:
        while True:
            if first_row:
                chunk = binary_in.read(1)
                #print(0, chunk)
                if not chunk:
                    break

                escape_length = int.from_bytes(chunk, byteorder='big', signed = True)
                min_diff = -2**((8*escape_length)-1)+1
                max_diff = abs(min_diff)
                
                chunk = binary_in.read(3)
                if not chunk:
                    break

                frame = int.from_bytes(chunk, byteorder = 'big', signed = False)
                #print(1, chunk)
                
                first_row = False
            else:
                if escape == 1:
                    chunk = binary_in.read(3)
                    #print(3, chunk)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                    #print(current_value)
                    
                    print(f"{current_value}")

                    escape = 0
                    
                else:
                    chunk = binary_in.read(escape_length)
                    #print(2,chunk)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
                    #print(current_value)
    
                    if min_diff <= current_value <= max_diff:
                        diff = frame + current_value
                        #print(frame, current_value, diff)
                        print(f"{diff}")
                    else:
                        escape = 1

def FrameOfReference_encoding_int64(input_file, output_file):
    #first we read the first 200 lines
    sample = []
    
    with open(input_file, 'r') as text_in:
        for line in text_in:
            current_value = int(line.strip())
            sample.append(current_value)
            
            if len(sample) == 200:
                break

    frame = int(np.mean(sample))

    sample_diff = []
    for i in sample:
        sample_diff.append(i-frame)

    if -128 <= np.quantile(sample_diff, 0.9) <= 127:
        escape_length = 1
    elif -32768 <= np.quantile(sample_diff, 0.9) <= 32767:
        escape_length = 2
    else:
        escape_length = 3
        
    count = 0
    escape_code = int(-2**((8*escape_length)-1)).to_bytes(length=escape_length, byteorder='big',signed=True)  # Special escape code for differences
    min_diff = -2**((8*escape_length)-1)+1
    max_diff = abs(min_diff)
    
    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())
            diff = current_value - frame
            
            if count == 0:
                #running_value = current_value
                binary_out.write(escape_length.to_bytes(length=1, byteorder='big', signed=True)) ## write escape code
                binary_out.write(frame.to_bytes(length=4, byteorder='big', signed=False))
                
            if min_diff <= diff <= max_diff:
                binary_out.write(diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                #running_value = current_value

            else:
                binary_out.write(escape_code)
                binary_out.write(current_value.to_bytes(length=4, byteorder='big', signed=False))

            count+=1

def FrameOfReference_decoding_int64(input_file):
    first_row = True
    escape = 0

    with open(input_file, 'rb') as binary_in:
        while True:
            if first_row:
                chunk = binary_in.read(1)
                if not chunk:
                    break

                escape_length = int.from_bytes(chunk, byteorder='big', signed = True)
                min_diff = -2**((8*escape_length)-1)+1
                max_diff = abs(min_diff)
                
                chunk = binary_in.read(4)
                if not chunk:
                    break

                frame = int.from_bytes(chunk, byteorder = 'big', signed = False)

                first_row = False
            else:
                if escape == 1:
                    chunk = binary_in.read(4)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=False)
                    
                    print(f"{current_value}")

                    escape = 0
                    
                else:
                    chunk = binary_in.read(escape_length)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if min_diff <= current_value <= max_diff:
                        diff = frame + current_value
                        print(f"{diff}")
                    else:
                        escape = 1
