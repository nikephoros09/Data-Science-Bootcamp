#!/bin/sh

output_csv="hh_concatenated.csv"

is_first=1
for file in $(ls res/*.csv | sort -n); do
    if (( is_first )); then
        cat "$file" > "$output_csv"
        is_first=0
    else
        tail -n +2 "$file" >> "$output_csv"
    fi
done