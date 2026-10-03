import sys, requests, re, time
from bs4 import BeautifulSoup

def fetch(ticker, field):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    # headers = {
    #     "accept": "text/html",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.132 Safari/537.36"
    # }
    headers = {
        "accept": "text/html",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    if r.status_code != 200:
        raise Exception(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    for row in soup.select('div.row.lv-0'):
        if (lab := row.find('div', class_=re.compile('rowTitle'))) and lab.text.strip() == field:
            vals = [v.text.strip() for v in row.find_all('div', class_=re.compile('column yf-'))]
            return (field, *vals)
    raise Exception('Field not found')

# if __name__ == '__main__':
#     try:
#         print(fetch(sys.argv[1], sys.argv[2]))
#         time.sleep(5)
#     except Exception as e:
#         print(e)