import os
import sys

def ckeckCMD():
    '''
    Ckeck the command line from the terminal for validity and print the corresponding message (if needed).
    '''
    accepted_arg1 = ['en','de']
    accepted_arg2 = ['bin','rle','dic','for','dif']
    accepted_arg3 = ['int8','int16','int32','int64','string']

    if len(sys.argv)!=5:
        return 'error_length'
    
    if sys.argv[1] not in accepted_arg1 or sys.argv[2] not in accepted_arg2 or sys.argv[3] not in accepted_arg3:
        return 'error_term'
    
    cwd = os.path.dirname(__file__)
    file_found, file_fullpath = False, None
    if sys.argv[4] in os.listdir(cwd):
        file_found = True
        file_fullpath = os.path.join(cwd, sys.argv[4])
    
    if not file_found and 'data' in os.listdir(cwd):
        data_path = os.path.join(cwd, 'data')
        if sys.argv[4] in os.listdir(data_path):
            file_found = True
            file_fullpath = os.path.join(data_path, sys.argv[4])
    
    if not file_found and 'encoded_files' in os.listdir(cwd):
        encoded_files_path = os.path.join(cwd, 'encoded_files')
        if sys.argv[4] in os.listdir(encoded_files_path):
            file_found = True
            file_fullpath = os.path.join(encoded_files_path, sys.argv[4])

    if not file_found:
        return 'error_file'
    
    return file_fullpath


def printNotAcceptedCMD(error_msg):
    '''
    Print error message in case checkCMD() function returns error code.
    param error_msg:    the error message from the given error command line 
    '''
    stdout = 'The command was not accepted due to the following reason:'
    if error_msg == 'error_length':
        print(f'{stdout} too many/few arguments')
    if error_msg == 'error_term':
        print(f'{stdout} wrong argument(s) given')
    if error_msg == 'error_file':
        print(f'{stdout} file not found in the working directory')
    print('Please run the file using the following format:')
    print('$ python program.py (en|de) (bin|rle|dic|for|dif) (int8|int16|int32|int64|string) filename')


def updateLogfile(file, logging, cmd, start, end):
    file_handler = open(file, 'a')
    if logging == 'time':
        time = end - start
        file_handler.write(f'Command: {cmd}     |     Time: {time}\n')
    elif logging == 'size':
        file_handler.write(f'Command: {cmd}     |     Original file size: {start}     |     Encoded file size: {end}\n')
    else:
        file_handler.write(f'Ooops! Something went wrong! (You gave the wrong logging type)\n')
    file_handler.close()

def make_output_dir(target):
    cwd = os.path.dirname(__file__)
    output_path = os.path.join(cwd, target)
    try:
        os.mkdir(output_path)
    except OSError as error:
        print(error)
    return output_path


def calculate_max_bit_length(input_file):
    with open(input_file, 'r') as f:
        integers = [int(line.strip()) for line in f]

    max_bit_length = max(num.bit_length() for num in integers)
    return max_bit_length

def choose_encoding_width(mean_bits):
    if mean_bits <= 8:
        return "int8"
    elif mean_bits <= 16:
        return "int16"
    elif mean_bits <= 32:
        return "int32"
    elif mean_bits <= 64:
        return "int64"
    else:
        raise ValueError("Unsupported encoding width")


