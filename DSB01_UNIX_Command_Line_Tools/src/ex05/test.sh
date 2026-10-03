#!/bin/sh

res03="../ex03/hh_positions.csv"
res05="../ex05/hh_concatenated.csv"

if cmp -s "$res03" "$res05"; then
    echo "Результаты заданий 3 и 5 одинаковы"
else
    echo "Результаты заданий 3 и 5 отличаются"
fi