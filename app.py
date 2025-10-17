from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    signals_df = pd.read_csv("stock_signals.csv")
    companies = signals_df['ticker'].unique()  # use 'ticker' column
    return render_template("index.html", companies=companies)

@app.route("/dashboard")
def dashboard():
    selected_company = request.args.get("company")
    signals_df = pd.read_csv("stock_signals.csv")
    news_df = pd.read_csv("multi_stock_news.csv")  # if you have news
    
    # Filter data for selected company
    company_signals = signals_df[signals_df['ticker'] == selected_company].to_dict(orient="records")
    company_news = news_df[news_df['ticker'] == selected_company].to_dict(orient="records")
    
    return render_template(
        "dashboard.html",
        company=selected_company,
        signals=company_signals,
        news=company_news
    )

if __name__ == "__main__":
    app.run(debug=True)
