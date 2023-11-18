# ADBMS_A3
 comp and decomp methods benchmark

In the assignment, we consider

• a total of 5 (five) compression techniques:

◦ “bin”: uncompressed binary format (for integer types, only), 1

◦ “rle”: run-length encoding,

◦ “dic”: dictionary encoding,

◦ “for”: frame of reference encoding (for integer types, only),

◦ “dif”: differential encoding (for integer types, only);

• a total of 5 (five) data types:

◦ “int8”: 8-bit (1-byte) integer,

◦ “int16”: 16-bit (2-byte) integer,

◦ “int32”: 32-bit (4-byte) integer,

◦ “int64”: 64-bit (8-byte) integer,

◦ “string”: character string of arbitrary length.

# Folders and Files
- data: This folder has all 33 original files

- encoded_files: Contains all the files that are encoded

- decoded_files: Contains all the files that have been decoded

- program.py: The main program, the only one that we run for encoding and decoding. The corresponding file leverages five other secondary python scripts

- helper.py: It has methods that all the algorithms/scripts use.

- bin_script.py: BIN encoding.

- dic_script.py: DIC encoding.

- diff_script.py: DIFF encoding.

- rle_script.py: RLE encoding.

- for_script.py: FOR encoding.

- script.sh: Bash script that runs all the experiments.


# How to run

## 1. Run a single file 

### 1.1. Encoding
encoding syntax: python program.py en {alg} {datatype} {file}
$ python program.py en bin int8 l_discount-int8.csv

### 1.2. Decoding
decoding syntax: python program.py de {alg} {datatype} {file}.{alg} > decoded_files/{file}.{alg}.csv
$ python program.py de bin int8 l_discount-int8.csv.bin > decoded_files/l_discount-int8.csv.bin

### 1.3. Check the integrity
integrity check syntax: diff data/{file} decoded_files/{file}.{alg}.csv
diff data/l_discount-int8.csv decoded_files/l_discount-int8.csv.bin.csv

## 2. Run all the experiments
./script.sh
