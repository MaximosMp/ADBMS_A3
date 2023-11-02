# %%
import csv
import numpy as np

# %% [markdown]
# # INT 8

# %% [markdown]
# ### Encoding

# %%
def differential_encoding_int8(input_file, output_file):
    running_value = 0  
    count = 0
    escape_code = int(-128).to_bytes(length=1, byteorder='big',signed=True)  # Special escape code for differences that can't be represented in 8 bits

    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())

            if count == 0:
                #running_value = current_value
                binary_out.write(current_value.to_bytes(length=1, byteorder='big', signed=True)) ## write value in 16 bits
            else:
                diff = current_value - running_value

                if -127 <= diff <= 127:
                    binary_out.write(diff.to_bytes(length=1, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=1, byteorder='big', signed=True))


            running_value = current_value
            count+=1

# %%
input_csv_file = 'ADM-2023-Assignment-3-data-TPCH-SF-1\l_tax-int8.csv'
output_dif_file = 'encoded_output.csv.dif'

differential_encoding_int8(input_csv_file, output_dif_file)

#from 11,722 KB to 5,861 KB

# %% [markdown]
# ### Decoding

# %%
def differential_decoding_int8(input_file, output_file):
    running_value = 0
    escape = 1

    with open(input_file, 'rb') as binary_in, open(output_file, 'w') as text_out:
        while True:
            if escape == 1:
                chunk = binary_in.read(1)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder= 'big', signed=True)
                
                text_out.write(f"{current_value}\n")
                running_value = current_value
                escape = 0
            else:
                chunk = binary_in.read(1)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)

                if -127 <= current_value <= 127:
                    running_value += current_value
                    text_out.write(f"{running_value}\n")
                else:
                    escape = 1
                
            

# %%
input_dif_file = 'encoded_output.csv.dif'
output_csv_file = 'decoded_output.csv.dif.csv'

differential_decoding_int8(input_dif_file, output_csv_file)

# back to 11,722 KB

# %% [markdown]
# # INT 16

# %% [markdown]
# ### Encoding

# %%
def differential_encoding_int16(input_file, output_file):
    running_value = 0  
    count = 0
    escape_code = int(-128).to_bytes(length=1, byteorder='big',signed=True)  # Special escape code for differences that can't be represented in 8 bits

    with open(input_file, 'r') as text_in, open(output_file, 'wb') as binary_out:
        for line in text_in:
            current_value = int(line.strip())

            if count == 0:
                #running_value = current_value
                binary_out.write(current_value.to_bytes(length=2, byteorder='big', signed=True)) ## write value in 16 bits
            else:
                diff = current_value - running_value

                if -127 <= diff <= 127:
                    binary_out.write(diff.to_bytes(length=1, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=2, byteorder='big', signed=True))


            running_value = current_value
            count+=1
                    
                

# %%
input_csv_file = 'ADM-2023-Assignment-3-data-TPCH-SF-1\l_discount-int16.csv'
output_dif_file = 'encoded_output.csv.dif'

differential_encoding_int16(input_csv_file, output_dif_file)

#from 12,255 KB to 5,861 KB

# %% [markdown]
# ### Decoding

# %%
def differential_decoding_int16(input_file, output_file):
    running_value = 0
    escape = 1

    with open(input_file, 'rb') as binary_in, open(output_file, 'w') as text_out:
        while True:
            if escape == 1:
                chunk = binary_in.read(2)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder= 'big', signed=True)
                
                text_out.write(f"{current_value}\n")
                running_value = current_value
                escape = 0
            else:
                chunk = binary_in.read(1)
                if not chunk:
                    break
                current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)

                if -127 <= current_value <= 127:
                    running_value += current_value
                    text_out.write(f"{running_value}\n")
                else:
                    escape = 1
                
            

# %%
input_dif_file = 'encoded_output.csv.dif'
output_csv_file = 'decoded_output.csv.dif.csv'

differential_decoding_int16(input_dif_file, output_csv_file)

# back to 12,255 KB

# %% [markdown]
# # INT 32

# %% [markdown]
# ### Encoding

# %%
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
                binary_out.write(current_value.to_bytes(length=3, byteorder='big', signed=True)) ## write value in 32 bits
            else:
                diff = current_value - running_value

                if min_diff <= diff <= max_diff:
                    binary_out.write(diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=3, byteorder='big', signed=True))


            running_value = current_value
            count+=1
                    
                

# %%
input_csv_file = 'ADM-2023-Assignment-3-data-TPCH-SF-1\l_suppkey-int32.csv'
output_dif_file = 'encoded_output.csv.dif'

differential_encoding_int32(input_csv_file, output_dif_file)

#from 28,655 KB to 11,722 KB

# %% [markdown]
# ### Decoding

# %%
def differential_decoding_int32(input_file, output_file):
    running_value = 0
    escape = 1
    first_row = True
    
    with open(input_file, 'rb') as binary_in, open(output_file, 'w') as text_out:
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
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=True)
                    
                    text_out.write(f"{current_value}\n")
                    running_value = current_value
                    escape = 0
                else:
                    chunk = binary_in.read(escape_length)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if min_diff <= current_value <= max_diff:
                        running_value += current_value
                        text_out.write(f"{running_value}\n")
                    else:
                        escape = 1
                    
            

# %%
input_dif_file = 'encoded_output.csv.dif'
output_csv_file = 'decoded_output.csv.dif.csv'

differential_decoding_int32(input_dif_file, output_csv_file)

# back to 28,655 KB

# %% [markdown]
# # INT 64

# %% [markdown]
# ### Encoding

# %%
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
                binary_out.write(current_value.to_bytes(length=4, byteorder='big', signed=True)) ## write value in 64 bits
            else:
                diff = current_value - running_value

                if min_diff <= diff <= max_diff:
                    binary_out.write(diff.to_bytes(length=escape_length, byteorder='big', signed=True))
                    #running_value = current_value

                else:
                    binary_out.write(escape_code)
                    binary_out.write(current_value.to_bytes(length=4, byteorder='big', signed=True))


            running_value = current_value
            count+=1

# %%
input_csv_file = 'ADM-2023-Assignment-3-data-TPCH-SF-1\l_extendedprice-int64.csv'
output_dif_file = 'encoded_output.csv.dif'

differential_encoding_int64(input_csv_file, output_dif_file)

# from 46,131 KB to 17,689

# %% [markdown]
# ### Decoding

# %%
def differential_decoding_int64(input_file, output_file):
    running_value = 0
    escape = 1
    first_row = True
    
    with open(input_file, 'rb') as binary_in, open(output_file, 'w') as text_out:
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
                    current_value = int.from_bytes(chunk, byteorder= 'big', signed=True)
                    
                    text_out.write(f"{current_value}\n")
                    running_value = current_value
                    escape = 0
                else:
                    chunk = binary_in.read(escape_length)
                    if not chunk:
                        break
                    current_value = int.from_bytes(chunk, byteorder = 'big', signed = True)
    
                    if min_diff <= current_value <= max_diff:
                        running_value += current_value
                        text_out.write(f"{running_value}\n")
                    else:
                        escape = 1
                    
            

# %%
input_dif_file = 'encoded_output.csv.dif'
output_csv_file = 'decoded_output.csv.dif.csv'

differential_decoding_int64(input_dif_file, output_csv_file)

# back to 46,131 KB


