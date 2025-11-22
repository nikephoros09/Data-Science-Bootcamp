input_csv="../ex03/hh_positions.csv"

header=$(head -n 1 "$input_csv")

tail -n +2 "$input_csv" | while IFS= read -r line
do
    field2=$(echo "$line" | cut -d',' -f2)
    date_part=$(echo "$field2" | cut -d'T' -f1)

    file="res/${date_part}.csv"

    if [ ! -f "$file" ]; then
        echo "$header" > "$file"
    fi

    echo "$line" >> "$file"
done