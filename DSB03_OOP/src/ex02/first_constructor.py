import sys

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self):
      
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
        if len(lines) < 2:
            raise Exception("Wrong file structure")
        header = lines[0].strip().split(',')
        if len(header) != 2 or not header[0] or not header[1]:
            raise Exception("Wrong file structure")

        allowed_values = {"0", "1"}
        
        for line in lines[1:]:
            columns = [item.strip() for item in line.strip().split(',')]
            if len(columns) != 2 or not all(item in allowed_values for item in columns):
                raise Exception("Wrong file structure")
            if columns[0] == columns[1]:
                raise Exception("Wrong file structure")

        return ''.join(lines)

if __name__ == '__main__':
        research = Research(sys.argv[1])
        final_res = research.file_reader()
        print(final_res)

