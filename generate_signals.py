import pandas as pd

# Step 1: Read your CSV
df = pd.read_csv("multi_stock_news.csv")

# Step 2: Make sure 'sentiment' is numeric
df['sentiment'] = pd.to_numeric(df['sentiment'], errors='coerce')

# Step 3: Aggregate sentiment per stock
agg_sentiment = df.groupby('ticker')['sentiment'].mean().reset_index()

# Step 4: Generate simple buy/hold/sell signals
def generate_signal(score):
    if score > 0.1:
        return "BUY"
    elif score < -0.1:
        return "SELL"
    else:
        return "HOLD"

agg_sentiment['signal'] = agg_sentiment['sentiment'].apply(generate_signal)

# Step 5: Save the result
agg_sentiment.to_csv("stock_signals.csv", index=False)

print("Signals generated successfully! Check 'stock_signals.csv'")
print(agg_sentiment)
