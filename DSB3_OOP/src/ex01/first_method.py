class Research:
    def file_reader():
        the_file = "./data.csv"
        with open(the_file) as f:
            return f.read()
if __name__ == "__main__":
    print(Research.file_reader())