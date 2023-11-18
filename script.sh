#!/bin/bash

decode_and_check() {
	python program.py de "$1" "$2" "$3"."$1" > decoded_files/"$3"."$1".csv
	echo "$3."$1" > decoded_files/"$3"."$1".csv" >> errors_logfile.txt
	diff data/"$3" decoded_files/"$3"."$1".csv >> errors_logfile.txt
}

# encoding phase: bin, for, dif
for tech in 'bin' 'for' 'dif'
do
	python program.py en $tech int16 l_discount-int16.csv
	python program.py en $tech int32 l_discount-int32.csv
	python program.py en $tech int64 l_discount-int64.csv
	python program.py en $tech int8 l_discount-int8.csv
	python program.py en $tech int32 l_extendedprice-int32.csv
	python program.py en $tech int64 l_extendedprice-int64.csv
	python program.py en $tech int16 l_linenumber-int16.csv
	python program.py en $tech int32 l_linenumber-int32.csv
	python program.py en $tech int64 l_linenumber-int64.csv
	python program.py en $tech int8 l_linenumber-int8.csv
	python program.py en $tech int32 l_orderkey-int32.csv
	python program.py en $tech int64 l_orderkey-int64.csv
	python program.py en $tech int32 l_partkey-int32.csv
	python program.py en $tech int64 l_partkey-int64.csv
	python program.py en $tech int16 l_quantity-int16.csv
	python program.py en $tech int32 l_quantity-int32.csv
	python program.py en $tech int64 l_quantity-int64.csv
	python program.py en $tech int8 l_quantity-int8.csv
	python program.py en $tech int16 l_suppkey-int16.csv
	python program.py en $tech int32 l_suppkey-int32.csv
	python program.py en $tech int64 l_suppkey-int64.csv
	python program.py en $tech int16 l_tax-int16.csv
	python program.py en $tech int32 l_tax-int32.csv
	python program.py en $tech int64 l_tax-int64.csv
	python program.py en $tech int8 l_tax-int8.csv
done


# decoding phase: bin, for, dif
for tech in 'bin' 'for' 'dif'
do
	decode_and_check $tech "int16" "l_discount-int16.csv"
	decode_and_check $tech "int32" "l_discount-int32.csv"
	decode_and_check $tech "int64" "l_discount-int64.csv"
	decode_and_check $tech "int8" "l_discount-int8.csv"
	decode_and_check $tech "int32" "l_extendedprice-int32.csv"
	decode_and_check $tech "int64" "l_extendedprice-int64.csv"
	decode_and_check $tech "int16" "l_linenumber-int16.csv"
	decode_and_check $tech "int32" "l_linenumber-int32.csv"
	decode_and_check $tech "int64" "l_linenumber-int64.csv"
	decode_and_check $tech "int8" "l_linenumber-int8.csv"
	decode_and_check $tech "int32" "l_orderkey-int32.csv"
	decode_and_check $tech "int64" "l_orderkey-int64.csv"
	decode_and_check $tech "int32" "l_partkey-int32.csv"
	decode_and_check $tech "int64" "l_partkey-int64.csv"
	decode_and_check $tech "int16" "l_quantity-int16.csv"
	decode_and_check $tech "int32" "l_quantity-int32.csv"
	decode_and_check $tech "int64" "l_quantity-int64.csv"
	decode_and_check $tech "int8" "l_quantity-int8.csv"
	decode_and_check $tech "int16" "l_suppkey-int16.csv"
	decode_and_check $tech "int32" "l_suppkey-int32.csv"
	decode_and_check $tech "int64" "l_suppkey-int64.csv"
	decode_and_check $tech "int16" "l_tax-int16.csv"
	decode_and_check $tech "int32" "l_tax-int32.csv"
	decode_and_check $tech "int64" "l_tax-int64.csv"
	decode_and_check $tech "int8" "l_tax-int8.csv"
done


#---------------------------------------------------------------------


# encoding phase: rle, dic
for tech in 'rle' 'dic'
do
	python program.py en $tech string l_comment-string.csv
	python program.py en $tech string l_commitdate-string.csv
	python program.py en $tech int16 l_discount-int16.csv
	python program.py en $tech int32 l_discount-int32.csv
	python program.py en $tech int64 l_discount-int64.csv
	python program.py en $tech int8 l_discount-int8.csv
	python program.py en $tech int32 l_extendedprice-int32.csv
	python program.py en $tech int64 l_extendedprice-int64.csv
	python program.py en $tech int16 l_linenumber-int16.csv
	python program.py en $tech int32 l_linenumber-int32.csv
	python program.py en $tech int64 l_linenumber-int64.csv
	python program.py en $tech int8 l_linenumber-int8.csv
	python program.py en $tech string l_linestatus-string.csv
	python program.py en $tech int32 l_orderkey-int32.csv
	python program.py en $tech int64 l_orderkey-int64.csv
	python program.py en $tech int32 l_partkey-int32.csv
	python program.py en $tech int64 l_partkey-int64.csv
	python program.py en $tech int16 l_quantity-int16.csv
	python program.py en $tech int32 l_quantity-int32.csv
	python program.py en $tech int64 l_quantity-int64.csv
	python program.py en $tech int8 l_quantity-int8.csv
	python program.py en $tech string l_receiptdate-string.csv
	python program.py en $tech string l_returnflag-string.csv
	python program.py en $tech string l_shipdate-string.csv
	python program.py en $tech string l_shipinstruct-string.csv
	python program.py en $tech string l_shipmode-string.csv
	python program.py en $tech int16 l_suppkey-int16.csv
	python program.py en $tech int32 l_suppkey-int32.csv
	python program.py en $tech int64 l_suppkey-int64.csv
	python program.py en $tech int16 l_tax-int16.csv
	python program.py en $tech int32 l_tax-int32.csv
	python program.py en $tech int64 l_tax-int64.csv
	python program.py en $tech int8 l_tax-int8.csv
done


# decoding phase: rle, dic
for tech in 'rle' 'dic'
do
	decode_and_check $tech "string" "l_comment-string.csv"
	decode_and_check $tech "string" "l_commitdate-string.csv"
	decode_and_check $tech "int16" "l_discount-int16.csv"
	decode_and_check $tech "int32" "l_discount-int32.csv"
	decode_and_check $tech "int64" "l_discount-int64.csv"
	decode_and_check $tech "int8" "l_discount-int8.csv"
	decode_and_check $tech "int32" "l_extendedprice-int32.csv"
	decode_and_check $tech "int64" "l_extendedprice-int64.csv"
	decode_and_check $tech "int16" "l_linenumber-int16.csv"
	decode_and_check $tech "int32" "l_linenumber-int32.csv"
	decode_and_check $tech "int64" "l_linenumber-int64.csv"
	decode_and_check $tech "int8" "l_linenumber-int8.csv"
	decode_and_check $tech "string" "l_linestatus-string.csv"
	decode_and_check $tech "int32" "l_orderkey-int32.csv"
	decode_and_check $tech "int64" "l_orderkey-int64.csv"
	decode_and_check $tech "int32" "l_partkey-int32.csv"
	decode_and_check $tech "int64" "l_partkey-int64.csv"
	decode_and_check $tech "int16" "l_quantity-int16.csv"
	decode_and_check $tech "int32" "l_quantity-int32.csv"
	decode_and_check $tech "int64" "l_quantity-int64.csv"
	decode_and_check $tech "int8" "l_quantity-int8.csv"
	decode_and_check $tech "string" "l_receiptdate-string.csv"
	decode_and_check $tech "string" "l_returnflag-string.csv"
	decode_and_check $tech "string" "l_shipdate-string.csv"
	decode_and_check $tech "string" "l_shipinstruct-string.csv"
	decode_and_check $tech "string" "l_shipmode-string.csv"
	decode_and_check $tech "int16" "l_suppkey-int16.csv"
	decode_and_check $tech "int32" "l_suppkey-int32.csv"
	decode_and_check $tech "int64" "l_suppkey-int64.csv"
	decode_and_check $tech "int16" "l_tax-int16.csv"
	decode_and_check $tech "int32" "l_tax-int32.csv"
	decode_and_check $tech "int64" "l_tax-int64.csv"
	decode_and_check $tech "int8" "l_tax-int8.csv"
done