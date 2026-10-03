def csv_line_to_tsv(line):
    result =[] 
    field = ''
    inside_quotes = False

    for char in line:
        if char == '"':
            inside_quotes = not inside_quotes
            continue
        if char == ',' and not inside_quotes:
            result.append(field)
            field = ''
        else:
            field += char
    result.append(field)
    return '\t'.join(result)

def convert_csv_to_tsv(csv_input='./ds.csv', tsv_output='./ds.tsv'):
    with open(csv_input, 'r', encoding='utf-8') as to_format, \
         open(tsv_output, 'w', encoding='utf-8') as formatted:
        for line in to_format:
            tsv_line = csv_line_to_tsv(line)
            formatted.write(tsv_line)

if __name__ == '__main__':
    convert_csv_to_tsv() 