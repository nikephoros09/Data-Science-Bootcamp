import sys
import urllib3
import re
from bs4 import BeautifulSoup

def fetch(ticker, field):
    url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    headers = {
        "accept": "text/html",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.7151.132 Safari/537.36"
        ),
        "referer": f"https://finance.yahoo.com/quote/{ticker}"
    }

    http = urllib3.PoolManager(
        headers=headers,
        timeout=urllib3.Timeout(connect=5.0, read=15.0)
    )

    response = http.request('GET', url, preload_content=True)

    if response.status != 200:
        raise Exception(response.status)

    soup = BeautifulSoup(response.data, 'html.parser')
    for row in soup.select('div.row.lv-0'):
        lab = row.find('div', class_=re.compile('rowTitle'))
        if lab and lab.text.strip() == field:
            vals = [v.text.strip() for v in row.find_all('div', class_=re.compile('column yf-'))]
            return (field, *vals)
    raise Exception('Field not found')

if __name__ == '__main__':
    try:
        print(fetch(sys.argv[1], sys.argv[2]))
        # time.sleep(5)
    except Exception as e:
        print(e)