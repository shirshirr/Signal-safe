import json
from pathlib import Path
import pandas as pd

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_news(path=DATA_DIR / "sample_news.jsonl"):
    items = []
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            items.append(json.loads(line))
    df = pd.DataFrame(items)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

def load_prices(path=DATA_DIR / "prices.csv"):
    df = pd.read_csv(path, parse_dates=['date'])
    return df

if __name__ == '__main__':
    news = load_news()
    prices = load_prices()
    print("news sample:", news.head(2).to_dict(orient='records'))
    print("prices sample:", prices.head())
