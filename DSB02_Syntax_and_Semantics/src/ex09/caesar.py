import sys
def caesar():
    if len(sys.argv) != 4:
        raise Exception("Invalid number of arguments")
    operation_mode = sys.argv[1]
    input_text = sys.argv[2]
    if input_text.isascii() == False:
        raise Exception("The script does not support your language yet.")
    shift = int(sys.argv[3])
    signed_shift = shift if operation_mode == 'encode' else -shift
    final_result = ''
    for curr_char in input_text:
        if 'a' <= curr_char <= 'z':
            letter_a = ord('a')
            new_curr_char = chr(letter_a + (ord(curr_char) - letter_a +  signed_shift) % 26)
            final_result += new_curr_char
        elif 'A' <= curr_char <= 'Z':
            letter_a = ord('A')
            new_curr_char = chr(letter_a + (ord(curr_char) - letter_a +  signed_shift) % 26)
            final_result += new_curr_char
        else:
            final_result += curr_char
    print(final_result)
if __name__ == '__main__':
    caesar()