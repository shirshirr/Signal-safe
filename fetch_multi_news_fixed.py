from GoogleNews import GoogleNews
import pandas as pd
from textblob import TextBlob

# List of stock tickers
tickers = ["AAPL", "MSFT", "TSLA", "RELIANCE.NS"]

all_articles = []

googlenews = GoogleNews(lang='en')

for ticker in tickers:
    print(f"Fetching news for {ticker}...")
    googlenews.clear()
    googlenews.search(ticker)
    results = googlenews.results()
    
    for article in results:
        title = article.get('title', '')
        url = article.get('link', '')
        publishedAt = article.get('date', '')
        
        # Fix: remove Google redirect parameters
        url = url.split("&ved=")[0] if url else ''
        
        # Sentiment analysis
        sentiment = round(TextBlob(title).sentiment.polarity, 9) if title else 0
        
        all_articles.append({
            'ticker': ticker,
            'title': title,
            'url': url,
            'publishedAt': publishedAt,
            'sentiment': sentiment
        })

# Save to CSV
df = pd.DataFrame(all_articles)
df.to_csv("multi_stock_news.csv", index=False)

print(f"Saved {len(all_articles)} articles to multi_stock_news.csv")
