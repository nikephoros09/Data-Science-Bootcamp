#!/bin/sh

input_csv="../ex01/hh.csv"
output_csv="hh_sorted.csv"

head -n 1 "$input_csv" > "$output_csv"
tail -n +2 "$input_csv" | sort -t, -k2,2 -k1,1 >> "$output_csv"
