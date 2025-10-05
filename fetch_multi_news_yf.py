import yfinance as yf
import pandas as pd
from textblob import TextBlob

TICKERS = ["AAPL", "MSFT", "TSLA", "RELIANCE.NS"]

all_news = []

for ticker in TICKERS:
    print(f"Fetching news for {ticker}...")
    stock = yf.Ticker(ticker)
    news_items = stock.news  # returns list of dicts

    for article in news_items:
        title = article.get("title", "")
        url_link = article.get("link", "")
        published_at = article.get("providerPublishTime", "")
        if published_at:
            published_at = pd.to_datetime(published_at, unit="s")
        sentiment = TextBlob(title).sentiment.polarity
        all_news.append({
            "ticker": ticker,
            "title": title,
            "url": url_link,
            "publishedAt": published_at,
            "sentiment": sentiment
        })

df = pd.DataFrame(all_news)
df.to_csv("multi_stock_news.csv", index=False)
print(f"Saved {len(df)} articles to multi_stock_news.csv")
