
from random import randint
class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True):
        with open(self.file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise Exception("Wrong file structure!")

        start = 0
        if has_header:
            header = lines[0].split(',')
            if len(header) != 2 or not header[0] or not header[1]:
                raise Exception("Wrong file structure")
            start = 1

        allowed_values = {"0", "1"}
        result = []

        for line in lines[start:]:
            columns = [item.strip() for item in line.split(',')]
            if len(columns) != 2 or not all(c in allowed_values for c in columns):
                raise Exception("Wrong file structure")
            if columns[0] == columns[1]:
                raise Exception("Wrong file structure")
            result.append([int(columns[0]), int(columns[1])])
        if not result:
            raise Exception("Wrong file structure")
        return result

    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            heads = sum(row[0] for row in self.data)
            tails = sum(row[1] for row in self.data)
            return heads, tails

        def fractions(self, heads, tails):
            total = heads + tails
            heads_percent = heads / total
            tails_percent = tails / total
            return round(heads_percent, 4), round(tails_percent, 4)

    class Analytics(Calculations):
        def predict_random(self, num_predictions):
            result = []
            for _ in range(num_predictions):
                item = randint(0,1)
                result.append([item, 1-item])
     
            return result

        def predict_last(self):
            return self.data[-1]
        
        @staticmethod
        def save_file(data, filename, extension):
            with open(f"{filename}.{extension}", "w") as file:
                file.write(str(data))
        

