class MustRead:
    the_file = "./data.csv"
    with open(the_file) as f:
        print(f.read())

if __name__ == "__main__":
    MustRead()