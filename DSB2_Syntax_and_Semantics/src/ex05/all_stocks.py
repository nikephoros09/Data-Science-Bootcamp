import sys

def all_stocks():
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
    TICKERS = {v: k for k, v in COMPANIES.items()}
    LOWER_COMPANIES = [k.lower() for k in COMPANIES]
        
    if len(sys.argv) != 2:
        return

    arg = sys.argv[1]

    if ',,' in arg:
        return

    substrings = arg.split(',')
    stripped_substrings = [substr.strip() for substr in substrings]
    if any(substr == '' for substr in stripped_substrings):
        return

    output = []
    for substr in stripped_substrings:
        upper_substr = substr.upper()
        if upper_substr in TICKERS:
            company = TICKERS[upper_substr]
            output.append(f"{upper_substr} is a ticker symbol for {company}")
        else:
            lower_substr = substr.lower()
            if lower_substr in LOWER_COMPANIES:
                index = LOWER_COMPANIES.index(lower_substr)
                company = list(COMPANIES.keys())[index]
                ticker = COMPANIES[company]
                price = STOCKS[ticker]
                output.append(f"{company} stock price is {price}")
            else:
                cap_substr = substr.capitalize()
                output.append(f"{cap_substr} is an unknown company or an unknown ticker symbol")

    if output:
        print('\n'.join(output))

if __name__ == '__main__':
    all_stocks()