import sys
import os
import time
from bin_script import bin_encode, bin_decode
from rle_script import rle_encode, rle_decode
from dic_script import dic_encode, dic_decode
from diff_script import * #differential_encoding_int8, differential_encoding_int16, differential_encoding_int32, differential_encoding_int64
from helper import ckeckCMD, printNotAcceptedCMD, make_output_dir, updateLogfile
from for_script import * #FrameOfReference_encoding_int8, FrameOfReference_encoding_int16, FrameOfReference_encoding_int32, FrameOfReference_encoding_int64

if __name__ == '__main__':

    # fetch the input file path
    input_file_path = ckeckCMD()

    # check if the input file path is valid
    if 'error' in input_file_path:
        printNotAcceptedCMD(input_file_path)
        exit()

    # start the timer
    start_timer = time.time()    

    if sys.argv[1] == 'en':

        if sys.argv[2] == 'bin':
            bin_encode(input_file_path, sys.argv[3])
        elif sys.argv[2] == 'rle':
            rle_encode(sys.argv[3], input_file_path)
        elif sys.argv[2] == 'dic':
            dic_encode(sys.argv[3], input_file_path)
        elif sys.argv[2] == 'for':
            output_dir_path = make_output_dir('encoded_files')
            filename = os.path.basename(input_file_path) + '.for'
            encoded_file = os.path.join(output_dir_path, filename)
           
            if sys.argv[3] == 'int8':       
                encoded_file = FrameOfReference_encoding_int8(input_file_path, encoded_file)

            elif sys.argv[3] == 'int16':
                encoded_file = FrameOfReference_encoding_int16(input_file_path, encoded_file)

            
            elif sys.argv[3] == 'int32':
                encoded_file = FrameOfReference_encoding_int32(input_file_path, encoded_file)

            
            elif sys.argv[3] == 'int64':
                encoded_file = FrameOfReference_encoding_int64(input_file_path, encoded_file)
          
            else:
                printNotAcceptedCMD('error_term')
                exit()


        elif sys.argv[2] == 'dif':
            output_dir_path = make_output_dir('encoded_files')
            filename = os.path.basename(input_file_path) + '.dif'
            encoded_file = os.path.join(output_dir_path, filename)

            if sys.argv[3] == 'int8':
                encoded_file = differential_encoding_int8(input_file_path, encoded_file)

            elif sys.argv[3] == 'int16':
                encoded_file = differential_encoding_int16(input_file_path, encoded_file)

            elif sys.argv[3] == 'int32':
                encoded_file = differential_encoding_int32(input_file_path, encoded_file)

            elif sys.argv[3] == 'int64':
                encoded_file = differential_encoding_int64(input_file_path, encoded_file)
        else:
            printNotAcceptedCMD('error_term')
            exit()


    elif sys.argv[1] == 'de':
        if sys.argv[2] == 'bin':
            bin_decode(input_file_path, sys.argv[2])
        elif sys.argv[2] == 'rle': 
            rle_decode(input_file_path)
        
        elif sys.argv[2] == 'dic':
            dic_decode(input_file_path)
        
        
        elif sys.argv[2] == 'for':

            if sys.argv[3] == 'int8':
                decoded_file = FrameOfReference_decoding_int8(input_file_path)

                for line in decoded_file:
                    print(line)

            elif sys.argv[3] == 'int16':
                decoded_file = FrameOfReference_decoding_int16(input_file_path)

                for line in decoded_file:
                    print(line)

            elif sys.argv[3] == 'int32':
                decoded_file = FrameOfReference_decoding_int32(input_file_path)

                for line in decoded_file:
                    print(line)

            elif sys.argv[3] == 'int64':
                decoded_file = FrameOfReference_decoding_int64(input_file_path)

                for line in decoded_file:
                    print(line)

            else:
                printNotAcceptedCMD('error_term')
                exit()
            



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
        original_file_size = os.path.getsize(input_file_path)
        filename = os.path.basename(input_file_path) + f'.{sys.argv[2]}'
        output_dir_path = make_output_dir('encoded_files')
        file = os.path.join(output_dir_path, filename)
        encoded_file_size = os.path.getsize(file)
        updateLogfile('logfile.txt', 'size', sys.argv, original_file_size, encoded_file_size)

    

    if sys.argv[1] == 'run_all':

        method = ['en', 'de']
        encoding = ['bin', 'rle', 'dic', 'for_', 'dif']
        width = ['int8', 'int16', 'int32', 'int64']

        for m in method:
            for e in encoding:
                for w in width:
                    
                    if m == 'en':
                        if e == bin:
                            bin_encode(input_file_path, w)
                        elif e == 'rle':
                            rle_encode(w, input_file_path)
                        elif e == 'dic':
                            dic_encode(w, input_file_path)
                        
                        elif e == 'for_':
                            output_dir_path = make_output_dir('encoded_files')
                            filename = os.path.basename(input_file_path) + '.for'
                            encoded_file = os.path.join(output_dir_path, filename)
                            if w == 'int8':
                                encoded_file = FrameOfReference_encoding_int8(input_file_path, encoded_file)
                            elif w == 'int16':
                                encoded_file = FrameOfReference_encoding_int16(input_file_path, encoded_file)
                            elif w == 'int32':
                                encoded_file = FrameOfReference_encoding_int32(input_file_path, encoded_file)
                            elif w == 'int64':
                                encoded_file = FrameOfReference_encoding_int64(input_file_path, encoded_file)
                            else:
                                printNotAcceptedCMD('error_term')
                                exit()
                        elif e == 'dif':
                            output_dir_path = make_output_dir('encoded_files')
                            filename = os.path.basename(input_file_path) + '.dif'
                            encoded_file = os.path.join(output_dir_path, filename)
                            if w == 'int8':
                                encoded_file = differential_encoding_int8(input_file_path, encoded_file)
                            elif w == 'int16':
                                encoded_file = differential_encoding_int16(input_file_path, encoded_file)
                            elif w == 'int32':
                                encoded_file = differential_encoding_int32(input_file_path, encoded_file)
                            elif w == 'int64':
                                encoded_file = differential_encoding_int64(input_file_path, encoded_file)
                            else:
                                printNotAcceptedCMD('error_term')
                                exit()
                        else:
                            printNotAcceptedCMD('error_term')
                            exit()
                    elif m == 'de':
                        if e == bin:
                            bin_decode(input_file_path, w)
                        elif e == 'rle': 
                            rle_decode(input_file_path)
                        elif e == 'dic':
                            dic_decode(input_file_path)
                        elif e == 'for_':
                            if w == 'int8'