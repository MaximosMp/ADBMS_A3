import sys
import os
import time


#from bin_script import bin_encode, bin_decode
#from rle_script import rle_encode, rle_decode
from dic_script import dic_encode, dic_decode

from for_script import (
    FrameOfReference_encoding_int8,  FrameOfReference_decoding_int8,
    FrameOfReference_encoding_int16, FrameOfReference_decoding_int16,
    FrameOfReference_encoding_int32, FrameOfReference_decoding_int32,
    FrameOfReference_encoding_int64, FrameOfReference_decoding_int64
)

from diff_script import (
    differential_encoding_int8,  differential_decoding_int8,
    differential_encoding_int16, differential_decoding_int16,
    differential_encoding_int32, differential_decoding_int32,
    differential_encoding_int64, differential_decoding_int64
)

# from for_script import for_encode, for_decode
# from dif_script import dif_encode, dif_decode
from helper import *

if __name__ == '__main__':
    response = ckeckCMD()
    if 'error' in response:
        printNotAcceptedCMD(response)
        exit()

    start_timer = time.time()    

    if sys.argv[1] == 'en':
        if sys.argv[2] == 'bin':
            pass
        elif sys.argv[2] == 'rle':
            pass
        elif sys.argv[2] == 'dic':
            dic_encode(sys.argv[3], response)
        elif sys.argv[2] == 'for':
            pass
        elif sys.argv[2] == 'dif':
            pass
        else:
            printNotAcceptedCMD('error_term')
            exit()
    elif sys.argv[1] == 'de':
        if sys.argv[2] == 'bin':
            pass
        elif sys.argv[2] == 'rle': 
            pass
        elif sys.argv[2] == 'dic':
            dic_decode(response)
        elif sys.argv[2] == 'for':
            pass
        elif sys.argv[2] == 'dif':
            pass
        else:
            printNotAcceptedCMD('error_term')
            exit()
    else:
        printNotAcceptedCMD('error_term')
        exit()

    end_timer = time.time()
    updateLogfile('logfile.txt', 'time', sys.argv, start_timer, end_timer)

    if sys.argv[1] == 'en':
        original_file_size = os.path.getsize(response)
        filename = os.path.basename(response) + '.dic'
        output_dir_path = make_output_dir('encoded_files')
        file = os.path.join(output_dir_path, filename)
        encoded_file_size = os.path.getsize(file)
        updateLogfile('logfile.txt', 'size', sys.argv, original_file_size, encoded_file_size)
        pass

    # ------------ maximos

    if sys.argv[1] == 'en':

        if sys.arg[2] == 'for':

            original_file_size = os.path.getsize(response)
            filename = os.path.basename(response) + '.for'

            path = sys.arg[3]

            outfile = 'encoded_files/' + filename + '.for

            encoded_file = FrameOfReference_encoding_int8(path, outfile)

            encoded_file_size = os.path.getsize(encoded_file)

            updateLogfile('logfile.txt', 'size', sys.argv, original_file_size, encoded_file_size)

        elif sys.arg[2] == 'dif':

            original_file_size = os.path.getsize(response)
            filename = os.path.basename(response) + '.dif'

            path = sys.arg[3]

            outfile = 'encoded_files/' + filename + '.dif

            encoded_file = differential_encoding_int8(path, outfile)

            encoded_file_size = os.path.getsize(encoded_file)

            updateLogfile('logfile.txt', 'size', sys.argv, original_file_size, encoded_file_size)
        
        else:

            pass
    
    elif sys.argv[1] == 'de':

        if sys.arg[2] == 'for':

        #####

            path = sys.arg[3]

            decoded_file = FrameOfReference_decoding_int8(path, outfile)

        ######

        elif sys.arg[2] == 'dif':

        ####

            path = sys.arg[3]

            decoded_file = differential_decoding_int8(path, outfile)

        ####
        
        else:

            pass

