import sys

def letter_starter():
    needed_email = sys.argv[1]
    with open('employees.tsv', 'r') as f:
        next(f)
        for line in f:
            list_as_list = line.strip().split('\t')
            if list_as_list[2] == needed_email:
                needed_name = list_as_list[0]
    letter = (f"Dear {needed_name}, welcome to our team! We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.")
    print(letter)

if __name__ == '__main__':
    letter_starter()