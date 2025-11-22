import sys
class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True):
        with open(self.file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise Exception("Wrong file structure")

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
        def counts(data):
            heads = sum(row[0] for row in data)
            tails = sum(row[1] for row in data)
            return heads, tails

        def fractions(heads, tails):
            total = heads + tails
            heads_percent = heads / total
            tails_percent = tails  / total
            return round(heads_percent,4), round(tails_percent,4)
if __name__ == '__main__':
        research = Research(sys.argv[1])
        raw_count = research.file_reader(has_header=True)
        print(raw_count)
        heads, tails = research.Calculations.counts(raw_count)
        print(f'{heads} {tails}')
        heads_fraction, tails_fraction = research.Calculations.fractions(heads, tails)
        print(f'{heads_fraction} {tails_fraction}')
