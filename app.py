from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Helper functions to read CSVs
def get_news():
    try:
        news_df = pd.read_csv("multi_stock_news.csv")
        # latest 5 news per ticker
        news_df = news_df.groupby("ticker").head(5)
        return news_df.to_dict(orient="records")
    except:
        return []

def get_signals():
    try:
        signals_df = pd.read_csv("stock_signals.csv")
        return signals_df.to_dict(orient="records")
    except:
        return []

@app.route('/')
def home():
    news = get_news()
    signals = get_signals()
    return render_template('index.html', news=news, signals=signals)

if __name__ == "__main__":
    app.run(debug=True)
