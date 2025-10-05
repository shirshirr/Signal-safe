import json
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

def generate():
    start = datetime(2023, 9, 1)
    tick = 'AAPL'
    news = []
    for i in range(10):
        d = start + timedelta(days=i)
        for j in range(2):
            item = {
                'id': f'{tick}_{i}_{j}',
                'source': 'synthetic',
                'datetime': (d.replace(hour=9+j)).isoformat(),
                'text': f'Synthetic headline {i}-{j} about {tick}',
                'ticker': tick
            }
            news.append(item)
    with open(DATA_DIR / 'sample_news.jsonl','w',encoding='utf8') as f:
        for it in news:
            f.write(json.dumps(it) + '\n')

    import csv
    with open(DATA_DIR / 'prices.csv','w',newline='',encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['date','ticker','open','high','low','close','volume'])
        price = 150.0
        for i in range(10):
            d = (start + timedelta(days=i)).date().isoformat()
            open_p = round(price + (i%3 - 1) * 0.5, 2)
            close_p = round(open_p + (0.5 if i%2==0 else -0.3),2)
            high_p = max(open_p, close_p) + 0.5
            low_p = min(open_p, close_p) - 0.5
            volume = 1000000 + i*1000
            writer.writerow([d, tick, open_p, high_p, low_p, close_p, volume])
            price = close_p
    print('Generated sample data in data/')

if __name__ == '__main__':
    generate()
