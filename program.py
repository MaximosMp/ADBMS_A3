import sys
import os
import time


#from bin_script import bin_encode, bin_decode
#from rle_script import rle_encode, rle_decode
from dic_script import dic_encode, dic_decode
from diff_script import for_encode, for_decode
#from dif_script import dif_encode, dif_decode


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