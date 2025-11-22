#!/bin/sh

input_csv="../ex03/hh_positions.csv"
output_csv="hh_uniq_positions.csv"

printf '"name","count"\n' > "$output_csv"

tail -n +2 "$input_csv" |
cut -d',' -f3 |
tr -d '"' |
sort |
uniq -c |
sort -k1,1nr |
awk '{print "\"" $2 "\"," $1}' >> "$output_csv"