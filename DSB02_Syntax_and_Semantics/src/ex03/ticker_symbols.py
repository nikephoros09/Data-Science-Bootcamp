import sys

def ticker_symbols():
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
        ticker = sys.argv[1].upper()
        if ticker in STOCKS:
            full_name = [key for key, value in COMPANIES.items() if value == ticker]
            if full_name:
                print(f"{full_name[0]} {STOCKS[ticker]}")
            else:
                print("Unknown ticker")
        else:
            print("Unknown ticker")

if __name__ == "__main__":
    ticker_symbols()