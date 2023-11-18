import sys
import os
import time
from bin_script import bin_encode, bin_decode
from rle_script import rle_encode, rle_decode
from dic_script import dic_encode, dic_decode
from diff_script import * 
from helper import ckeckCMD, printNotAcceptedCMD, make_output_dir, updateLogfile, findDatatype
from for_script import * 


if __name__ == '__main__':

    # fetch the input file path
    input_file_path = ckeckCMD()

    # check if the input file path is valid
    if 'error' in input_file_path:
        printNotAcceptedCMD(input_file_path)
        exit()

    # start the timer
    start_timer = time.time()    

    # encoding phase
    if sys.argv[1] == 'en':
        if sys.argv[2] == 'bin':
            bin_encode(input_file_path, sys.argv[3])
        elif sys.argv[2] == 'rle':
            rle_encode(sys.argv[3], input_file_path)
        elif sys.argv[2] == 'dic':
            dic_encode(sys.argv[3], input_file_path)
        elif sys.argv[2] == 'for':
            for_controller_encode(sys.argv[3], input_file_path)
        elif sys.argv[2] == 'dif':
            dif_controller_encode(sys.argv[3], input_file_path) 
    elif sys.argv[1] == 'de':
        if sys.argv[2] == 'bin':
            bin_decode(input_file_path, sys.argv[3])
        elif sys.argv[2] == 'rle': 
            rle_decode(input_file_path)
        elif sys.argv[2] == 'dic':
            dic_decode(input_file_path)
        elif sys.argv[2] == 'for':
            for_controller_decode(sys.argv[3], input_file_path)
        elif sys.argv[2] == 'dif':
            dif_controller_decode(sys.argv[3], input_file_path)


    end_timer = time.time()
    updateLogfile('logfile.txt', 'time', sys.argv, start_timer, end_timer)

    if sys.argv[1] == 'en':
        original_file_size = os.path.getsize(input_file_path)
        filename = os.path.basename(input_file_path) + f'.{sys.argv[2]}'
        output_dir_path = make_output_dir('encoded_files')
        file = os.path.join(output_dir_path, filename)
        encoded_file_size = os.path.getsize(file)
        updateLogfile('logfile.txt', 'size', sys.argv, original_file_size, encoded_file_size)