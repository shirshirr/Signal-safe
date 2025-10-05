import requests
import pandas as pd
from textblob import TextBlob
from datetime import datetime, timedelta

# Replace with your NewsAPI key
API_KEY = "YOUR_NEWSAPI_KEY"

# List of stocks you want to track
TICKERS = ["AAPL", "MSFT", "TSLA", "RELIANCE.NS"]

# Dates
to_date = datetime.now().date()
from_date = to_date - timedelta(days=7)  # last 7 days

all_news = []

for ticker in TICKERS:
    print(f"Fetching news for {ticker}...")
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}&from={from_date}&to={to_date}"
        f"&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("articles"):
            for article in data["articles"]:
                title = article.get("title", "")
                url_link = article.get("url", "")
                published_at = article.get("publishedAt", "")
                # Sentiment analysis
                sentiment = TextBlob(title).sentiment.polarity
                all_news.append({
                    "ticker": ticker,
                    "title": title,
                    "url": url_link,
                    "publishedAt": published_at,
                    "sentiment": sentiment
                })

    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")

# Save to CSV
df = pd.DataFrame(all_news)
df.to_csv("multi_stock_news.csv", index=False)
print(f"Saved {len(df)} articles to multi_stock_news.csv")
