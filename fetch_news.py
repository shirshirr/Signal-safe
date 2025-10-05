import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from textblob import TextBlob
import time

load_dotenv()  # loads .env file

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # make sure your .env has it

def fetch_stock_news(ticker, days_back=7, retries=3):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}&"
        f"from={start_date.strftime('%Y-%m-%d')}&"
        f"to={end_date.strftime('%Y-%m-%d')}&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={NEWS_API_KEY}"
    )
    
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=30)
            data = response.json()
            
            # check for errors from API
            if data.get("status") != "ok":
                print("News API error:", data.get("message"))
                return pd.DataFrame()
            
            articles = data.get("articles", [])
            news_list = []
            
            for a in articles:
                title = a["title"]
                url = a["url"]
                publishedAt = a["publishedAt"]
                
                # sentiment scoring
                sentiment = TextBlob(title).sentiment.polarity
                news_list.append({
                    "title": title,
                    "url": url,
                    "publishedAt": publishedAt,
                    "sentiment": sentiment
                })
            
            df = pd.DataFrame(news_list)
            df.to_csv(f"{ticker}_real_news.csv", index=False)
            print(f"Saved {len(df)} articles to {ticker}_real_news.csv")
            return df
        
        except Exception as e:
            print(f"Error fetching news (attempt {attempt+1}): {e}")
            attempt += 1
            time.sleep(5)  # wait 5 seconds before retrying
    
    print("Failed to fetch news after retries.")
    return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_stock_news("AAPL")  # replace with any stock/company
    print(df.head())
