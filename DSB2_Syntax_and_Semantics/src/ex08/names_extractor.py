import sys

def names_extractor():
    input_file = sys.argv[1]
    with open(input_file) as file_input, open('employees.tsv', 'w') as file_output:
        file_output.write('Name\tSurname\tE-mail\n')
        for line in file_input:
            email = line.strip()
            full_name = email.split('@')[0].split('.')
            name = full_name[0].capitalize()
            surname = full_name[1].capitalize()
            file_output.write(f"{name}\t{surname}\t{email}\n")

if __name__ == '__main__':
    names_extractor()
