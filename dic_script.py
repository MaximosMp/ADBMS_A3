import os
import pickle
import numpy as np
from helper import *

def getLinesFromFile(filename):
    file_handler = open(filename, 'r')
    lines = file_handler.readlines()
    file_handler.close()
    return lines

def writeFile(output_dir_path, file_path_arg, values_encoded, mapping):
    filename = os.path.basename(file_path_arg) + '.dic'
    file = os.path.join(output_dir_path, filename)
    dict_to_save = {'val': values_encoded, 'map': mapping}
    with open(file, 'wb') as handle:
        pickle.dump(dict_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)

def dic_encode(datatype, file_path_arg):
    # retrieve and store data
    values = list()
    lines = getLinesFromFile(file_path_arg)  
    if datatype == 'string': 
        for line in lines:   
            values.append(line)
    else:
        for line in lines:
            values.append(line.strip())

    # get unique values and map them to a number --> [[value, code], [], ..]
    values_uniq = list(set(values))
    mapping = dict()
    for i in range(len(values_uniq)):
        mapping[values_uniq[i]] = i

    # encode the data
    values_encoded = list()
    for value in values:
        values_encoded.append(mapping[value])

    # mapping from dict to list
    mapping = list(mapping.items())

    # correct the datatype for mapping and values_encoded if not string
    if datatype == 'string':
        max_bit_length = max(values_encoded).bit_length()
        datatype = choose_encoding_width(max_bit_length)
        if datatype == 'int8':
            values_encoded = np.array(values_encoded, dtype=np.int8)
        elif datatype == 'int16':
            values_encoded = np.array(values_encoded, dtype=np.int16)
        elif datatype == 'int32':
            values_encoded = np.array(values_encoded, dtype=np.int32)
        elif datatype == 'int64':
            values_encoded = np.array(values_encoded, dtype=np.int64)
    else:
        max_bit_length = max((int)(num).bit_length() for num in values)
        datatype = choose_encoding_width(max_bit_length)
        if datatype == 'int8':
            mapping = np.array(mapping, dtype=np.int8)
            values_encoded = np.array(values_encoded, dtype=np.int8)
        elif datatype == 'int16':
            mapping = np.array(mapping, dtype=np.int16)
            values_encoded = np.array(values_encoded, dtype=np.int16)
        elif datatype == 'int32':
            mapping = np.array(mapping, dtype=np.int32)
            values_encoded = np.array(values_encoded, dtype=np.int32)
        elif datatype == 'int64':
            mapping = np.array(mapping, dtype=np.int64)
            values_encoded = np.array(values_encoded, dtype=np.int64)

    # write to file  
    output_dir_path = make_output_dir('encoded_files')
    writeFile(output_dir_path, file_path_arg, values_encoded, mapping)

def dic_decode(file_path_arg):
    # retrieve and store data
    file_handler = open(file_path_arg, 'rb')
    with open(file_path_arg, 'rb') as file_handler:
        data = pickle.load(file_handler)
    file_handler.close()

    # list to dict mapping
    mapping = dict()
    for i in range(len(data['map'])):
        mapping[data['map'][i][1]] = data['map'][i][0]

    # decode the data
    values_decoded = list()
    for value in data['val']:
        values_decoded.append(mapping[value])
    
    # print data to console (stdout)
    for value in values_decoded:
        if isinstance(value, str):
            print(value.replace('\n', ''))
        else:
            print(value)