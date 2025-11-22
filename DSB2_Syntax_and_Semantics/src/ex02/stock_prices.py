import sys

def stock_prices():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
        }
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
        }
    if len(sys.argv) == 2:
        name = sys.argv[1].capitalize()
        if name in COMPANIES:
            print(STOCKS[COMPANIES[name]])
        else:
            print("Unknown company")

if __name__ == "__main__":
    stock_prices()